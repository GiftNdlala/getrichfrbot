"""
Technical Indicators Module for XAUUSD Trading Signal Engine
Implements various technical indicators for analysis
"""

import pandas as pd
import numpy as np
from typing import List, Union, Optional

class TechnicalIndicators:
    """
    Calculates various technical indicators for price analysis
    """
    
    def __init__(self):
        """Initialize the technical indicators calculator"""
        pass
    
    def add_sma(self, data: pd.DataFrame, periods: Union[int, List[int]] = 20) -> pd.DataFrame:
        """
        Add Simple Moving Average (SMA) indicators
        
        Args:
            data (pd.DataFrame): Price data
            periods (Union[int, List[int]]): Period(s) for SMA calculation
            
        Returns:
            pd.DataFrame: Data with SMA columns added
        """
        if isinstance(periods, int):
            periods = [periods]
        
        for period in periods:
            column_name = f'SMA_{period}'
            data[column_name] = data['Close'].rolling(window=period).mean()
        
        return data
    
    def add_ema(self, data: pd.DataFrame, periods: Union[int, List[int]] = 20) -> pd.DataFrame:
        """
        Add Exponential Moving Average (EMA) indicators
        
        Args:
            data (pd.DataFrame): Price data
            periods (Union[int, List[int]]): Period(s) for EMA calculation
            
        Returns:
            pd.DataFrame: Data with EMA columns added
        """
        if isinstance(periods, int):
            periods = [periods]
        
        for period in periods:
            column_name = f'EMA_{period}'
            data[column_name] = data['Close'].ewm(span=period).mean()
        
        return data
    
    def add_rsi(self, data: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """
        Add Relative Strength Index (RSI) indicator
        
        Args:
            data (pd.DataFrame): Price data
            period (int): Period for RSI calculation (default: 14)
            
        Returns:
            pd.DataFrame: Data with RSI column added
        """
        # Calculate price changes
        delta = data['Close'].diff()
        
        # Separate gains and losses
        gains = delta.where(delta > 0, 0)
        losses = -delta.where(delta < 0, 0)
        
        # Calculate average gains and losses
        avg_gains = gains.rolling(window=period).mean()
        avg_losses = losses.rolling(window=period).mean()
        
        # Calculate RS and RSI
        rs = avg_gains / avg_losses
        rsi = 100 - (100 / (1 + rs))
        
        data[f'RSI_{period}'] = rsi
        
        return data
    
    def add_macd(self, data: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
        """
        Add MACD (Moving Average Convergence Divergence) indicator
        
        Args:
            data (pd.DataFrame): Price data
            fast (int): Fast EMA period (default: 12)
            slow (int): Slow EMA period (default: 26)
            signal (int): Signal line period (default: 9)
            
        Returns:
            pd.DataFrame: Data with MACD columns added
        """
        # Calculate fast and slow EMAs
        ema_fast = data['Close'].ewm(span=fast).mean()
        ema_slow = data['Close'].ewm(span=slow).mean()
        
        # Calculate MACD line
        macd_line = ema_fast - ema_slow
        
        # Calculate signal line
        signal_line = macd_line.ewm(span=signal).mean()
        
        # Calculate histogram
        histogram = macd_line - signal_line
        
        # Add to dataframe
        data[f'MACD_{fast}_{slow}'] = macd_line
        data[f'MACD_Signal_{signal}'] = signal_line
        data[f'MACD_Histogram'] = histogram
        
        return data
    
    def add_bollinger_bands(self, data: pd.DataFrame, period: int = 20, std_dev: float = 2) -> pd.DataFrame:
        """
        Add Bollinger Bands indicator
        
        Args:
            data (pd.DataFrame): Price data
            period (int): Period for SMA calculation (default: 20)
            std_dev (float): Number of standard deviations (default: 2)
            
        Returns:
            pd.DataFrame: Data with Bollinger Bands columns added
        """
        # Calculate SMA
        sma = data['Close'].rolling(window=period).mean()
        
        # Calculate standard deviation
        std = data['Close'].rolling(window=period).std()
        
        # Calculate upper and lower bands
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        
        # Add to dataframe
        data[f'BB_Upper_{period}'] = upper_band
        data[f'BB_Middle_{period}'] = sma
        data[f'BB_Lower_{period}'] = lower_band
        data[f'BB_Width_{period}'] = upper_band - lower_band
        data[f'BB_Position_{period}'] = (data['Close'] - lower_band) / (upper_band - lower_band)
        
        return data
    
    def add_stochastic(self, data: pd.DataFrame, k_period: int = 14, d_period: int = 3) -> pd.DataFrame:
        """
        Add Stochastic Oscillator indicator
        
        Args:
            data (pd.DataFrame): Price data
            k_period (int): %K period (default: 14)
            d_period (int): %D period (default: 3)
            
        Returns:
            pd.DataFrame: Data with Stochastic columns added
        """
        # Calculate %K
        lowest_low = data['Low'].rolling(window=k_period).min()
        highest_high = data['High'].rolling(window=k_period).max()
        
        k_percent = 100 * ((data['Close'] - lowest_low) / (highest_high - lowest_low))
        
        # Calculate %D (SMA of %K)
        d_percent = k_percent.rolling(window=d_period).mean()
        
        # Add to dataframe
        data[f'Stoch_K_{k_period}'] = k_percent
        data[f'Stoch_D_{d_period}'] = d_percent
        
        return data
    
    def add_atr(self, data: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """
        Add Average True Range (ATR) indicator
        
        Args:
            data (pd.DataFrame): Price data
            period (int): Period for ATR calculation (default: 14)
            
        Returns:
            pd.DataFrame: Data with ATR column added
        """
        # Calculate True Range
        high_low = data['High'] - data['Low']
        high_close = np.abs(data['High'] - data['Close'].shift())
        low_close = np.abs(data['Low'] - data['Close'].shift())
        
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        
        # Calculate ATR
        atr = true_range.rolling(window=period).mean()
        
        data[f'ATR_{period}'] = atr
        
        return data
    
    def add_volume_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Add volume-based indicators
        
        Args:
            data (pd.DataFrame): Price data
            
        Returns:
            pd.DataFrame: Data with volume indicators added
        """
        # Volume SMA (ensure we operate on a Series even if 'Volume' is a 1-col DataFrame)
        vol_col = data.get('Volume')
        if isinstance(vol_col, pd.DataFrame):
            vol_series = vol_col.iloc[:, 0]
        else:
            vol_series = vol_col
        data['Volume_SMA_20'] = vol_series.rolling(window=20).mean()
        
        # Volume ratio (current volume / average volume)
        data['Volume_Ratio'] = vol_series / data['Volume_SMA_20']
        
        # On-Balance Volume (OBV)
        obv = (np.sign(data['Close'].diff()) * data['Volume']).fillna(0).cumsum()
        data['OBV'] = obv
        
        return data
    
    def add_price_patterns(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Add basic price pattern recognition
        
        Args:
            data (pd.DataFrame): Price data
            
        Returns:
            pd.DataFrame: Data with pattern columns added
        """
        # Higher highs and lower lows
        data['Higher_High'] = data['High'] > data['High'].shift(1)
        data['Lower_Low'] = data['Low'] < data['Low'].shift(1)
        
        # Price above/below moving averages
        if 'SMA_20' in data.columns:
            data['Above_SMA20'] = data['Close'] > data['SMA_20']
        if 'SMA_50' in data.columns:
            data['Above_SMA50'] = data['Close'] > data['SMA_50']
        
        # Gap up/down
        data['Gap_Up'] = data['Open'] > data['Close'].shift(1)
        data['Gap_Down'] = data['Open'] < data['Close'].shift(1)
        
        return data
    
    def calculate_all_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate all basic technical indicators
        
        Args:
            data (pd.DataFrame): Price data
            
        Returns:
            pd.DataFrame: Data with all indicators added
        """
        print("Calculating technical indicators...")
        # Defensive: ensure datetime index, sorted, and de-duplicated to avoid
        # reindex errors like "cannot reindex on an axis with duplicate labels"
        data = data.copy()
        try:
            if not isinstance(data.index, pd.DatetimeIndex):
                # Common upstream column names for time
                for tcol in ("time", "Time", "timestamp", "Timestamp"):
                    if tcol in data.columns:
                        data[tcol] = pd.to_datetime(data[tcol], errors='coerce', utc=True)
                        data = data.set_index(tcol)
                        break
            # Drop duplicate index stamps, keep last, and sort
            if getattr(data.index, "has_duplicates", False):
                data = data[~data.index.duplicated(keep='last')]
            data = data.sort_index()
        except Exception:
            # Continue with best-effort if sanitation fails
            pass
        
        # Moving averages
        data = self.add_sma(data, periods=[20, 50, 200])
        data = self.add_ema(data, periods=[12, 26])
        
        # Oscillators
        data = self.add_rsi(data, period=14)
        data = self.add_macd(data)
        data = self.add_stochastic(data)
        
        # Volatility indicators
        data = self.add_bollinger_bands(data)
        data = self.add_atr(data)
        
        # Volume indicators
        data = self.add_volume_indicators(data)
        
        # Price patterns
        data = self.add_price_patterns(data)
        
        print("All technical indicators calculated successfully!")
        return data
