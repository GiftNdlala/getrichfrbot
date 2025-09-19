"""
Live Data Streaming Module for XAUUSD Trading Signals
Fetches real-time price data and generates live trading signals
"""

import yfinance as yf
import pandas as pd
import numpy as np
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, Optional, Callable
import json
import os
from dataclasses import dataclass, asdict

from indicators import TechnicalIndicators
from signal_generator import SignalGenerator

@dataclass
class LiveSignal:
    """Data class for live trading signals"""
    timestamp: str
    symbol: str
    current_price: float
    signal: int  # -1: SELL, 0: HOLD, 1: BUY
    signal_type: str  # "BUY", "SELL", "HOLD"
    confidence: float
    rsi: float
    macd: float
    macd_signal: float
    sma_20: float
    sma_50: float
    price_change: float
    price_change_pct: float

class LiveDataStream:
    """
    Real-time data streaming and signal generation for XAUUSD
    """
    
    def __init__(self, symbol: str = "GC=F", update_interval: int = 30):
        """
        Initialize live data streaming
        
        Args:
            symbol (str): Yahoo Finance symbol for Gold (GC=F)
            update_interval (int): Update interval in seconds
        """
        self.symbol = symbol  # GC=F for Gold futures
        self.update_interval = update_interval
        self.indicators = TechnicalIndicators()
        self.signal_generator = SignalGenerator()
        
        # Data storage
        self.current_data = pd.DataFrame()
        self.current_signal = None
        self.last_update = None
        self.is_running = False
        
        # Callbacks for signal updates
        self.signal_callbacks = []
        
        # Historical data for indicators (need minimum 200 periods)
        self.historical_data = self._fetch_initial_data()
        
    def _fetch_initial_data(self) -> pd.DataFrame:
        """Fetch initial historical data for indicator calculations"""
        try:
            print("📊 Fetching initial historical data...")
            ticker = yf.Ticker(self.symbol)
            
            # Get 1 year of daily data for indicator calculations
            data = ticker.history(period="1y", interval="1d")
            
            if data.empty:
                print("⚠️ No data received, using mock data")
                return self._generate_mock_data()
            
            # Calculate all indicators on historical data
            data = self.indicators.calculate_all_indicators(data)
            
            print(f"✅ Loaded {len(data)} historical data points")
            return data
            
        except Exception as e:
            print(f"❌ Error fetching initial data: {e}")
            return self._generate_mock_data()
    
    def _generate_mock_data(self) -> pd.DataFrame:
        """Generate mock historical data if real data fails"""
        print("🎭 Generating mock historical data...")
        
        # Generate 365 days of mock data
        dates = pd.date_range(start=datetime.now() - timedelta(days=365), 
                            end=datetime.now(), 
                            freq='D')
        
        # Start around typical gold price
        base_price = 2640.0
        prices = []
        
        for i in range(len(dates)):
            # Add some realistic price movement
            change = np.random.normal(0, 20)  # Gold typically moves $10-30/day
            base_price += change
            prices.append(base_price)
        
        data = pd.DataFrame({
            'Open': prices,
            'High': [p + abs(np.random.normal(0, 15)) for p in prices],
            'Low': [p - abs(np.random.normal(0, 15)) for p in prices],
            'Close': prices,
            'Volume': np.random.randint(50000, 200000, len(dates))
        }, index=dates)
        
        # Calculate indicators
        data = self.indicators.calculate_all_indicators(data)
        return data
    
    def _fetch_current_quote(self) -> Optional[Dict]:
        """Fetch current real-time quote"""
        try:
            ticker = yf.Ticker(self.symbol)
            
            # Get current quote
            info = ticker.info
            history = ticker.history(period="2d", interval="1m")
            
            if history.empty:
                return None
            
            current_price = history['Close'].iloc[-1]
            prev_close = history['Close'].iloc[-2] if len(history) > 1 else current_price
            
            return {
                'price': float(current_price),
                'prev_close': float(prev_close),
                'timestamp': datetime.now(),
                'volume': float(history['Volume'].iloc[-1]) if not history['Volume'].empty else 0
            }
            
        except Exception as e:
            print(f"⚠️ Error fetching current quote: {e}")
            return self._generate_mock_quote()
    
    def _generate_mock_quote(self) -> Dict:
        """Generate mock current quote"""
        if not self.historical_data.empty:
            last_price = self.historical_data['Close'].iloc[-1]
            # Add small random movement
            current_price = last_price + np.random.normal(0, 5)
        else:
            current_price = 2640.0 + np.random.normal(0, 10)
        
        return {
            'price': current_price,
            'prev_close': current_price - np.random.normal(0, 3),
            'timestamp': datetime.now(),
            'volume': np.random.randint(1000, 5000)
        }
    
    def _update_historical_data(self, current_quote: Dict):
        """Update historical data with new quote"""
        new_row = pd.DataFrame({
            'Open': [current_quote['price']],
            'High': [current_quote['price']],
            'Low': [current_quote['price']],
            'Close': [current_quote['price']],
            'Volume': [current_quote['volume']]
        }, index=[current_quote['timestamp']])
        
        # Add to historical data
        self.historical_data = pd.concat([self.historical_data, new_row])
        
        # Keep only last 400 rows for efficiency
        if len(self.historical_data) > 400:
            self.historical_data = self.historical_data.tail(400)
        
        # Recalculate indicators
        self.historical_data = self.indicators.calculate_all_indicators(self.historical_data)
    
    def _generate_live_signal(self, current_quote: Dict) -> LiveSignal:
        """Generate live trading signal from current data"""
        
        # Get latest indicator values
        latest_data = self.historical_data.iloc[-1]
        
        # Generate signal using signal generator
        signals = self.signal_generator.generate_signals(self.historical_data.tail(50))
        current_signal = signals.iloc[-1] if not signals.empty else 0
        
        # Calculate confidence based on indicator alignment
        confidence = self._calculate_confidence(latest_data, current_signal)
        
        # Determine signal type
        if current_signal == 1:
            signal_type = "BUY"
        elif current_signal == -1:
            signal_type = "SELL"
        else:
            signal_type = "HOLD"
        
        # Calculate price changes
        price_change = current_quote['price'] - current_quote['prev_close']
        price_change_pct = (price_change / current_quote['prev_close']) * 100
        
        return LiveSignal(
            timestamp=current_quote['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
            symbol=self.symbol,
            current_price=current_quote['price'],
            signal=int(current_signal),
            signal_type=signal_type,
            confidence=confidence,
            rsi=float(latest_data.get('RSI_14', 50)),
            macd=float(latest_data.get('MACD_12_26', 0)),
            macd_signal=float(latest_data.get('MACD_Signal_9', 0)),
            sma_20=float(latest_data.get('SMA_20', current_quote['price'])),
            sma_50=float(latest_data.get('SMA_50', current_quote['price'])),
            price_change=price_change,
            price_change_pct=price_change_pct
        )
    
    def _calculate_confidence(self, latest_data: pd.Series, signal: int) -> float:
        """Calculate signal confidence based on indicator alignment"""
        confidence_score = 50.0  # Base confidence
        
        try:
            rsi = latest_data.get('RSI_14', 50)
            macd = latest_data.get('MACD_12_26', 0)
            macd_signal = latest_data.get('MACD_Signal_9', 0)
            price = latest_data.get('Close', 0)
            sma_20 = latest_data.get('SMA_20', price)
            sma_50 = latest_data.get('SMA_50', price)
            
            if signal == 1:  # BUY signal
                if rsi < 70 and rsi > 30:  # Not overbought
                    confidence_score += 10
                if macd > macd_signal:  # MACD bullish
                    confidence_score += 15
                if price > sma_20 > sma_50:  # Price above SMAs
                    confidence_score += 15
                if rsi > 50:  # RSI bullish
                    confidence_score += 10
                    
            elif signal == -1:  # SELL signal
                if rsi > 30 and rsi < 70:  # Not oversold
                    confidence_score += 10
                if macd < macd_signal:  # MACD bearish
                    confidence_score += 15
                if price < sma_20 < sma_50:  # Price below SMAs
                    confidence_score += 15
                if rsi < 50:  # RSI bearish
                    confidence_score += 10
            
            # Cap confidence at 95%
            confidence_score = min(confidence_score, 95.0)
            
        except Exception as e:
            print(f"⚠️ Error calculating confidence: {e}")
        
        return confidence_score
    
    def add_signal_callback(self, callback: Callable):
        """Add callback function to be called when new signals are generated"""
        self.signal_callbacks.append(callback)
    
    def _notify_callbacks(self, signal: LiveSignal):
        """Notify all registered callbacks of new signal"""
        for callback in self.signal_callbacks:
            try:
                callback(signal)
            except Exception as e:
                print(f"⚠️ Error in callback: {e}")
    
    def start_streaming(self):
        """Start the live data streaming"""
        self.is_running = True
        
        def stream_loop():
            print(f"🚀 Starting live data stream for {self.symbol}")
            print(f"⏱️ Update interval: {self.update_interval} seconds")
            
            while self.is_running:
                try:
                    # Fetch current quote
                    current_quote = self._fetch_current_quote()
                    
                    if current_quote:
                        # Update historical data
                        self._update_historical_data(current_quote)
                        
                        # Generate signal
                        live_signal = self._generate_live_signal(current_quote)
                        
                        # Store current signal
                        self.current_signal = live_signal
                        self.last_update = datetime.now()
                        
                        # Notify callbacks
                        self._notify_callbacks(live_signal)
                        
                        # Print update
                        print(f"🔄 {live_signal.timestamp} | {live_signal.symbol} | ${live_signal.current_price:.2f} | {live_signal.signal_type} ({live_signal.confidence:.1f}%)")
                        
                    else:
                        print("⚠️ Failed to fetch current quote")
                
                except Exception as e:
                    print(f"❌ Error in streaming loop: {e}")
                
                # Wait for next update
                time.sleep(self.update_interval)
        
        # Start streaming in background thread
        self.stream_thread = threading.Thread(target=stream_loop, daemon=True)
        self.stream_thread.start()
    
    def stop_streaming(self):
        """Stop the live data streaming"""
        self.is_running = False
        print("🛑 Live data streaming stopped")
    
    def get_current_signal(self) -> Optional[LiveSignal]:
        """Get the current live signal"""
        return self.current_signal
    
    def get_status(self) -> Dict:
        """Get current streaming status"""
        return {
            'is_running': self.is_running,
            'last_update': self.last_update.isoformat() if self.last_update else None,
            'symbol': self.symbol,
            'update_interval': self.update_interval,
            'current_signal': asdict(self.current_signal) if self.current_signal else None
        }

# Example usage
if __name__ == "__main__":
    def signal_callback(signal: LiveSignal):
        print(f"🎯 NEW SIGNAL: {signal.signal_type} | ${signal.current_price:.2f} | Confidence: {signal.confidence:.1f}%")
        if signal.signal != 0:
            print(f"📊 RSI: {signal.rsi:.1f} | MACD: {signal.macd:.2f} | Price Change: {signal.price_change_pct:+.2f}%")
    
    # Create and start live stream
    stream = LiveDataStream(symbol="GC=F", update_interval=30)
    stream.add_signal_callback(signal_callback)
    stream.start_streaming()
    
    try:
        # Keep running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stream.stop_streaming()
        print("👋 Live streaming stopped by user")