"""
Mock Data Generator for XAUUSD Trading Signal Engine
Creates synthetic price data for testing when real data is unavailable
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional

class MockDataGenerator:
    """
    Generates synthetic price data for testing purposes
    """
    
    def __init__(self):
        """Initialize the mock data generator"""
        self.base_price = 2000.0  # Starting gold price
        self.volatility = 0.02    # Daily volatility
    
    def generate_price_data(self, days: int = 90, start_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Generate synthetic OHLCV price data
        
        Args:
            days (int): Number of days to generate
            start_date (datetime, optional): Start date for data
            
        Returns:
            pd.DataFrame: Synthetic price data
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=days)
        
        # Generate date range
        dates = pd.date_range(start=start_date, periods=days, freq='D')
        
        # Generate random walk for price
        np.random.seed(42)  # For reproducible results
        returns = np.random.normal(0, self.volatility, days)
        returns[0] = 0  # First day no change
        
        # Calculate cumulative price
        prices = [self.base_price]
        for ret in returns[1:]:
            new_price = prices[-1] * (1 + ret)
            prices.append(new_price)
        
        # Generate OHLC data
        data = []
        for i, (date, close) in enumerate(zip(dates, prices)):
            # Generate realistic OHLC from close price
            daily_range = close * 0.02  # 2% daily range
            high = close + np.random.uniform(0, daily_range)
            low = close - np.random.uniform(0, daily_range)
            open_price = prices[i-1] if i > 0 else close
            
            # Generate volume
            volume = np.random.randint(1000000, 5000000)
            
            data.append({
                'Open': open_price,
                'High': high,
                'Low': low,
                'Close': close,
                'Volume': volume
            })
        
        # Create DataFrame
        df = pd.DataFrame(data, index=dates)
        
        # Add additional columns that the engine expects
        df['Returns'] = df['Close'].pct_change()
        df['Log_Returns'] = np.log(df['Close'] / df['Close'].shift(1))
        df['Typical_Price'] = (df['High'] + df['Low'] + df['Close']) / 3
        df['Price_Range'] = df['High'] - df['Low']
        df['Pct_Change'] = df['Close'].pct_change() * 100
        
        return df
    
    def get_data_info(self, data: pd.DataFrame) -> dict:
        """
        Get information about the generated data
        
        Args:
            data (pd.DataFrame): Price data
            
        Returns:
            dict: Data information
        """
        if data.empty:
            return {}
        
        info = {
            'start_date': data.index[0],
            'end_date': data.index[-1],
            'total_days': len(data),
            'current_price': data['Close'].iloc[-1],
            'price_change': data['Close'].iloc[-1] - data['Close'].iloc[0],
            'price_change_pct': ((data['Close'].iloc[-1] / data['Close'].iloc[0]) - 1) * 100,
            'avg_volume': data['Volume'].mean(),
            'volatility': data['Returns'].std() * np.sqrt(252),  # Annualized volatility
            'min_price': data['Low'].min(),
            'max_price': data['High'].max()
        }
        
        return info
