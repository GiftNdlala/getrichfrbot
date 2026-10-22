#!/usr/bin/env python3
"""
XAUUSD Live Trading Signals - Windows-Compatible Startup Script
Easy way to start the live signal dashboard on Windows
"""

import os
import sys
import subprocess
import time
from datetime import datetime

def check_requirements():
    """Check if all required packages are installed"""
    try:
        import flask
        import yfinance
        import pandas
        import numpy
        print("✓ All required packages found")
        return True
    except ImportError as e:
        print(f"✗ Missing required package: {e}")
        print("📦 Installing requirements...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print("✓ Requirements installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("✗ Failed to install requirements")
            return False

def start_live_dashboard():
    """Start the live trading signals dashboard"""
    print("="*60)
    print("XAUUSD LIVE TRADING SIGNALS DASHBOARD")
    print("="*60)
    print(f"📅 Starting at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check requirements
    if not check_requirements():
        print("✗ Cannot start dashboard due to missing requirements")
        return
    
    print("🚀 Starting live signal system...")
    print()
    print("📊 What you'll get:")
    print("   ✓ Real-time XAUUSD price updates (every 30 seconds)")
    print("   ✓ Live BUY/SELL/HOLD signals") 
    print("   ✓ Signal confidence percentage")
    print("   ✓ Key technical indicators (RSI, MACD, SMAs)")
    print("   ✓ Mobile-friendly web interface")
    print()
    print("🌐 Dashboard will be available at:")
    print("   📱 http://localhost:5000")
    print("   🖥️  http://127.0.0.1:5000")
    print()
    print("💡 Usage:")
    print("   1. Open the URL in your browser/phone")
    print("   2. Watch for BUY/SELL signals")
    print("   3. Trade manually on your demo account")
    print("   4. Press Ctrl+C here to stop")
    print()
    print("-"*60)
    
    try:
        # Set UTF-8 encoding for Windows
        if os.name == 'nt':  # Windows
            os.system('chcp 65001 >nul 2>&1')
        
        # Add current directory to Python path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        # Import and start dashboard
        from live_dashboard import app, init_live_stream, ensure_professional_template
        
        print("Setting up professional Get Rich FR Bot dashboard...")
        ensure_professional_template()
        
        print("Initializing live data stream with REAL market data...")
        init_live_stream()
        
        print("✓ Starting web server...")
        print("🎯 Dashboard ready! Open http://localhost:5000")
        print()
        print("*** LIVE SIGNALS ACTIVE - 3-TIER ALERT SYSTEM ***")
        print("🔴 HIGH ALERT: 40-50 pips target | Higher risk/reward")
        print("🟡 MEDIUM ALERT: 20-30 pips target | Balanced approach") 
        print("🟢 LOW ALERT: 10-15 pips target | Conservative/high success")
        print()
        
        # Start Flask app
        app.run(
            host=os.getenv("BOT_HOST", "127.0.0.1"),
            port=int(os.getenv("BOT_PORT", "5000")),
            debug=False,
            threaded=True,
        )
        
    except KeyboardInterrupt:
        print()
        print("🛑 Dashboard stopped by user")
    except Exception as e:
        print(f"✗ Error starting dashboard: {e}")
        print()
        print("🔍 Troubleshooting:")
        print("   1. Make sure you're in the project directory")
        print("   2. Check that all files are present")
        print("   3. Try: python -m pip install -r requirements.txt")
        print("   4. On Windows, try: chcp 65001 && python start_live_signals.py")
    
    print()
    print("👋 Thanks for using XAUUSD Live Signals!")

if __name__ == "__main__":
    start_live_dashboard()