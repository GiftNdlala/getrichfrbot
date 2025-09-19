#!/usr/bin/env python3
"""
XAUUSD Trading Signal Engine - Phase 1.1
Main entry point for the trading signal engine
"""

import sys
import os
from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from typing import Optional, Tuple

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data_loader import DataLoader
from src.indicators import TechnicalIndicators
from src.signal_generator import SignalGenerator
from src.visualizer import ChartVisualizer

class TradingSignalEngine:
    """
    Main trading signal engine class
    """
    
    def __init__(self, symbol: str = "XAUUSD"):
        """
        Initialize the trading signal engine
        
        Args:
            symbol (str): Trading symbol for XAUUSD (Gold futures)
        """
        self.symbol = symbol
        self.data_loader = DataLoader()
        self.indicators = TechnicalIndicators()
        self.signal_generator = SignalGenerator()
        self.visualizer = ChartVisualizer()
        self.data = None
        
    def load_data(self, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
        """
        Load historical price data for XAUUSD
        
        Args:
            period (str): Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval (str): Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
            
        Returns:
            pd.DataFrame: Historical price data
        """
        print(f"Loading {period} of {interval} data for {self.symbol}...")
        
        try:
            self.data = self.data_loader.fetch_data(self.symbol, period, interval)
            print(f"Successfully loaded {len(self.data)} data points")
            print(f"Date range: {self.data.index[0].date()} to {self.data.index[-1].date()}")
            return self.data
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def calculate_indicators(self) -> pd.DataFrame:
        """
        Calculate technical indicators for the loaded data
        
        Returns:
            pd.DataFrame: Data with calculated indicators
        """
        if self.data is None:
            print("No data loaded. Please load data first.")
            return None
            
        print("Calculating technical indicators...")
        
        # Calculate basic indicators
        self.data = self.indicators.add_sma(self.data, periods=[20, 50, 200])
        self.data = self.indicators.add_rsi(self.data, period=14)
        self.data = self.indicators.add_macd(self.data)
        self.data = self.indicators.add_bollinger_bands(self.data, period=20)
        
        print("Technical indicators calculated successfully!")
        return self.data
    
    def generate_signals(self) -> pd.DataFrame:
        """
        Generate trading signals based on technical indicators
        
        Returns:
            pd.DataFrame: Data with trading signals
        """
        if self.data is None:
            print("No data with indicators. Please calculate indicators first.")
            return None
            
        print("Generating trading signals...")
        
        # Generate signals based on different strategies
        self.data = self.signal_generator.sma_crossover_signals(self.data)
        self.data = self.signal_generator.rsi_signals(self.data)
        self.data = self.signal_generator.macd_signals(self.data)
        
        # Combine signals into final signal
        self.data = self.signal_generator.combine_signals(self.data)
        
        print("Trading signals generated successfully!")
        return self.data
    
    def visualize_signals(self, save_path: Optional[str] = None):
        """
        Visualize the price data with trading signals
        
        Args:
            save_path (str, optional): Path to save the chart image
        """
        if self.data is None:
            print("No data available for visualization.")
            return
            
        print("Creating visualization...")
        
        # Create the chart
        fig, ax = self.visualizer.create_price_chart(self.data, self.symbol)
        
        # Add signals to the chart
        self.visualizer.add_signals_to_chart(ax, self.data)
        
        # Add indicators to the chart
        self.visualizer.add_indicators_to_chart(ax, self.data)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Chart saved to: {save_path}")
        
        plt.show()
        print("Visualization completed!")
    
    def run_analysis(self, period: str = "1y", interval: str = "1d", 
                    save_chart: bool = False) -> pd.DataFrame:
        """
        Run complete analysis pipeline
        
        Args:
            period (str): Data period
            interval (str): Data interval
            save_chart (bool): Whether to save the chart image
            
        Returns:
            pd.DataFrame: Complete analysis with signals
        """
        print("=" * 50)
        print("XAUUSD TRADING SIGNAL ENGINE - PHASE 1.1")
        print("=" * 50)
        
        # Step 1: Load data
        data = self.load_data(period, interval)
        if data is None:
            return None
        
        # Step 2: Calculate indicators
        data = self.calculate_indicators()
        if data is None:
            return None
        
        # Step 3: Generate signals
        data = self.generate_signals()
        if data is None:
            return None
        
        # Step 4: Visualize results
        chart_path = None
        if save_chart:
            chart_path = f"charts/xauusd_signals_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            os.makedirs("charts", exist_ok=True)
        
        self.visualize_signals(chart_path)
        
        print("=" * 50)
        print("ANALYSIS COMPLETE!")
        print("=" * 50)
        
        return data

def main():
    """
    Main function to run the trading signal engine
    """
    # Create the engine
    engine = TradingSignalEngine()
    
    # Run analysis with default parameters
    # You can modify these parameters as needed
    data = engine.run_analysis(
        period="6mo",      # 6 months of data
        interval="1d",     # Daily intervals
        save_chart=True    # Save the chart
    )
    
    if data is not None:
        # Display some basic statistics
        print("\nBASIC STATISTICS:")
        print(f"Total data points: {len(data)}")
        print(f"Date range: {data.index[0].date()} to {data.index[-1].date()}")
        
        # Count signals
        buy_signals = len(data[data['signal'] == 1])
        sell_signals = len(data[data['signal'] == -1])
        print(f"Buy signals: {buy_signals}")
        print(f"Sell signals: {sell_signals}")

if __name__ == "__main__":
    main()
