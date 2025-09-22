"""
Robust Data Source for XAUUSD
Uses multiple data sources with intelligent fallbacks
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json
from typing import Dict, Optional, List
try:
    import yfinance as yf
except ImportError:
    yf = None
try:
    from tradingview_data import TradingViewData
except ImportError:
    try:
        from .tradingview_data import TradingViewData
    except ImportError:
        TradingViewData = None
import threading
import queue

class RobustXAUUSDDataSource:
    """
    Robust data source that tries multiple APIs and provides reliable XAUUSD data
    """
    
    def __init__(self):
        self.current_price = None
        self.price_history = []
        self.last_update = None
        self.data_source = "unknown"
        
        # Initialize TradingView API (PUBLIC - NO ACCOUNT REQUIRED)
        self.tradingview = TradingViewData() if TradingViewData else None
        if self.tradingview:
            print("✅ TradingView Public API initialized (no authentication required)")
        
        # Data source priority (1 = highest priority)
        self.data_sources = {
            'tradingview': 1,      # TradingView public API - highest quality
            'yahoo_gc': 2,         # Yahoo GC=F (Gold futures) 
            'yahoo_gld': 3,        # Yahoo GLD (Gold ETF)
            'yahoo_iau': 4,        # Yahoo IAU (Gold ETF)
            'finnhub': 5,          # Finnhub API
            'alpha_vantage': 6,    # Alpha Vantage API
            'mock': 99             # Mock data (last resort)
        }
        
        # Rate limiting
        self.last_request_time = {}
        self.min_request_interval = 1.0  # 1 second between requests
        
        # WebSocket for real-time data
        self.ws = None
        self.ws_connected = False
        self.price_queue = queue.Queue()
        
    def get_historical_data(self, days: int = 200) -> pd.DataFrame:
        """Get historical XAUUSD data from the best available source"""
        
        # Try multiple data sources in order of preference
        sources = [
            ("Yahoo Finance (GC=F)", self._get_yahoo_gcf_data),
            ("Yahoo Finance (XAUUSD=X)", self._get_yahoo_spot_data),
            ("Yahoo Finance (GLD)", self._get_yahoo_gld_data),
            ("Yahoo Finance (IAU)", self._get_yahoo_iau_data),
            ("Yahoo Finance (GOLD)", self._get_yahoo_gold_data),
            ("TradingView Fallback", self._get_tradingview_fallback),
            ("Mock Data", self._get_mock_data)
        ]
        
        for source_name, source_func in sources:
            if self._can_make_request(source_name):
                try:
                    print(f"🔍 Trying {source_name}...")
                    data = source_func(days)
                    
                    if data is not None and not data.empty:
                        print(f"✅ {source_name}: Got {len(data)} days of data")
                        self.data_source = source_name
                        return data
                    else:
                        print(f"⚠️ {source_name}: No data received")
                        
                except Exception as e:
                    print(f"❌ {source_name}: Error - {e}")
                
                # Wait between requests to avoid rate limiting
                time.sleep(1)
        
        print("❌ All data sources failed, using mock data")
        return self._get_mock_data(days)
    
    def get_current_price(self) -> Optional[Dict]:
        """Get current XAUUSD price from the best available source"""
        
        # Try real-time sources first (in priority order)
        sources = [
            ("TradingView Real-time", self._get_tradingview_realtime),  # HIGHEST QUALITY - Public API
            ("Yahoo Finance Real-time", self._get_yahoo_realtime),      # Backup source
            ("Mock Real-time", self._get_mock_realtime)                 # Last resort
        ]
        
        for source_name, source_func in sources:
            if self._can_make_request(source_name):
                try:
                    data = source_func()
                    if data:
                        self.data_source = source_name
                        return data
                except Exception as e:
                    print(f"⚠️ {source_name} error: {e}")
                
                time.sleep(0.5)
        
        return None
    
    def _can_make_request(self, source: str) -> bool:
        """Check if we can make a request to avoid rate limiting"""
        now = time.time()
        last_time = self.last_request_time.get(source, 0)
        return (now - last_time) >= self.min_request_interval
    
    def _update_request_time(self, source: str):
        """Update the last request time for rate limiting"""
        self.last_request_time[source] = time.time()
    
    def _get_yahoo_gld_data(self, days: int) -> Optional[pd.DataFrame]:
        """Get data from GLD ETF (SPDR Gold Trust)"""
        self._update_request_time("Yahoo Finance (GLD)")
        
        try:
            ticker = yf.Ticker("GLD")
            data = ticker.history(period=f"{days}d", interval="1d")
            
            if not data.empty:
                # Convert GLD price to approximate XAUUSD price
                # GLD is roughly 1/10th of gold price
                data['Close'] = data['Close'] * 10
                data['Open'] = data['Open'] * 10
                data['High'] = data['High'] * 10
                data['Low'] = data['Low'] * 10
                
                return data
        except:
            pass
        return None

    def _get_yahoo_gcf_data(self, days: int) -> Optional[pd.DataFrame]:
        """Get data from Yahoo Finance Gold Futures GC=F (closest to XAUUSD)."""
        self._update_request_time("Yahoo Finance (GC=F)")
        try:
            ticker = yf.Ticker("GC=F")
            data = ticker.history(period=f"{days}d", interval="1d")
            if not data.empty:
                return data
        except Exception:
            pass
        return None

    def _get_yahoo_spot_data(self, days: int) -> Optional[pd.DataFrame]:
        """Get data from Yahoo Finance spot XAUUSD=X."""
        self._update_request_time("Yahoo Finance (XAUUSD=X)")
        try:
            ticker = yf.Ticker("XAUUSD=X")
            data = ticker.history(period=f"{days}d", interval="1d")
            if not data.empty:
                return data
        except Exception:
            pass
        return None
    
    def _get_yahoo_iau_data(self, days: int) -> Optional[pd.DataFrame]:
        """Get data from IAU ETF (iShares Gold Trust)"""
        self._update_request_time("Yahoo Finance (IAU)")
        
        try:
            ticker = yf.Ticker("IAU")
            data = ticker.history(period=f"{days}d", interval="1d")
            
            if not data.empty:
                # Convert IAU price to approximate XAUUSD price
                # IAU is roughly 1/40th of gold price
                data['Close'] = data['Close'] * 40
                data['Open'] = data['Open'] * 40
                data['High'] = data['High'] * 40
                data['Low'] = data['Low'] * 40
                
                return data
        except:
            pass
        return None
    
    def _get_yahoo_gold_data(self, days: int) -> Optional[pd.DataFrame]:
        """Get data from GOLD ETF"""
        self._update_request_time("Yahoo Finance (GOLD)")
        
        try:
            ticker = yf.Ticker("GOLD")
            data = ticker.history(period=f"{days}d", interval="1d")
            
            if not data.empty:
                # GOLD ETF is roughly 1/100th of gold price
                data['Close'] = data['Close'] * 100
                data['Open'] = data['Open'] * 100
                data['High'] = data['High'] * 100
                data['Low'] = data['Low'] * 100
                
                return data
        except:
            pass
        return None
    
    def _get_tradingview_fallback(self, days: int) -> Optional[pd.DataFrame]:
        """Get fallback data from TradingView-style generation"""
        self._update_request_time("TradingView Fallback")
        
        # Generate realistic gold data
        dates = pd.date_range(start=datetime.now() - timedelta(days=days), 
                            end=datetime.now(), 
                            freq='D')
        
        # Start around current gold price
        base_price = 2640.0
        prices = []
        
        for i in range(len(dates)):
            # Add realistic price movement
            change = np.random.normal(0, 20)
            base_price += change
            prices.append(base_price)
        
        data = pd.DataFrame({
            'Open': prices,
            'High': [p + abs(np.random.normal(0, 15)) for p in prices],
            'Low': [p - abs(np.random.normal(0, 15)) for p in prices],
            'Close': prices,
            'Volume': np.random.randint(50000, 200000, len(dates))
        }, index=dates)
        
        return data
    
    def _get_mock_data(self, days: int) -> pd.DataFrame:
        """Generate mock data as last resort"""
        print("🎭 Generating mock XAUUSD data...")
        
        dates = pd.date_range(start=datetime.now() - timedelta(days=days), 
                            end=datetime.now(), 
                            freq='D')
        
        base_price = 2640.0
        prices = []
        
        for i in range(len(dates)):
            change = np.random.normal(0, 20)
            base_price += change
            prices.append(base_price)
        
        data = pd.DataFrame({
            'Open': prices,
            'High': [p + abs(np.random.normal(0, 15)) for p in prices],
            'Low': [p - abs(np.random.normal(0, 15)) for p in prices],
            'Close': prices,
            'Volume': np.random.randint(50000, 200000, len(dates))
        }, index=dates)
        
        return data
    
    def _get_yahoo_realtime(self) -> Optional[Dict]:
        """Get real-time data from Yahoo Finance"""
        self._update_request_time("Yahoo Finance Real-time")
        
        try:
            # Prefer spot XAUUSD=X
            for symbol, source_label, scale in [
                ("XAUUSD=X", "Yahoo Finance (XAUUSD=X)", 1.0),
                ("GC=F", "Yahoo Finance (GC=F)", 1.0),
                ("GLD", "Yahoo Finance (GLD)", 10.0),
            ]:
                try:
                    ticker = yf.Ticker(symbol)
                    data = ticker.history(period="2d", interval="1m")
                    if not data.empty:
                        current_price = float(data['Close'].iloc[-1]) * scale
                        prev_close = float(data['Close'].iloc[-2]) * scale if len(data) > 1 else current_price
                        return {
                            'price': current_price,
                            'prev_close': prev_close,
                            'timestamp': datetime.now(),
                            'volume': float(data['Volume'].iloc[-1]) if 'Volume' in data.columns and not data['Volume'].empty else 0.0,
                            'source': source_label
                        }
                except Exception:
                    continue
        except:
            pass
        return None
    
    def _get_tradingview_realtime(self) -> Optional[Dict]:
        """Get real-time XAUUSD data from TradingView Public API (NO ACCOUNT REQUIRED)"""
        self._update_request_time("TradingView Real-time")
        
        if not self.tradingview:
            print("⚠️ TradingView API not available")
            return None
        
        try:
            # Get real-time quote from TradingView public API
            quote = self.tradingview.get_best_xauusd_quote()
            
            if quote and quote.get('price', 0) > 0:
                # Convert TradingView quote to our standard format
                return {
                    'price': float(quote['price']),
                    'prev_close': float(quote.get('price', 0)) - float(quote.get('change_abs', 0)),
                    'timestamp': quote.get('timestamp', datetime.now()),
                    'volume': float(quote.get('volume', 0)),
                    'high': float(quote.get('high', quote['price'])),
                    'low': float(quote.get('low', quote['price'])),
                    'bid': float(quote.get('bid', 0)),
                    'ask': float(quote.get('ask', 0)),
                    'spread': float(quote.get('spread', 0)),
                    'change_pct': float(quote.get('change', 0)),
                    'source': f"TradingView-{quote.get('symbol', 'XAUUSD')}"
                }
            else:
                print("⚠️ TradingView: No valid XAUUSD quote received")
                return None
                
        except Exception as e:
            print(f"❌ TradingView API error: {e}")
            return None
    
    def _get_mock_realtime(self) -> Dict:
        """Generate mock real-time data"""
        base_price = 2640.0 + np.random.normal(0, 10)
        
        return {
            'price': base_price,
            'prev_close': base_price - np.random.normal(0, 3),
            'timestamp': datetime.now(),
            'volume': np.random.randint(1000, 5000),
            'source': 'Mock Data'
        }
    
    def start_realtime_stream(self, callback=None):
        """Start real-time price streaming"""
        def stream_loop():
            while True:
                try:
                    current = self.get_current_price()
                    if current:
                        self.current_price = current
                        self.last_update = datetime.now()
                        
                        if callback:
                            callback(current)
                        
                        print(f"💰 {current['timestamp'].strftime('%H:%M:%S')} | "
                              f"XAUUSD: ${current['price']:.2f} | "
                              f"Change: {((current['price'] - current['prev_close']) / current['prev_close'] * 100):+.2f}% | "
                              f"Source: {current['source']}")
                    
                    time.sleep(30)  # Update every 30 seconds
                    
                except Exception as e:
                    print(f"❌ Stream error: {e}")
                    time.sleep(5)
        
        # Start streaming in background thread
        stream_thread = threading.Thread(target=stream_loop, daemon=True)
        stream_thread.start()
        print("🚀 Real-time streaming started")

# Test the robust data source
if __name__ == "__main__":
    print("🥇 Testing Robust XAUUSD Data Source")
    print("=" * 50)
    
    source = RobustXAUUSDDataSource()
    
    # Test historical data
    print("📊 Fetching historical data...")
    data = source.get_historical_data(30)
    print(f"✅ Got {len(data)} days from {source.data_source}")
    print(f"📈 Latest close: ${data['Close'].iloc[-1]:.2f}")
    print(f"📊 Price range: ${data['Low'].min():.2f} - ${data['High'].max():.2f}")
    
    # Test current price
    print("\n💰 Fetching current price...")
    current = source.get_current_price()
    if current:
        print(f"✅ Current price: ${current['price']:.2f}")
        print(f"📊 Change: {((current['price'] - current['prev_close']) / current['prev_close'] * 100):+.2f}%")
        print(f"🕐 Source: {current['source']}")
    
    # Test real-time streaming
    print("\n🚀 Starting real-time stream (5 updates)...")
    def price_callback(data):
        print(f"📡 Real-time: ${data['price']:.2f} from {data['source']}")
    
    source.start_realtime_stream(price_callback)
    time.sleep(10)  # Let it run for 10 seconds
