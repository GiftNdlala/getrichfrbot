"""
Get Rich FR Bot - Professional Live Trading Signal Dashboard
Clean implementation with real market data and professional branding
Created by Gift Ndlala
"""

from flask import Flask, render_template, jsonify, request
from dataclasses import asdict
import logging
import threading
import time
import json
from datetime import datetime
import os
import sys

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.live_data_stream import LiveDataStream, LiveSignal
from src.config import get_config
from src.persistence import PersistenceManager
from src.mt5_connector import MT5Connector
from src.executor import AutoTrader

app = Flask(__name__)

# Global variables
streams = {}
streams_lock = threading.RLock()
current_signal_data = None
signal_history = []
persistence = PersistenceManager()
# Auto-take-profit settings
auto_take_profit = {
    'enabled': False,
    'threshold': 30.0  # Default threshold
}
auto_tp_lock = threading.Lock()
auto_tp_stop = threading.Event()
auto_tp_thread = None


def _requested_symbol(payload=None):
    """Read a symbol consistently from JSON, query string, or the configured default."""
    payload = payload or {}
    return (
        payload.get('symbol')
        or request.args.get('symbol')
        or get_config().get('broker', {}).get('symbol', 'XAUUSD')
    )


def configure_dashboard_logging() -> bool:
    """Control whether Flask request/access logs are shown in the terminal."""
    cfg = get_config()
    enabled = bool(cfg.get('logging', {}).get('dashboard_access_logs', False))

    werkzeug_logger = logging.getLogger('werkzeug')
    app_logger = logging.getLogger('flask.app')
    if enabled:
        werkzeug_logger.setLevel(logging.INFO)
        app_logger.setLevel(logging.INFO)
        print("📝 Dashboard access logs: ENABLED")
    else:
        werkzeug_logger.setLevel(logging.ERROR)
        app_logger.setLevel(logging.ERROR)
        print("🔇 Dashboard access logs: DISABLED")
    return enabled

