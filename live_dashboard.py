"""
Live Trading Signal Dashboard
Simple web-based UI for monitoring live XAUUSD trading signals
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
    """Initialize the live data stream"""
    global live_stream
    
    def signal_callback(signal: LiveSignal):
        global current_signal_data, signal_history
        current_signal_data = {
            'timestamp': signal.timestamp,
            'symbol': signal.symbol,
            'current_price': signal.current_price,
            'signal': signal.signal,
            'signal_type': signal.signal_type,
            'confidence': signal.confidence,
            'rsi': signal.rsi,
            'macd': signal.macd,
            'macd_signal': signal.macd_signal,
            'sma_20': signal.sma_20,
            'sma_50': signal.sma_50,
            'price_change': signal.price_change,
            'price_change_pct': signal.price_change_pct,
            
            # Risk Management Data
            'entry_price': signal.entry_price,
            'stop_loss': signal.stop_loss,
            'take_profit_1': signal.take_profit_1,
            'take_profit_2': signal.take_profit_2,
            'take_profit_3': signal.take_profit_3,
            'risk_reward_ratio': signal.risk_reward_ratio,
            'atr_value': signal.atr_value,
            'position_size_percent': signal.position_size_percent,
            'risk_amount_dollars': signal.risk_amount_dollars,
            'potential_profit_tp1': signal.potential_profit_tp1,
            'potential_profit_tp2': signal.potential_profit_tp2,
            'potential_profit_tp3': signal.potential_profit_tp3
        }
        
        # Add to history (keep last 10)
        signal_history.append(current_signal_data.copy())
        if len(signal_history) > 10:
            signal_history.pop(0)
        
        # Print signal update
        if signal.signal != 0:
            print(f"🎯 {signal.signal_type} SIGNAL: ${signal.current_price:.2f} (Confidence: {signal.confidence:.1f}%)")
    
    # Create and start live stream
    live_stream = LiveDataStream(symbol="GC=F", update_interval=30)
    live_stream.add_signal_callback(signal_callback)
    live_stream.start_streaming()
    print("✅ Live stream initialized and started")

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

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
        'data': signal_history,
        'count': len(signal_history)
    })

@app.route('/api/status')
def get_status():
    """API endpoint to get system status"""
    if live_stream:
        status = live_stream.get_status()
        status['dashboard_status'] = 'running'
    else:
        status = {'dashboard_status': 'initializing'}
    
    return jsonify(status)

# Create templates directory and HTML template
def create_dashboard_template():
    """Create the HTML template for the dashboard"""
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    os.makedirs(templates_dir, exist_ok=True)
    
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🥇 XAUUSD Live Trading Signals</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header .subtitle {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        
        .signal-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
        .price-section {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .current-price {
            font-size: 3rem;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .price-change {
            font-size: 1.5rem;
            margin-bottom: 5px;
        }
        
        .price-change.positive {
            color: #4CAF50;
        }
        
        .price-change.negative {
            color: #f44336;
        }
        
        .signal-section {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .signal-badge {
            display: inline-block;
            padding: 15px 30px;
            border-radius: 50px;
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 15px;
            min-width: 150px;
        }
        
        .signal-badge.BUY {
            background: #4CAF50;
            color: white;
            box-shadow: 0 0 20px rgba(76, 175, 80, 0.5);
        }
        
        .signal-badge.SELL {
            background: #f44336;
            color: white;
            box-shadow: 0 0 20px rgba(244, 67, 54, 0.5);
        }
        
        .signal-badge.HOLD {
            background: #FF9800;
            color: white;
            box-shadow: 0 0 20px rgba(255, 152, 0, 0.5);
        }
        
        .confidence {
            font-size: 1.2rem;
            margin-top: 10px;
        }
        
        .confidence-bar {
            width: 100%;
            height: 10px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 5px;
            margin-top: 10px;
            overflow: hidden;
        }
        
        .confidence-fill {
            height: 100%;
            background: linear-gradient(90deg, #FF6B6B, #FFE66D, #4ECDC4);
            transition: width 0.3s ease;
        }
        
        .indicators-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .indicator-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
        }
        
        .indicator-label {
            font-size: 0.9rem;
            opacity: 0.8;
            margin-bottom: 5px;
        }
        
        .indicator-value {
            font-size: 1.3rem;
            font-weight: bold;
        }
        
        .trade-details {
            background: rgba(255, 255, 255, 0.08);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid rgba(255, 215, 0, 0.3);
        }
        
        .trade-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .trade-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            border: 2px solid transparent;
            transition: all 0.3s ease;
        }
        
        .trade-card.entry {
            border-color: rgba(76, 175, 80, 0.5);
            background: rgba(76, 175, 80, 0.1);
        }
        
        .trade-card.stop-loss {
            border-color: rgba(244, 67, 54, 0.5);
            background: rgba(244, 67, 54, 0.1);
        }
        
        .trade-card.take-profit {
            border-color: rgba(255, 193, 7, 0.5);
            background: rgba(255, 193, 7, 0.1);
        }
        
        .trade-card.risk-reward {
            border-color: rgba(0, 188, 212, 0.5);
            background: rgba(0, 188, 212, 0.1);
        }
        
        .trade-label {
            font-size: 0.85rem;
            opacity: 0.9;
            margin-bottom: 8px;
            font-weight: 500;
        }
        
        .trade-value {
            font-size: 1.2rem;
            font-weight: bold;
            color: white;
        }
        
        .trade-sub {
            font-size: 0.8rem;
            margin-top: 5px;
            opacity: 0.8;
            color: #FFD700;
        }
        
        .position-size-section {
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .position-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
        }
        
        .position-card {
            background: rgba(0, 188, 212, 0.1);
            border: 1px solid rgba(0, 188, 212, 0.3);
            border-radius: 10px;
            padding: 15px;
            text-align: center;
        }
        
        .position-label {
            font-size: 0.85rem;
            opacity: 0.9;
            margin-bottom: 5px;
        }
        
        .position-value {
            font-size: 1.1rem;
            font-weight: bold;
            color: #00BCD4;
        }
        
        .status-bar {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
            text-align: center;
        }
        
        .last-update {
            font-size: 0.9rem;
            opacity: 0.8;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
        }
        
        .loading-spinner {
            width: 40px;
            height: 40px;
            border: 4px solid rgba(255, 255, 255, 0.3);
            border-top: 4px solid white;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .error {
            background: rgba(244, 67, 54, 0.2);
            border: 1px solid #f44336;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            margin: 20px 0;
        }
        
        @media (max-width: 600px) {
            .header h1 {
                font-size: 2rem;
            }
            
            .current-price {
                font-size: 2.5rem;
            }
            
            .signal-badge {
                font-size: 1.3rem;
                padding: 12px 25px;
            }
            
            .indicators-grid {
                grid-template-columns: 1fr 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🥇 XAUUSD Live Signals</h1>
            <div class="subtitle">Real-time Gold Trading Signals</div>
        </div>
        
        <div id="loading" class="loading">
            <div class="loading-spinner"></div>
            <div>Loading live data...</div>
        </div>
        
        <div id="error" class="error" style="display: none;">
            <h3>⚠️ Connection Error</h3>
            <p>Unable to load live signal data. Retrying...</p>
        </div>
        
        <div id="dashboard" style="display: none;">
            <div class="signal-card">
                <div class="price-section">
                    <div class="current-price" id="current-price">$0.00</div>
                    <div class="price-change" id="price-change">+$0.00 (+0.00%)</div>
                    <div class="last-update" id="timestamp">Last update: --</div>
                </div>
                
                <div class="signal-section">
                    <div class="signal-badge" id="signal-badge">HOLD</div>
                    <div class="confidence">
                        Confidence: <span id="confidence-text">0%</span>
                        <div class="confidence-bar">
                            <div class="confidence-fill" id="confidence-fill"></div>
                        </div>
                    </div>
                </div>
                
                <!-- Trade Details Section -->
                <div id="trade-details" class="trade-details" style="display: none;">
                    <h3 style="text-align: center; margin-bottom: 20px; color: #FFD700;">📋 Trade Details</h3>
                    
                    <div class="trade-grid">
                        <div class="trade-card entry">
                            <div class="trade-label">🎯 Entry Price</div>
                            <div class="trade-value" id="entry-price">--</div>
                        </div>
                        <div class="trade-card stop-loss">
                            <div class="trade-label">🛑 Stop Loss</div>
                            <div class="trade-value" id="stop-loss">--</div>
                        </div>
                        <div class="trade-card take-profit">
                            <div class="trade-label">🎯 Take Profit 1</div>
                            <div class="trade-value" id="take-profit-1">--</div>
                            <div class="trade-sub">Profit: <span id="profit-tp1">$--</span></div>
                        </div>
                        <div class="trade-card take-profit">
                            <div class="trade-label">🎯 Take Profit 2</div>
                            <div class="trade-value" id="take-profit-2">--</div>
                            <div class="trade-sub">Profit: <span id="profit-tp2">$--</span></div>
                        </div>
                        <div class="trade-card take-profit">
                            <div class="trade-label">🎯 Take Profit 3</div>
                            <div class="trade-value" id="take-profit-3">--</div>
                            <div class="trade-sub">Profit: <span id="profit-tp3">$--</span></div>
                        </div>
                        <div class="trade-card risk-reward">
                            <div class="trade-label">📊 Risk/Reward</div>
                            <div class="trade-value" id="risk-reward">1:--</div>
                        </div>
                    </div>
                    
                    <div class="position-size-section">
                        <h4 style="text-align: center; margin: 20px 0 10px; color: #00BCD4;">💰 Position Sizing</h4>
                        <div class="position-grid">
                            <div class="position-card">
                                <div class="position-label">Position Size</div>
                                <div class="position-value" id="position-size">--%</div>
                            </div>
                            <div class="position-card">
                                <div class="position-label">Risk Amount</div>
                                <div class="position-value" id="risk-amount">$--</div>
                            </div>
                            <div class="position-card">
                                <div class="position-label">ATR (14)</div>
                                <div class="position-value" id="atr-value">$--</div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="indicators-grid">
                    <div class="indicator-card">
                        <div class="indicator-label">RSI (14)</div>
                        <div class="indicator-value" id="rsi-value">--</div>
                    </div>
                    <div class="indicator-card">
                        <div class="indicator-label">MACD</div>
                        <div class="indicator-value" id="macd-value">--</div>
                    </div>
                    <div class="indicator-card">
                        <div class="indicator-label">SMA 20</div>
                        <div class="indicator-value" id="sma20-value">--</div>
                    </div>
                    <div class="indicator-card">
                        <div class="indicator-label">SMA 50</div>
                        <div class="indicator-value" id="sma50-value">--</div>
                    </div>
                </div>
                
                <div class="status-bar">
                    <div class="last-update">Next update in <span id="countdown">--</span> seconds</div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let updateInterval;
        let countdownInterval;
        let nextUpdateTime = 30;
        
        async function fetchCurrentSignal() {
            try {
                const response = await fetch('/api/current_signal');
                const result = await response.json();
                
                if (result.status === 'success') {
                    updateDashboard(result.data);
                    hideError();
                } else {
                    showLoading();
                }
            } catch (error) {
                showError();
                console.error('Error fetching signal:', error);
            }
        }
        
        function updateDashboard(data) {
            document.getElementById('loading').style.display = 'none';
            document.getElementById('dashboard').style.display = 'block';
            
            // Update price
            document.getElementById('current-price').textContent = `$${data.current_price.toFixed(2)}`;
            
            // Update price change
            const priceChangeElement = document.getElementById('price-change');
            const changeText = `${data.price_change >= 0 ? '+' : ''}$${data.price_change.toFixed(2)} (${data.price_change_pct >= 0 ? '+' : ''}${data.price_change_pct.toFixed(2)}%)`;
            priceChangeElement.textContent = changeText;
            priceChangeElement.className = `price-change ${data.price_change >= 0 ? 'positive' : 'negative'}`;
            
            // Update signal
            const signalBadge = document.getElementById('signal-badge');
            signalBadge.textContent = data.signal_type;
            signalBadge.className = `signal-badge ${data.signal_type}`;
            
            // Update confidence
            document.getElementById('confidence-text').textContent = `${data.confidence.toFixed(1)}%`;
            document.getElementById('confidence-fill').style.width = `${data.confidence}%`;
            
            // Update indicators
            document.getElementById('rsi-value').textContent = data.rsi.toFixed(1);
            document.getElementById('macd-value').textContent = data.macd.toFixed(2);
            document.getElementById('sma20-value').textContent = `$${data.sma_20.toFixed(2)}`;
            document.getElementById('sma50-value').textContent = `$${data.sma_50.toFixed(2)}`;
            
            // Update trade details (show only for BUY/SELL signals)
            const tradeDetails = document.getElementById('trade-details');
            if (data.signal_type !== 'HOLD') {
                tradeDetails.style.display = 'block';
                
                // Update trade prices
                document.getElementById('entry-price').textContent = `$${data.entry_price.toFixed(2)}`;
                document.getElementById('stop-loss').textContent = `$${data.stop_loss.toFixed(2)}`;
                document.getElementById('take-profit-1').textContent = `$${data.take_profit_1.toFixed(2)}`;
                document.getElementById('take-profit-2').textContent = `$${data.take_profit_2.toFixed(2)}`;
                document.getElementById('take-profit-3').textContent = `$${data.take_profit_3.toFixed(2)}`;
                document.getElementById('risk-reward').textContent = `1:${data.risk_reward_ratio.toFixed(1)}`;
                
                // Update potential profits
                document.getElementById('profit-tp1').textContent = `$${data.potential_profit_tp1.toFixed(0)}`;
                document.getElementById('profit-tp2').textContent = `$${data.potential_profit_tp2.toFixed(0)}`;
                document.getElementById('profit-tp3').textContent = `$${data.potential_profit_tp3.toFixed(0)}`;
                
                // Update position sizing
                document.getElementById('position-size').textContent = `${data.position_size_percent.toFixed(1)}%`;
                document.getElementById('risk-amount').textContent = `$${data.risk_amount_dollars.toFixed(0)}`;
                document.getElementById('atr-value').textContent = `$${data.atr_value.toFixed(2)}`;
            } else {
                tradeDetails.style.display = 'none';
            }
            
            // Update timestamp
            const timestamp = new Date(data.timestamp).toLocaleString();
            document.getElementById('timestamp').textContent = `Last update: ${timestamp}`;
            
            // Reset countdown
            nextUpdateTime = 30;
        }
        
        function showLoading() {
            document.getElementById('loading').style.display = 'block';
            document.getElementById('dashboard').style.display = 'none';
            document.getElementById('error').style.display = 'none';
        }
        
        function showError() {
            document.getElementById('loading').style.display = 'none';
            document.getElementById('dashboard').style.display = 'none';
            document.getElementById('error').style.display = 'block';
        }
        
        function hideError() {
            document.getElementById('error').style.display = 'none';
        }
        
        function updateCountdown() {
            if (nextUpdateTime > 0) {
                document.getElementById('countdown').textContent = nextUpdateTime;
                nextUpdateTime--;
            } else {
                document.getElementById('countdown').textContent = 'Updating...';
                nextUpdateTime = 30;
            }
        }
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            fetchCurrentSignal();
            
            // Set up intervals
            updateInterval = setInterval(fetchCurrentSignal, 30000); // 30 seconds
            countdownInterval = setInterval(updateCountdown, 1000); // 1 second
        });
        
        // Cleanup on page unload
        window.addEventListener('beforeunload', function() {
            if (updateInterval) clearInterval(updateInterval);
            if (countdownInterval) clearInterval(countdownInterval);
        });
    </script>
</body>
</html>'''
    
    with open(os.path.join(templates_dir, 'dashboard.html'), 'w') as f:
        f.write(html_content)
    print("✅ Dashboard template created")

if __name__ == '__main__':
    print("🚀 Starting XAUUSD Live Signal Dashboard")
    
    # Create template
    create_dashboard_template()
    
    # Initialize live stream
    init_live_stream()
    
    # Start Flask app
    print("🌐 Starting web dashboard...")
    print("📱 Open http://localhost:5000 in your browser")
    print("🎯 Live signals will update every 30 seconds")
    print("Press Ctrl+C to stop")
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
    except KeyboardInterrupt:
        if live_stream:
            live_stream.stop_streaming()
        print("\n👋 Dashboard stopped by user")