"""
Get Rich FR Bot - Professional Live Trading Signal Dashboard
Clean implementation with real market data and professional branding
Created by Gift Ndlala
"""

from flask import Flask, render_template, jsonify, request
from dataclasses import asdict
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

app = Flask(__name__)

# Global variables
streams = {}
current_signal_data = None
signal_history = []
persistence = PersistenceManager()

def init_live_stream():
    """Initialize live data streams for configured symbols"""
    global streams
    
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
        
        # Print signal update with alert categorization
        if signal.signal != 0:
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
    streams[symbol] = gold_stream

    # Start US30m secondary stream
    try:
        us_symbol = os.getenv('US30_SYMBOL', 'US30m')
        us_stream = LiveDataStream(symbol=us_symbol, update_interval=30)
        us_stream.add_signal_callback(signal_callback)
        us_stream.start_streaming()
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
    s = streams.get(sym)
    if s:
        s.is_running = False
        return jsonify({'status': 'paused', 'symbol': sym})
    return jsonify({'status': 'no_stream'})

@app.route('/api/resume', methods=['POST'])
def resume_trading():
    global streams
    sym = request.args.get('symbol') or get_config().get('broker', {}).get('symbol', 'XAUUSD')
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
    enabled = bool(request.json.get('enabled', False))
    sym = request.args.get('symbol') or get_config().get('broker', {}).get('symbol', 'XAUUSD')
    s = streams.get(sym)
    if s:
        s.set_farmer_enabled(enabled)
        return jsonify({'status': 'success', 'symbol': sym, 'farmer_enabled': s.farmer_enabled})
    return jsonify({'status': 'no_stream'})

@app.route('/api/engine_toggle', methods=['POST'])
def engine_toggle():
    global streams
    sym = request.args.get('symbol') or get_config().get('broker', {}).get('symbol', 'XAUUSD')
    s = streams.get(sym)
    if not s:
        return jsonify({'status': 'no_stream'})
    level = request.json.get('level')
    enabled = bool(request.json.get('enabled', True))
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
    enabled = bool(request.json.get('enabled', False))
    sym = request.args.get('symbol') or get_config().get('broker', {}).get('symbol', 'XAUUSD')
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
    sym = request.args.get('symbol') or get_config().get('broker', {}).get('symbol', 'XAUUSD')
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
    
    # Start Flask app
    print("🌐 Starting professional dashboard...")
    print("📱 Open http://localhost:5000 to see the new professional interface")
    print("🎯 Live signals with REAL market data will update every 30 seconds")
    print("Press Ctrl+C to stop")
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
    except KeyboardInterrupt:
        if live_stream:
            live_stream.stop_streaming()
        print("\n👋 Get Rich FR Bot dashboard stopped")