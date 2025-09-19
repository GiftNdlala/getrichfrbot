"""
Signal Generator Module for XAUUSD Trading Signal Engine
Generates trading signals based on technical indicators
"""

import pandas as pd
import numpy as np
from typing import Optional, Dict, Any

class SignalGenerator:
    """
    Generates trading signals based on technical indicators
    """
    
    def __init__(self):
        """Initialize the signal generator"""
        self.signal_columns = []
    
    def sma_crossover_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate signals based on SMA crossovers
        
        Args:
            data (pd.DataFrame): Price data with SMA indicators
            
        Returns:
            pd.DataFrame: Data with SMA crossover signals
        """
        # Check if we have the required SMA columns
        sma_columns = [col for col in data.columns if col.startswith('SMA_')]
        
        if len(sma_columns) < 2:
            print("Warning: Need at least 2 SMA periods for crossover signals")
            return data
        
        # Sort SMA columns by period
        sma_columns.sort(key=lambda x: int(x.split('_')[1]))
        
        # Generate signals for different SMA combinations
        for i in range(len(sma_columns) - 1):
            fast_sma = sma_columns[i]
            slow_sma = sma_columns[i + 1]
            
            # Create signal column name
            signal_col = f'SMA_Signal_{fast_sma.split("_")[1]}_{slow_sma.split("_")[1]}'
            
            # Generate crossover signals
            # 1 = Buy signal (fast SMA crosses above slow SMA)
            # -1 = Sell signal (fast SMA crosses below slow SMA)
            # 0 = No signal
            
            data[signal_col] = 0
            
            # Buy signal: fast SMA crosses above slow SMA
            buy_condition = (data[fast_sma] > data[slow_sma]) & (data[fast_sma].shift(1) <= data[slow_sma].shift(1))
            data.loc[buy_condition, signal_col] = 1
            
            # Sell signal: fast SMA crosses below slow SMA
            sell_condition = (data[fast_sma] < data[slow_sma]) & (data[fast_sma].shift(1) >= data[slow_sma].shift(1))
            data.loc[sell_condition, signal_col] = -1
            
            self.signal_columns.append(signal_col)
        
        return data
    
    def rsi_signals(self, data: pd.DataFrame, period: int = 14, 
                    oversold: float = 30, overbought: float = 70) -> pd.DataFrame:
        """
        Generate signals based on RSI levels
        
        Args:
            data (pd.DataFrame): Price data with RSI indicator
            period (int): RSI period used
            oversold (float): Oversold threshold (default: 30)
            overbought (float): Overbought threshold (default: 70)
            
        Returns:
            pd.DataFrame: Data with RSI signals
        """
        rsi_col = f'RSI_{period}'
        
        if rsi_col not in data.columns:
            print(f"Warning: RSI_{period} not found in data")
            return data
        
        signal_col = f'RSI_Signal_{period}'
        data[signal_col] = 0
        
        # Buy signal: RSI crosses above oversold level
        buy_condition = (data[rsi_col] > oversold) & (data[rsi_col].shift(1) <= oversold)
        data.loc[buy_condition, signal_col] = 1
        
        # Sell signal: RSI crosses below overbought level
        sell_condition = (data[rsi_col] < overbought) & (data[rsi_col].shift(1) >= overbought)
        data.loc[sell_condition, signal_col] = -1
        
        self.signal_columns.append(signal_col)
        
        return data
    
    def macd_signals(self, data: pd.DataFrame, fast: int = 12, slow: int = 26) -> pd.DataFrame:
        """
        Generate signals based on MACD crossovers
        
        Args:
            data (pd.DataFrame): Price data with MACD indicators
            fast (int): Fast EMA period
            slow (int): Slow EMA period
            
        Returns:
            pd.DataFrame: Data with MACD signals
        """
        macd_col = f'MACD_{fast}_{slow}'
        signal_col = f'MACD_Signal_{signal}'
        
        if macd_col not in data.columns or signal_col not in data.columns:
            print(f"Warning: MACD indicators not found in data")
            print(f"Available MACD columns: {[col for col in data.columns if 'MACD' in col]}")
            return data
        
        # Create MACD signal column
        data[f'{signal_col}_Signals'] = 0
        
        # Buy signal: MACD line crosses above signal line
        buy_condition = (data[macd_col] > data[signal_col]) & (data[macd_col].shift(1) <= data[signal_col].shift(1))
        data.loc[buy_condition, f'{signal_col}_Signals'] = 1
        
        # Sell signal: MACD line crosses below signal line
        sell_condition = (data[macd_col] < data[signal_col]) & (data[macd_col].shift(1) >= data[signal_col].shift(1))
        data.loc[sell_condition, f'{signal_col}_Signals'] = -1
        
        self.signal_columns.append(f'{signal_col}_Signals')
        
        return data
    
    def bollinger_bands_signals(self, data: pd.DataFrame, period: int = 20) -> pd.DataFrame:
        """
        Generate signals based on Bollinger Bands
        
        Args:
            data (pd.DataFrame): Price data with Bollinger Bands
            period (int): Bollinger Bands period
            
        Returns:
            pd.DataFrame: Data with Bollinger Bands signals
        """
        upper_col = f'BB_Upper_{period}'
        lower_col = f'BB_Lower_{period}'
        
        if upper_col not in data.columns or lower_col not in data.columns:
            print(f"Warning: Bollinger Bands not found in data")
            return data
        
        signal_col = f'BB_Signal_{period}'
        data[signal_col] = 0
        
        # Buy signal: Price touches or crosses below lower band
        buy_condition = (data['Close'] <= data[lower_col]) & (data['Close'].shift(1) > data[lower_col].shift(1))
        data.loc[buy_condition, signal_col] = 1
        
        # Sell signal: Price touches or crosses above upper band
        sell_condition = (data['Close'] >= data[upper_col]) & (data['Close'].shift(1) < data[upper_col].shift(1))
        data.loc[sell_condition, signal_col] = -1
        
        self.signal_columns.append(signal_col)
        
        return data
    
    def volume_confirmation_signals(self, data: pd.DataFrame, volume_threshold: float = 1.5) -> pd.DataFrame:
        """
        Generate volume confirmation signals
        
        Args:
            data (pd.DataFrame): Price data with volume indicators
            volume_threshold (float): Volume ratio threshold for confirmation
            
        Returns:
            pd.DataFrame: Data with volume confirmation signals
        """
        if 'Volume_Ratio' not in data.columns:
            print("Warning: Volume_Ratio not found in data")
            return data
        
        signal_col = 'Volume_Confirmation'
        data[signal_col] = 0
        
        # Volume confirmation: high volume supports the price movement
        high_volume = data['Volume_Ratio'] > volume_threshold
        
        # Combine with price movement
        price_up = data['Close'] > data['Close'].shift(1)
        price_down = data['Close'] < data['Close'].shift(1)
        
        # Buy confirmation: price up with high volume
        buy_condition = price_up & high_volume
        data.loc[buy_condition, signal_col] = 1
        
        # Sell confirmation: price down with high volume
        sell_condition = price_down & high_volume
        data.loc[sell_condition, signal_col] = -1
        
        self.signal_columns.append(signal_col)
        
        return data
    
    def trend_following_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trend following signals based on multiple indicators
        
        Args:
            data (pd.DataFrame): Price data with indicators
            
        Returns:
            pd.DataFrame: Data with trend following signals
        """
        signal_col = 'Trend_Following_Signal'
        data[signal_col] = 0
        
        # Check if we have the required indicators
        required_indicators = ['SMA_20', 'SMA_50', 'RSI_14']
        missing_indicators = [ind for ind in required_indicators if ind not in data.columns]
        
        if missing_indicators:
            print(f"Warning: Missing indicators for trend following: {missing_indicators}")
            return data
        
        # Trend following conditions
        uptrend = (data['Close'] > data['SMA_20']) & (data['SMA_20'] > data['SMA_50']) & (data['RSI_14'] > 50)
        downtrend = (data['Close'] < data['SMA_20']) & (data['SMA_20'] < data['SMA_50']) & (data['RSI_14'] < 50)
        
        # Generate signals
        data.loc[uptrend, signal_col] = 1
        data.loc[downtrend, signal_col] = -1
        
        self.signal_columns.append(signal_col)
        
        return data
    
    def combine_signals(self, data: pd.DataFrame, method: str = 'majority') -> pd.DataFrame:
        """
        Combine multiple signals into a final signal
        
        Args:
            data (pd.DataFrame): Price data with multiple signals
            method (str): Method to combine signals ('majority', 'weighted', 'consensus')
            
        Returns:
            pd.DataFrame: Data with combined signal
        """
        if not self.signal_columns:
            print("Warning: No signal columns found")
            return data
        
        # Filter out NaN values and get only signal columns
        signal_data = data[self.signal_columns].fillna(0)
        
        if method == 'majority':
            # Simple majority vote
            combined_signal = signal_data.sum(axis=1)
            data['signal'] = np.where(combined_signal > 0, 1, 
                                    np.where(combined_signal < 0, -1, 0))
        
        elif method == 'weighted':
            # Weighted average (you can adjust weights)
            weights = np.ones(len(self.signal_columns))
            weighted_sum = (signal_data * weights).sum(axis=1)
            data['signal'] = np.where(weighted_sum > 0.5, 1,
                                    np.where(weighted_sum < -0.5, -1, 0))
        
        elif method == 'consensus':
            # All signals must agree
            positive_signals = (signal_data > 0).sum(axis=1)
            negative_signals = (signal_data < 0).sum(axis=1)
            total_signals = len(self.signal_columns)
            
            data['signal'] = np.where(positive_signals == total_signals, 1,
                                    np.where(negative_signals == total_signals, -1, 0))
        
        else:
            print(f"Unknown method: {method}. Using majority vote.")
            combined_signal = signal_data.sum(axis=1)
            data['signal'] = np.where(combined_signal > 0, 1,
                                    np.where(combined_signal < 0, -1, 0))
        
        # Add signal strength (number of confirming signals)
        data['signal_strength'] = signal_data.abs().sum(axis=1)
        
        return data
    
    def generate_all_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate all types of signals
        
        Args:
            data (pd.DataFrame): Price data with indicators
            
        Returns:
            pd.DataFrame: Data with all signals
        """
        print("Generating trading signals...")
        
        # Generate different types of signals
        data = self.sma_crossover_signals(data)
        data = self.rsi_signals(data)
        data = self.macd_signals(data)
        data = self.bollinger_bands_signals(data)
        data = self.volume_confirmation_signals(data)
        data = self.trend_following_signals(data)
        
        # Combine all signals
        data = self.combine_signals(data, method='majority')
        
        print(f"Generated {len(self.signal_columns)} signal types")
        print(f"Signal columns: {self.signal_columns}")
        
        return data
    
    def get_signal_statistics(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Get statistics about the generated signals
        
        Args:
            data (pd.DataFrame): Price data with signals
            
        Returns:
            Dict[str, Any]: Signal statistics
        """
        if 'signal' not in data.columns:
            return {}
        
        stats = {
            'total_signals': len(data[data['signal'] != 0]),
            'buy_signals': len(data[data['signal'] == 1]),
            'sell_signals': len(data[data['signal'] == -1]),
            'signal_ratio': len(data[data['signal'] != 0]) / len(data),
            'buy_ratio': len(data[data['signal'] == 1]) / len(data[data['signal'] != 0]) if len(data[data['signal'] != 0]) > 0 else 0,
            'sell_ratio': len(data[data['signal'] == -1]) / len(data[data['signal'] != 0]) if len(data[data['signal'] != 0]) > 0 else 0
        }
        
        return stats
