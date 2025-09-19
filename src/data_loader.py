"""
Data Loader Module for XAUUSD Trading Signal Engine
Handles fetching and processing historical price data
"""

import pandas as pd
import yfinance as yf
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, Tuple
import warnings
from .mock_data_generator import MockDataGenerator

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

class DataLoader:
    """
    Handles loading and processing of historical price data
    """
    
    def __init__(self):
        """Initialize the data loader"""
        self.supported_symbols = {
            'XAUUSD': 'GC=F',     # Gold Futures
            'GOLD': 'GC=F',        # Gold Futures
            'XAU': 'GC=F',         # Gold Futures
            'SPY': 'SPY',          # S&P 500 ETF (fallback)
            'AAPL': 'AAPL'         # Apple stock (fallback)
        }
        self.mock_generator = MockDataGenerator()
        self.use_mock_data = False
    
    def fetch_data(self, symbol: str, period: str = "1y", 
                   interval: str = "1d") -> pd.DataFrame:
        """
        Fetch historical price data using yfinance
        
        Args:
            symbol (str): Trading symbol (e.g., 'GC=F' for Gold futures)
            period (str): Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval (str): Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
            
        Returns:
            pd.DataFrame: Historical price data with OHLCV columns
        """
        try:
            # Normalize symbol
            symbol = self._normalize_symbol(symbol)
            
            # Fetch data using yfinance
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval)
            
            if data.empty:
                print(f"Warning: No data found for {symbol}, trying fallback...")
                # Try fallback symbols
                fallback_symbols = ['SPY', 'AAPL', 'MSFT']
                for fallback in fallback_symbols:
                    print(f"Trying fallback symbol: {fallback}")
                    ticker = yf.Ticker(fallback)
                    data = ticker.history(period=period, interval=interval)
                    if not data.empty:
                        print(f"Successfully loaded data for {fallback}")
                        break
                
                if data.empty:
                    raise ValueError(f"No data found for any symbol")
            
            # Clean and prepare the data
            data = self._clean_data(data)
            
            return data
            
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            print("Falling back to mock data for testing...")
            return self._generate_mock_data(period)
    
    def _normalize_symbol(self, symbol: str) -> str:
        """
        Normalize symbol to standard format
        
        Args:
            symbol (str): Input symbol
            
        Returns:
            str: Normalized symbol
        """
        symbol = symbol.upper()
        
        # Check if it's a supported symbol
        if symbol in self.supported_symbols:
            return self.supported_symbols[symbol]
        
        # If it's already in the correct format, return as is
        if symbol == 'SPY':
            return symbol
        
        # Default to XAUUSD
        return 'XAUUSD'
    
    def _generate_mock_data(self, period: str = "3mo") -> pd.DataFrame:
        """
        Generate mock data when real data is unavailable
        
        Args:
            period (str): Data period
            
        Returns:
            pd.DataFrame: Mock price data
        """
        # Convert period to days
        period_days = {
            '1d': 1, '5d': 5, '1mo': 30, '3mo': 90, 
            '6mo': 180, '1y': 365, '2y': 730, '5y': 1825, '10y': 3650, 'max': 3650
        }
        
        days = period_days.get(period, 90)
        
        print(f"Generating {days} days of mock XAUUSD data...")
        mock_data = self.mock_generator.generate_price_data(days)
        
        # Add some realistic gold price characteristics
        mock_data['Close'] = mock_data['Close'] + np.random.normal(0, 10, len(mock_data))
        mock_data['High'] = mock_data[['Open', 'Close']].max(axis=1) + np.random.uniform(0, 20, len(mock_data))
        mock_data['Low'] = mock_data[['Open', 'Close']].min(axis=1) - np.random.uniform(0, 20, len(mock_data))
        
        return mock_data
    
    def _clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and prepare the data for analysis
        
        Args:
            data (pd.DataFrame): Raw price data
            
        Returns:
            pd.DataFrame: Cleaned data
        """
        # Remove any rows with NaN values
        data = data.dropna()
        
        # Ensure we have the required columns
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        missing_columns = [col for col in required_columns if col not in data.columns]
        
        if missing_columns:
            print(f"Warning: Missing columns: {missing_columns}")
        
        # Add additional useful columns
        data['Returns'] = data['Close'].pct_change()
        data['Log_Returns'] = np.log(data['Close'] / data['Close'].shift(1))
        
        # Calculate typical price (used for some indicators)
        data['Typical_Price'] = (data['High'] + data['Low'] + data['Close']) / 3
        
        # Calculate price range
        data['Price_Range'] = data['High'] - data['Low']
        
        # Calculate percentage change
        data['Pct_Change'] = data['Close'].pct_change() * 100
        
        return data
    
    def get_data_info(self, data: pd.DataFrame) -> dict:
        """
        Get information about the loaded data
        
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
    
    def save_data(self, data: pd.DataFrame, filename: str = None) -> str:
        """
        Save data to CSV file
        
        Args:
            data (pd.DataFrame): Data to save
            filename (str, optional): Filename. If None, auto-generate
            
        Returns:
            str: Path to saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"data/xauusd_data_{timestamp}.csv"
        
        # Create data directory if it doesn't exist
        import os
        os.makedirs('data', exist_ok=True)
        
        # Save to CSV
        data.to_csv(filename)
        print(f"Data saved to: {filename}")
        
        return filename
    
    def load_saved_data(self, filename: str) -> pd.DataFrame:
        """
        Load data from saved CSV file
        
        Args:
            filename (str): Path to CSV file
            
        Returns:
            pd.DataFrame: Loaded data
        """
        try:
            data = pd.read_csv(filename, index_col=0, parse_dates=True)
            print(f"Data loaded from: {filename}")
            return data
        except Exception as e:
            print(f"Error loading data from {filename}: {e}")
            return pd.DataFrame()
