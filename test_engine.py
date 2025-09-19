#!/usr/bin/env python3
"""
Test script for XAUUSD Trading Signal Engine
"""

import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import TradingSignalEngine

def test_engine():
    """
    Test the trading signal engine with a small dataset
    """
    print("=" * 50)
    print("TESTING XAUUSD TRADING SIGNAL ENGINE")
    print("=" * 50)
    
    # Create the engine
    engine = TradingSignalEngine()
    
    # Test with a smaller dataset for faster testing
    print("\nTesting with 3 months of daily data...")
    
    try:
        # Run analysis with test parameters
        data = engine.run_analysis(
            period="3mo",      # 3 months of data
            interval="1d",     # Daily intervals
            save_chart=False   # Don't save chart for testing
        )
        
        if data is not None:
            print("\n✅ TEST PASSED!")
            print(f"Successfully processed {len(data)} data points")
            print(f"Date range: {data.index[0].date()} to {data.index[-1].date()}")
            
            # Show some basic statistics
            if 'signal' in data.columns:
                buy_signals = len(data[data['signal'] == 1])
                sell_signals = len(data[data['signal'] == -1])
                print(f"Generated {buy_signals} buy signals and {sell_signals} sell signals")
            
            # Show available columns
            print(f"\nAvailable indicators: {len([col for col in data.columns if 'SMA_' in col or 'RSI_' in col or 'MACD_' in col])}")
            
        else:
            print("\n❌ TEST FAILED!")
            print("No data returned from analysis")
            
    except Exception as e:
        print(f"\n❌ TEST FAILED!")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_engine()