def init_live_stream():
    """Initialize live data streams for configured symbols"""
    global streams

    # The dashboard can be started by a service manager, a local operator, or
    # the resume endpoint.  Make startup idempotent so one process cannot
    # accidentally create two workers for the same symbol.
    with streams_lock:
        if any(stream.is_running for stream in streams.values()):
            return streams
        streams.clear()
    
    def signal_callback(signal: LiveSignal):
        global current_signal_data, signal_history
        
        # Sanitize values to be JSON-safe (no NaN/inf)
        def sanitize(value):
            try:
                if value is None:
                    return 0
                if isinstance(value, float):
                    if value != value or value == float('inf') or value == float('-inf'):
                        return 0.0
                return value
            except Exception:
                return 0

        current_signal_data = {
            'timestamp': signal.timestamp,
            'symbol': signal.symbol,
            'current_price': sanitize(signal.current_price),
            'signal': int(sanitize(signal.signal)),
            'signal_type': signal.signal_type,
            'confidence': sanitize(signal.confidence),
            'rsi': sanitize(signal.rsi),
            'macd': sanitize(signal.macd),
            'macd_signal': sanitize(signal.macd_signal),
            'sma_20': sanitize(signal.sma_20),
            'sma_50': sanitize(signal.sma_50),
            'price_change': sanitize(signal.price_change),
            'price_change_pct': sanitize(signal.price_change_pct),
            
            # Alert Category Data
            'alert_level': signal.alert_level,
            'alert_color': signal.alert_color,
            'target_pips': int(sanitize(signal.target_pips)),
            'success_rate': sanitize(signal.success_rate),
            
            # Risk Management Data
            'entry_price': sanitize(signal.entry_price),
            'stop_loss': sanitize(signal.stop_loss),
            'take_profit_1': sanitize(signal.take_profit_1),
            'take_profit_2': sanitize(signal.take_profit_2),
            'take_profit_3': sanitize(signal.take_profit_3),
            'risk_reward_ratio': sanitize(signal.risk_reward_ratio),
            'atr_value': sanitize(signal.atr_value),
            'position_size_percent': sanitize(signal.position_size_percent),
            'risk_amount_dollars': sanitize(signal.risk_amount_dollars),
            'potential_profit_tp1': sanitize(signal.potential_profit_tp1),
            'potential_profit_tp2': sanitize(signal.potential_profit_tp2),
            'potential_profit_tp3': sanitize(signal.potential_profit_tp3)
        }
        
        # Add to history safely
        if not isinstance(signal_history, list):
            signal_history = []
        
        signal_history.append(current_signal_data.copy())
        if len(signal_history) > 10:
            signal_history.pop(0)
        
        # Print signal update with alert categorization (disabled by default; dashboard still updates)
        if signal.signal != 0:
            try:
                print_signal_alerts = os.getenv("PRINT_SIGNAL_ALERTS", "0").strip().lower() in {"1", "true", "yes", "on"}
            except Exception:
                print_signal_alerts = False

            if print_signal_alerts:
                alert_emoji = {'HIGH': '🔴', 'MEDIUM': '🟡', 'LOW': '🟢'}.get(signal.alert_level, '⭕')
                print(f"🎯 {signal.signal_type} SIGNAL: ${signal.current_price:.2f} | {alert_emoji} {signal.alert_level} ALERT")
                print(f"   Target: {signal.target_pips} pips | Success Rate: {signal.success_rate:.1f}% | Confidence: {signal.confidence:.1f}%")
    
    # Create and start live stream with REAL market data
    cfg = get_config()
    symbol = cfg.get('broker', {}).get('symbol', 'XAUUSD')
    # Start XAUUSDm (from config)
    gold_stream = LiveDataStream(symbol=symbol, update_interval=30)
    gold_stream.add_signal_callback(signal_callback)
    gold_stream.start_streaming()
    with streams_lock:
        streams[symbol] = gold_stream

    # Start US30m secondary stream
    try:
        us_symbol = os.getenv('US30_SYMBOL', 'US30m')
        us_stream = LiveDataStream(symbol=us_symbol, update_interval=30)
        us_stream.add_signal_callback(signal_callback)
        us_stream.start_streaming()
        with streams_lock:
            streams[us_symbol] = us_stream
        print(f"✅ Live stream initialized for {us_symbol}")
        # Sanity log to ensure data source path awareness
        try:
            mapped = getattr(us_stream, 'yf_symbol', us_symbol)
            print(f"🔎 {us_symbol} mapped to data source: {mapped}")
        except Exception:
            pass
    except Exception as e:
        print(f"⚠️ Could not start US30 stream: {e}")
    print("✅ Live streams initialized and started")
    return streams


def stop_live_streams(join_timeout: float = 10.0):
    """Stop all stream workers and wait briefly for clean shutdown."""
    with streams_lock:
        active_streams = list(streams.values())
        streams.clear()

    for stream in active_streams:
        try:
            stream.stop_streaming()
        except Exception as exc:
            print(f"⚠️ Error stopping {getattr(stream, 'symbol', 'stream')}: {exc}")

    for stream in active_streams:
        worker = getattr(stream, 'stream_thread', None)
        if worker and worker.is_alive():
            worker.join(timeout=join_timeout)


def start_background_monitors():
    """Start process-level monitors exactly once."""
    global auto_tp_thread
    if auto_tp_thread and auto_tp_thread.is_alive():
        return auto_tp_thread
    auto_tp_stop.clear()
    auto_tp_thread = threading.Thread(
        target=monitor_auto_take_profit,
        args=(auto_tp_stop,),
        name='auto-take-profit-monitor',
        daemon=True,
    )
    auto_tp_thread.start()
    return auto_tp_thread


def stop_background_monitors(join_timeout: float = 10.0):
    """Ask process-level monitors to stop and wait for them."""
    auto_tp_stop.set()
    if auto_tp_thread and auto_tp_thread.is_alive():
        auto_tp_thread.join(timeout=join_timeout)

# Routes
@app.route('/')
def dashboard():
    """Main dashboard page - Live Signals"""
    return render_template('dashboard.html', page='live')

@app.route('/live')
def live_signals():
    """Live Signals page"""
    return render_template('dashboard.html', page='live')

@app.route('/history')
def signal_history_page():
    """Signal History page"""
    return render_template('dashboard.html', page='history')

@app.route('/analytics') 
def analytics():
    """Analytics & Performance page"""
    return render_template('dashboard.html', page='analytics')

