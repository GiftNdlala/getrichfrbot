#!/usr/bin/env python3
"""
Test different symbols to find the best one for XAUUSD data
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def test_symbol(symbol, name):
    """Test a symbol and return results"""
    print(f"\n🔍 Testing {name} ({symbol})...")
    
    try:
        ticker = yf.Ticker(symbol)
        
        # Test 1: Get basic info
        info = ticker.info
        print(f"   📊 Symbol: {info.get('symbol', 'N/A')}")
        print(f"   📈 Name: {info.get('longName', 'N/A')}")
        print(f"   💰 Current Price: {info.get('currentPrice', 'N/A')}")
        print(f"   📅 Last Update: {info.get('regularMarketTime', 'N/A')}")
        
        # Test 2: Get historical data
        data = ticker.history(period="5d", interval="1d")
        if not data.empty:
            print(f"   ✅ Historical data: {len(data)} days")
            print(f"   📊 Latest close: ${data['Close'].iloc[-1]:.2f}")
            print(f"   📈 Price change: {((data['Close'].iloc[-1] - data['Close'].iloc[-2]) / data['Close'].iloc[-2] * 100):+.2f}%")
        else:
            print(f"   ❌ No historical data")
            
        # Test 3: Get real-time quote
        quote = ticker.history(period="1d", interval="1m")
        if not quote.empty:
            print(f"   ✅ Real-time data: {len(quote)} minutes")
            print(f"   💰 Latest price: ${quote['Close'].iloc[-1]:.2f}")
        else:
            print(f"   ❌ No real-time data")
            
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    print("🥇 Testing XAUUSD Symbol Options")
    print("=" * 50)
    
    # Test different symbols
    symbols_to_test = [
        ("GC=F", "Gold Futures (COMEX)"),
        ("XAUUSD=X", "XAUUSD Spot"),
        ("GOLD", "Gold ETF"),
        ("GLD", "SPDR Gold Trust"),
        ("IAU", "iShares Gold Trust"),
        ("OANDA:XAUUSD", "OANDA XAUUSD"),
        ("FX:XAUUSD", "FX XAUUSD"),
        ("XAU-USD", "XAU-USD"),
        ("GOLD=X", "Gold Spot"),
        ("XAUUSD", "XAUUSD Direct")
    ]
    
    working_symbols = []
    
    for symbol, name in symbols_to_test:
        if test_symbol(symbol, name):
            working_symbols.append((symbol, name))
    
    print(f"\n🎯 RESULTS SUMMARY")
    print("=" * 50)
    
    if working_symbols:
        print(f"✅ Found {len(working_symbols)} working symbols:")
        for symbol, name in working_symbols:
            print(f"   • {symbol} - {name}")
        
        print(f"\n💡 RECOMMENDATION:")
        print(f"   Use: {working_symbols[0][0]} - {working_symbols[0][1]}")
        print(f"   This should give you the most reliable XAUUSD data!")
    else:
        print("❌ No working symbols found")
        print("💡 Consider using TradingView API or other data sources")

if __name__ == "__main__":
    main()
