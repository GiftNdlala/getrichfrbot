"""
Get Rich FR Bot - Professional Live Trading Signal Dashboard
Clean implementation with real market data and professional branding
Created by Gift Ndlala
"""

from flask import Flask, render_template, jsonify, request
import threading
import time
import json
from datetime import datetime
import os
import sys

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.live_data_stream import LiveDataStream, LiveSignal

app = Flask(__name__)

# Global variables
live_stream = None
current_signal_data = None
signal_history = []

def init_live_stream():
    """Initialize the live data stream with real market data"""
    global live_stream
    
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
    live_stream = LiveDataStream(symbol="XAUUSD", update_interval=30)
    live_stream.add_signal_callback(signal_callback)
    live_stream.start_streaming()
    print("✅ Live stream with REAL market data initialized and started")

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
    """API endpoint to get current signal data"""
    if current_signal_data:
        return jsonify({
            'status': 'success',
            'data': current_signal_data,
            'last_update': datetime.now().isoformat()
        })
    else:
        return jsonify({
            'status': 'waiting',
            'message': 'Waiting for first signal...',
            'last_update': datetime.now().isoformat()
        })

@app.route('/api/signal_history')
def get_signal_history():
    """API endpoint to get signal history"""
    return jsonify({
        'status': 'success',
        'data': signal_history if isinstance(signal_history, list) else [],
        'count': len(signal_history) if isinstance(signal_history, list) else 0
    })

@app.route('/api/status')
def get_status():
    """API endpoint to get system status"""
    if live_stream:
        status = live_stream.get_status()
        status['dashboard_status'] = 'running'
        status['real_data'] = 'active'
    else:
        status = {'dashboard_status': 'initializing', 'real_data': 'loading'}
    
    return jsonify(status)

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