@app.route('/settings')
def settings():
    """Settings & Configuration page"""
    return render_template('dashboard.html', page='settings')

@app.route('/about')
def about():
    """About page"""
    return render_template('dashboard.html', page='about')

# API Routes
@app.route('/api/current_signal')
def get_current_signal():
    """API endpoint to get current signal data; accepts ?symbol="""
    sym = request.args.get('symbol') or get_config().get('broker', {}).get('symbol', 'XAUUSD')
    stream = streams.get(sym)
    if stream and stream.get_current_signal():
        return jsonify({'status':'success','data': asdict(stream.get_current_signal()), 'last_update': datetime.now().isoformat()})
    # Fallback DB
    last = persistence.latest_signal()
    if last:
        return jsonify({'status': 'success', 'data': last, 'last_update': datetime.now().isoformat()})
    return jsonify({'status': 'waiting', 'message': 'Waiting for first signal...', 'last_update': datetime.now().isoformat()})

@app.route('/api/signal_history')
def get_signal_history():
    """API endpoint to get signal history; accepts ?symbol & limit"""
    db_signals = []
    try:
        db_signals = persistence.recent_signals(10)
    except Exception:
        pass
    fallback = signal_history if isinstance(signal_history, list) else []
    data = db_signals if db_signals else fallback
    return jsonify({'status': 'success', 'data': data, 'count': len(data)})

@app.route('/api/status')
def get_status():
    """API endpoint to get system status; accepts ?symbol"""
    sym = request.args.get('symbol') or get_config().get('broker', {}).get('symbol', 'XAUUSD')
    stream = streams.get(sym)
    if stream:
        st = stream.get_status()
        st['dashboard_status'] = 'running'
        st['real_data'] = 'active'
        st['symbol'] = sym
        return jsonify(st)
    return jsonify({'dashboard_status': 'initializing', 'real_data': 'loading', 'symbol': sym})


@app.route('/api/health')
def health_check():
    """Small liveness/readiness endpoint for Windows services and Cloudflared."""
    now = datetime.now()
    with streams_lock:
        current_streams = list(streams.values())

    stream_health = {}
    ready = bool(current_streams)
    for stream in current_streams:
        status = stream.get_status()
        last_update = status.get('last_update')
        age_seconds = None
        if last_update:
            try:
                age_seconds = max(0.0, (now - datetime.fromisoformat(last_update)).total_seconds())
            except ValueError:
                age_seconds = None
        # A stream is considered ready only after it has produced a recent
        # update.  The generous threshold covers a temporary market/data pause.
        stream_ready = (
            bool(status.get('is_running'))
            and bool(status.get('worker_alive'))
            and (age_seconds is not None and age_seconds <= 180)
        )
        ready = ready and stream_ready
        stream_health[stream.symbol] = {
            'is_running': bool(status.get('is_running')),
            'worker_alive': bool(status.get('worker_alive')),
            'last_update': last_update,
            'age_seconds': age_seconds,
            'ready': stream_ready,
        }

    payload = {
        'status': 'ready' if ready else 'starting',
        'service': 'get-rich-fr-bot',
        'checked_at': now.isoformat(),
        'streams': stream_health,
        'auto_take_profit_monitor': bool(auto_tp_thread and auto_tp_thread.is_alive()),
    }
    return jsonify(payload), (200 if ready else 503)

@app.route('/api/trades')
def get_trades():
    symbol = request.args.get('symbol')
    try:
        open_trades = persistence.get_open_trades(symbol)
    except Exception:
        open_trades = []
    return jsonify({'status': 'success', 'open_trades': open_trades})

@app.route('/api/recent_trades')
def get_recent_trades():
    try:
        hours = int(request.args.get('hours', 20))
        limit = int(request.args.get('limit', 200))
    except Exception:
        hours, limit = 20, 200
    try:
        rows = persistence.recent_trades(hours=hours, limit=limit)
    except Exception:
        rows = []
    return jsonify({'status': 'success', 'trades': rows, 'hours': hours, 'count': len(rows)})

@app.route('/api/pause', methods=['POST'])
def pause_trading():
    global streams
    sym = request.args.get('symbol') or get_config().get('broker', {}).get('symbol', 'XAUUSD')
    with streams_lock:
        s = streams.get(sym)
    if s:
        s.is_running = False
        return jsonify({'status': 'paused', 'symbol': sym})
    return jsonify({'status': 'no_stream'})

@app.route('/api/resume', methods=['POST'])
def resume_trading():
    global streams
    sym = request.args.get('symbol') or get_config().get('broker', {}).get('symbol', 'XAUUSD')
    with streams_lock:
        s = streams.get(sym)
    if s and not s.is_running:
        s.start_streaming()
        return jsonify({'status': 'resumed', 'symbol': sym})
    return jsonify({'status': 'no_stream'})

@app.route('/api/session_toggle', methods=['POST'])
def session_toggle():
    global streams
    force = request.json.get('force', False)
    sym = request.args.get('symbol') or get_config().get('broker', {}).get('symbol', 'XAUUSD')
    s = streams.get(sym)
    if s:
        s.ignore_session_filter = bool(force)
        return jsonify({'status': 'success', 'symbol': sym, 'ignore_session_filter': s.ignore_session_filter})
    return jsonify({'status': 'no_stream'})

@app.route('/api/farmer_toggle', methods=['POST'])
def farmer_toggle():
    global streams
    payload = request.get_json(silent=True) or {}
    enabled = bool(payload.get('enabled', False))
    sym = _requested_symbol(payload)
    s = streams.get(sym)
    if s:
        s.set_farmer_enabled(enabled)
        return jsonify({'status': 'success', 'symbol': sym, 'farmer_enabled': s.farmer_enabled})
    return jsonify({'status': 'no_stream'})

@app.route('/api/engine_toggle', methods=['POST'])
def engine_toggle():
    global streams
    payload = request.get_json(silent=True) or {}
    sym = _requested_symbol(payload)
    s = streams.get(sym)
    if not s:
        return jsonify({'status': 'no_stream'})
    level = payload.get('level')
    enabled = bool(payload.get('enabled', True))
    s.set_engine_enabled(level, enabled)
    return jsonify({'status': 'success','symbol': sym,'level': level,'engine_low_enabled': s.enable_low,'engine_medium_enabled': s.enable_medium,'engine_high_enabled': s.enable_high})

@app.route('/api/engine_analytics')
def engine_analytics():
    hours = int(request.args.get('hours', 20))
    # optional symbol filter later
    try:
        rows = persistence.recent_trades(hours=hours, limit=2000)
    except Exception:
        rows = []
    counts = {'FARMER': 0, 'INTRADAY_LOW': 0, 'INTRADAY_MED': 0, 'SWING_HIGH': 0, 'INTRADAY': 0}
    for r in rows:
        engine = r.get('engine') or ''
        if engine in counts:
            counts[engine] += 1
    return jsonify({'status': 'success', 'hours': hours, 'counts': counts})

@app.route('/api/event_toggle', methods=['POST'])
def event_toggle():
    global streams
    payload = request.get_json(silent=True) or {}
    enabled = bool(payload.get('enabled', False))
    sym = _requested_symbol(payload)
    s = streams.get(sym)
    if s:
        s.set_event_mode(enabled)
        return jsonify({'status': 'success', 'symbol': sym, 'event_mode_enabled': s.event_mode_enabled})
    return jsonify({'status': 'no_stream'})

@app.route('/api/engine_mode', methods=['POST'])
def engine_mode():
    global streams
    payload = request.get_json(silent=True) or {}
    mode = payload.get('mode', 'ALL')
    sym = _requested_symbol(payload)
    s = streams.get(sym)
    if s:
        try:
            s.set_engine_mode(mode)
            return jsonify({
                'status': 'success',
                'symbol': sym,
                'engine_mode': s.engine_mode,
                'engine_low_enabled': s.enable_low,
                'engine_medium_enabled': s.enable_medium,
                'engine_high_enabled': s.enable_high,
                'farmer_enabled': s.farmer_enabled,
                'event_mode_enabled': s.event_mode_enabled
            })
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 400
    return jsonify({'status': 'no_stream'})

@app.route('/api/trading_toggle', methods=['POST'])
def trading_toggle():
    global streams
    payload = request.get_json(silent=True) or {}
    symbol = _requested_symbol(payload)
    stream = streams.get(symbol)
    if not stream:
        return jsonify({'status': 'no_stream'}), 404
    enabled = bool(payload.get('enabled', False))
    stream.set_trading_enabled(enabled)
    return jsonify({
        'status': 'success',
        'symbol': symbol,
        'trading_enabled': stream.trading_enabled,
        'engine_mode': stream.engine_mode
    })

@app.route('/api/nyupip/toggle', methods=['POST'])
def nyupip_toggle():
    global streams
    payload = request.get_json(silent=True) or {}
    enabled = bool(payload.get('enabled', False))
    sym = _requested_symbol(payload)
    s = streams.get(sym)
    if not s:
        return jsonify({'status': 'no_stream'}), 404
    try:
        s.set_nyupip_enabled(enabled)
        state = s.get_nyupip_state()
        return jsonify({'status': 'success', 'symbol': sym, 'enabled': state['enabled'], 'state': state})
    except Exception as exc:
        return jsonify({'status': 'error', 'message': str(exc)}), 500

@app.route('/api/nyupip/status')
def nyupip_status():
    global streams
    sym = request.args.get('symbol') or get_config().get('broker', {}).get('symbol', 'XAUUSD')
    s = streams.get(sym)
    if not s:
        return jsonify({'status': 'no_stream'}), 404
    state = s.get_nyupip_state()
    return jsonify({'status': 'success', 'symbol': sym, 'state': state})


@app.route('/api/ict_swing/toggle', methods=['POST'])
def ict_swing_toggle():
    global streams
    payload = request.get_json(silent=True) or {}
    enabled = bool(payload.get('enabled', False))
    sym = _requested_symbol(payload)
    s = streams.get(sym)
    if not s:
        return jsonify({'status': 'no_stream'}), 404
    try:
        s.set_ict_swing_enabled(enabled)
        state = s.get_ict_swing_state()
        return jsonify({'status': 'success', 'symbol': sym, 'enabled': state['enabled'], 'state': state})
    except Exception as exc:
        return jsonify({'status': 'error', 'message': str(exc)}), 500


@app.route('/api/ict_swing/status')
def ict_swing_status():
    global streams
    sym = request.args.get('symbol') or get_config().get('broker', {}).get('symbol', 'XAUUSD')
    s = streams.get(sym)
    if not s:
        return jsonify({'status': 'no_stream'}), 404
    state = s.get_ict_swing_state()
    return jsonify({'status': 'success', 'symbol': sym, 'state': state})


@app.route('/api/ict_atm/toggle', methods=['POST'])
def ict_atm_toggle():
    global streams
    payload = request.get_json(silent=True) or {}
    enabled = bool(payload.get('enabled', False))
    sym = _requested_symbol(payload)
    s = streams.get(sym)
    if not s:
        return jsonify({'status': 'no_stream'}), 404
    try:
        s.set_ict_atm_enabled(enabled)
        state = s.get_ict_atm_state()
        return jsonify({'status': 'success', 'symbol': sym, 'enabled': state['enabled'], 'state': state})
    except Exception as exc:
        return jsonify({'status': 'error', 'message': str(exc)}), 500


@app.route('/api/ict_atm/status')
def ict_atm_status():
    global streams
    sym = request.args.get('symbol') or get_config().get('broker', {}).get('symbol', 'XAUUSD')
    s = streams.get(sym)
    if not s:
        return jsonify({'status': 'no_stream'}), 404
    state = s.get_ict_atm_state()
    return jsonify({'status': 'success', 'symbol': sym, 'state': state})

@app.route('/api/close_all_trades', methods=['POST'])
def close_all_trades():
    """Kill switch: Close all open trades/positions"""
    try:
        mt5_conn = MT5Connector()
        if not mt5_conn.initialize():
            return jsonify({'status': 'error', 'message': 'MT5 not initialized'}), 500
        
        positions = mt5_conn.get_positions()
        if not positions:
            return jsonify({'status': 'success', 'message': 'No open positions', 'closed': 0})
        
        closed_count = 0
        failed_count = 0
        errors = []
        
        for pos in positions:
            try:
                autotrader = AutoTrader(pos.symbol)
                if autotrader.close_position(pos.ticket):
                    closed_count += 1
                else:
                    failed_count += 1
                    errors.append(f"Failed to close ticket {pos.ticket}")
            except Exception as e:
                failed_count += 1
                errors.append(f"Error closing ticket {pos.ticket}: {str(e)}")
        
        return jsonify({
            'status': 'success',
            'message': f'Closed {closed_count} positions',
            'closed': closed_count,
            'failed': failed_count,
            'errors': errors
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/close_profitable_trades', methods=['POST'])
def close_profitable_trades():
    """Kill switch: Close all open trades/positions with profits only (+)"""
    try:
        mt5_conn = MT5Connector()
        if not mt5_conn.initialize():
            return jsonify({'status': 'error', 'message': 'MT5 not initialized'}), 500
        
        positions = mt5_conn.get_positions()
        if not positions:
            return jsonify({'status': 'success', 'message': 'No open positions', 'closed': 0})
        
        # Filter only profitable positions (profit > 0)
        profitable_positions = [pos for pos in positions if float(getattr(pos, 'profit', 0)) > 0]
        
        if not profitable_positions:
            return jsonify({'status': 'success', 'message': 'No profitable positions', 'closed': 0})
        
        closed_count = 0
        failed_count = 0
        errors = []
        
        for pos in profitable_positions:
            try:
                autotrader = AutoTrader(pos.symbol)
                if autotrader.close_position(pos.ticket):
                    closed_count += 1
                else:
                    failed_count += 1
                    errors.append(f"Failed to close ticket {pos.ticket}")
            except Exception as e:
                failed_count += 1
                errors.append(f"Error closing ticket {pos.ticket}: {str(e)}")
        
        return jsonify({
            'status': 'success',
            'message': f'Closed {closed_count} profitable positions',
            'closed': closed_count,
            'failed': failed_count,
            'errors': errors
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/close_losing_trades', methods=['POST'])
def close_losing_trades():
    """Kill switch: Close all open trades/positions with losses only (-)"""
    try:
        mt5_conn = MT5Connector()
        if not mt5_conn.initialize():
            return jsonify({'status': 'error', 'message': 'MT5 not initialized'}), 500
        
        positions = mt5_conn.get_positions()
        if not positions:
            return jsonify({'status': 'success', 'message': 'No open positions', 'closed': 0})
        
        # Filter only losing positions (profit < 0)
        losing_positions = [pos for pos in positions if float(getattr(pos, 'profit', 0)) < 0]
        
        if not losing_positions:
            return jsonify({'status': 'success', 'message': 'No losing positions', 'closed': 0})
        
        closed_count = 0
        failed_count = 0
        errors = []
        
        for pos in losing_positions:
            try:
                autotrader = AutoTrader(pos.symbol)
                if autotrader.close_position(pos.ticket):
                    closed_count += 1
                else:
                    failed_count += 1
                    errors.append(f"Failed to close ticket {pos.ticket}")
            except Exception as e:
                failed_count += 1
                errors.append(f"Error closing ticket {pos.ticket}: {str(e)}")
        
        return jsonify({
            'status': 'success',
            'message': f'Closed {closed_count} losing positions',
            'closed': closed_count,
            'failed': failed_count,
            'errors': errors
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/total_profit', methods=['GET'])
def get_total_profit():
    """Get total unrealized profit from all open positions"""
    try:
        mt5_conn = MT5Connector()
        if not mt5_conn.initialize():
            return jsonify({'status': 'error', 'message': 'MT5 not initialized'}), 500
        
        positions = mt5_conn.get_positions()
        if not positions:
            return jsonify({
                'status': 'success',
                'total_profit': 0.0,
                'position_count': 0,
                'currency': 'USD'
            })
        
        acc_info = mt5_conn.get_account_info()
        currency = getattr(acc_info, 'currency', 'USD') if acc_info else 'USD'
        
        # Sum all unrealized profits
        total_profit = sum(float(getattr(pos, 'profit', 0)) for pos in positions)
        
        return jsonify({
            'status': 'success',
            'total_profit': round(total_profit, 2),
            'position_count': len(positions),
            'currency': currency
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/auto_take_profit', methods=['GET'])
def get_auto_take_profit():
    """Get auto-take-profit settings"""
    with auto_tp_lock:
        return jsonify({
            'status': 'success',
            'enabled': auto_take_profit['enabled'],
            'threshold': auto_take_profit['threshold']
        })

@app.route('/api/auto_take_profit', methods=['POST'])
def set_auto_take_profit():
    """Set auto-take-profit settings"""
    try:
        payload = request.get_json(silent=True) or {}
        enabled = bool(payload.get('enabled', False))
        threshold = float(payload.get('threshold', 30.0))
        
        if threshold < 0:
            return jsonify({'status': 'error', 'message': 'Threshold must be positive'}), 400
        
        with auto_tp_lock:
            auto_take_profit['enabled'] = enabled
            auto_take_profit['threshold'] = threshold
        
        return jsonify({
            'status': 'success',
            'enabled': enabled,
            'threshold': threshold,
            'message': f'Auto-take-profit {"enabled" if enabled else "disabled"} at {threshold} threshold'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

def monitor_auto_take_profit(stop_event=None):
    """Background thread that monitors total profit and closes all positions when threshold is reached"""
    stop_event = stop_event or threading.Event()
    while not stop_event.is_set():
        try:
            with auto_tp_lock:
                enabled = auto_take_profit['enabled']
                threshold = auto_take_profit['threshold']
            
            if enabled:
                try:
                    mt5_conn = MT5Connector()
                    if mt5_conn.initialize():
                        positions = mt5_conn.get_positions()
                        if positions:
                            total_profit = sum(float(getattr(pos, 'profit', 0)) for pos in positions)
                            
                            if total_profit >= threshold:
                                acc_info = mt5_conn.get_account_info()
                                currency = getattr(acc_info, 'currency', '') if acc_info else ''
                                
                                print(f"🎯 Auto-take-profit triggered! Total profit: {total_profit:.2f}{currency} >= {threshold:.2f}{currency}")
                                # Close all positions
                                closed_count = 0
                                failed_count = 0
                                for pos in positions:
                                    try:
                                        autotrader = AutoTrader(pos.symbol)
                                        if autotrader.close_position(pos.ticket):
                                            closed_count += 1
                                        else:
                                            failed_count += 1
                                    except Exception as e:
                                        failed_count += 1
                                        print(f"⚠️ Error closing position {pos.ticket}: {e}")
                                
                                print(f"✅ Auto-take-profit closed {closed_count} positions (failed: {failed_count})")
                                
                                # Disable auto-take-profit after triggering
                                with auto_tp_lock:
                                    auto_take_profit['enabled'] = False
                except Exception as e:
                    print(f"⚠️ Error in auto-take-profit monitor: {e}")
            
            # Check every 5 seconds
            stop_event.wait(5)
        except Exception as e:
            print(f"⚠️ Error in auto-take-profit monitor thread: {e}")
            stop_event.wait(5)

def ensure_professional_template():
    """Ensure the professional template is available"""
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    os.makedirs(templates_dir, exist_ok=True)
    
    template_path = os.path.join(templates_dir, 'dashboard.html')
    if os.path.exists(template_path):
        print("✅ Professional 'Get Rich FR Bot' template ready")
        return True
    else:
        print("❌ Professional template missing!")
        return False

if __name__ == '__main__':
    print("🚀 Starting Get Rich FR Bot - Professional Dashboard")
    print("💰 Created by Gift Ndlala")
    print("=" * 60)
    
    # Ensure template exists
    if not ensure_professional_template():
        print("❌ Cannot start - template missing")
        exit(1)
    
    # Initialize live stream with REAL market data
    print("📡 Initializing live data stream with REAL market data...")
    init_live_stream()
    
    # Start auto-take-profit monitoring thread
    print("💰 Starting auto-take-profit monitor...")
    start_background_monitors()
    print("✅ Auto-take-profit monitor started")
    
    # Start Flask app
    print("🌐 Starting professional dashboard...")
    print("📱 Open http://localhost:5000 to see the new professional interface")
    print("🎯 Live signals with REAL market data will update every 30 seconds")
    print("Press Ctrl+C to stop")
    configure_dashboard_logging()
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
    except KeyboardInterrupt:
        stop_background_monitors()
        stop_live_streams()
        print("\n👋 Get Rich FR Bot dashboard stopped")
