"""
Visualization Module for XAUUSD Trading Signal Engine
Creates charts with price data, indicators, and trading signals
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from typing import Optional, Tuple, List
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

class ChartVisualizer:
    """
    Creates visualizations for price data, indicators, and trading signals
    """
    
    def __init__(self):
        """Initialize the chart visualizer"""
        # Set style for better-looking charts
        plt.style.use('seaborn-v0_8')
        
        # Color scheme
        self.colors = {
            'price': '#1f77b4',
            'sma_20': '#ff7f0e',
            'sma_50': '#2ca02c',
            'sma_200': '#d62728',
            'rsi': '#9467bd',
            'macd': '#8c564b',
            'bollinger': '#e377c2',
            'buy_signal': '#2ca02c',
            'sell_signal': '#d62728',
            'volume': '#7f7f7f'
        }
    
    def create_price_chart(self, data: pd.DataFrame, symbol: str = "XAUUSD") -> Tuple[plt.Figure, plt.Axes]:
        """
        Create the main price chart
        
        Args:
            data (pd.DataFrame): Price data with indicators
            symbol (str): Trading symbol
            
        Returns:
            Tuple[plt.Figure, plt.Axes]: Figure and axes objects
        """
        # Create figure and axes
        fig, ax = plt.subplots(figsize=(15, 8))
        
        # Plot price data
        ax.plot(data.index, data['Close'], color=self.colors['price'], 
                linewidth=1.5, label='Close Price', alpha=0.8)
        
        # Add candlestick-like visualization
        ax.fill_between(data.index, data['Low'], data['High'], 
                       alpha=0.1, color=self.colors['price'])
        
        # Customize the chart
        ax.set_title(f'{symbol} Price Chart with Trading Signals', 
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Price (USD)', fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        return fig, ax
    
    def add_indicators_to_chart(self, ax: plt.Axes, data: pd.DataFrame) -> None:
        """
        Add technical indicators to the price chart
        
        Args:
            ax (plt.Axes): Matplotlib axes object
            data (pd.DataFrame): Price data with indicators
        """
        # Add SMA lines
        sma_columns = [col for col in data.columns if col.startswith('SMA_')]
        for sma_col in sma_columns:
            if sma_col in data.columns and not data[sma_col].isna().all():
                period = sma_col.split('_')[1]
                color_key = f'sma_{period}' if period in ['20', '50', '200'] else 'sma_20'
                color = self.colors.get(color_key, self.colors['sma_20'])
                
                ax.plot(data.index, data[sma_col], color=color, 
                       linewidth=1, label=f'SMA {period}', alpha=0.7)
        
        # Add Bollinger Bands
        bb_upper = [col for col in data.columns if col.startswith('BB_Upper_')]
        bb_lower = [col for col in data.columns if col.startswith('BB_Lower_')]
        
        if bb_upper and bb_lower:
            upper_col = bb_upper[0]
            lower_col = bb_lower[0]
            
            if upper_col in data.columns and lower_col in data.columns:
                ax.plot(data.index, data[upper_col], color=self.colors['bollinger'], 
                       linewidth=1, label='BB Upper', alpha=0.6, linestyle='--')
                ax.plot(data.index, data[lower_col], color=self.colors['bollinger'], 
                       linewidth=1, label='BB Lower', alpha=0.6, linestyle='--')
                
                # Fill Bollinger Bands area
                ax.fill_between(data.index, data[lower_col], data[upper_col], 
                               alpha=0.1, color=self.colors['bollinger'])
        
        # Update legend
        ax.legend(loc='upper left', fontsize=10)
    
    def add_signals_to_chart(self, ax: plt.Axes, data: pd.DataFrame) -> None:
        """
        Add trading signals to the chart
        
        Args:
            ax (plt.Axes): Matplotlib axes object
            data (pd.DataFrame): Price data with signals
        """
        if 'signal' not in data.columns:
            return
        
        # Get signal points
        buy_signals = data[data['signal'] == 1]
        sell_signals = data[data['signal'] == -1]
        
        # Plot buy signals
        if not buy_signals.empty:
            ax.scatter(buy_signals.index, buy_signals['Close'], 
                      color=self.colors['buy_signal'], marker='^', s=100, 
                      label='Buy Signal', zorder=5, alpha=0.8)
        
        # Plot sell signals
        if not sell_signals.empty:
            ax.scatter(sell_signals.index, sell_signals['Close'], 
                      color=self.colors['sell_signal'], marker='v', s=100, 
                      label='Sell Signal', zorder=5, alpha=0.8)
        
        # Update legend
        ax.legend(loc='upper left', fontsize=10)
    
    def create_rsi_chart(self, data: pd.DataFrame, symbol: str = "XAUUSD") -> Tuple[plt.Figure, plt.Axes]:
        """
        Create RSI chart
        
        Args:
            data (pd.DataFrame): Price data with RSI
            symbol (str): Trading symbol
            
        Returns:
            Tuple[plt.Figure, plt.Axes]: Figure and axes objects
        """
        rsi_columns = [col for col in data.columns if col.startswith('RSI_')]
        
        if not rsi_columns:
            print("No RSI data found")
            return None, None
        
        fig, ax = plt.subplots(figsize=(15, 4))
        
        # Plot RSI
        rsi_col = rsi_columns[0]
        ax.plot(data.index, data[rsi_col], color=self.colors['rsi'], 
                linewidth=1.5, label='RSI')
        
        # Add overbought and oversold lines
        ax.axhline(y=70, color='red', linestyle='--', alpha=0.7, label='Overbought (70)')
        ax.axhline(y=30, color='green', linestyle='--', alpha=0.7, label='Oversold (30)')
        ax.axhline(y=50, color='gray', linestyle='-', alpha=0.5, label='Neutral (50)')
        
        # Customize chart
        ax.set_title(f'{symbol} RSI Indicator', fontsize=14, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('RSI', fontsize=12)
        ax.set_ylim(0, 100)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        return fig, ax
    
    def create_macd_chart(self, data: pd.DataFrame, symbol: str = "XAUUSD") -> Tuple[plt.Figure, plt.Axes]:
        """
        Create MACD chart
        
        Args:
            data (pd.DataFrame): Price data with MACD
            symbol (str): Trading symbol
            
        Returns:
            Tuple[plt.Figure, plt.Axes]: Figure and axes objects
        """
        macd_columns = [col for col in data.columns if col.startswith('MACD_')]
        
        if len(macd_columns) < 2:
            print("Insufficient MACD data found")
            return None, None
        
        fig, ax = plt.subplots(figsize=(15, 4))
        
        # Find MACD line and signal line
        macd_line = None
        signal_line = None
        
        for col in macd_columns:
            if 'Signal' in col:
                signal_line = col
            elif 'Histogram' not in col:
                macd_line = col
        
        if macd_line and signal_line:
            # Plot MACD line
            ax.plot(data.index, data[macd_line], color=self.colors['macd'], 
                    linewidth=1.5, label='MACD Line')
            
            # Plot signal line
            ax.plot(data.index, data[signal_line], color='orange', 
                    linewidth=1.5, label='Signal Line')
            
            # Plot histogram
            if 'MACD_Histogram' in data.columns:
                colors = ['green' if x >= 0 else 'red' for x in data['MACD_Histogram']]
                ax.bar(data.index, data['MACD_Histogram'], color=colors, 
                       alpha=0.6, label='MACD Histogram')
        
        # Add zero line
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        
        # Customize chart
        ax.set_title(f'{symbol} MACD Indicator', fontsize=14, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('MACD', fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        return fig, ax
    
    def create_volume_chart(self, data: pd.DataFrame, symbol: str = "XAUUSD") -> Tuple[plt.Figure, plt.Axes]:
        """
        Create volume chart
        
        Args:
            data (pd.DataFrame): Price data with volume
            symbol (str): Trading symbol
            
        Returns:
            Tuple[plt.Figure, plt.Axes]: Figure and axes objects
        """
        if 'Volume' not in data.columns:
            print("No volume data found")
            return None, None
        
        fig, ax = plt.subplots(figsize=(15, 4))
        
        # Create volume bars with color based on price direction
        colors = ['green' if close > open else 'red' 
                 for close, open in zip(data['Close'], data['Open'])]
        
        ax.bar(data.index, data['Volume'], color=colors, alpha=0.6, label='Volume')
        
        # Add volume SMA if available
        if 'Volume_SMA_20' in data.columns:
            ax.plot(data.index, data['Volume_SMA_20'], color='blue', 
                    linewidth=1.5, label='Volume SMA (20)')
        
        # Customize chart
        ax.set_title(f'{symbol} Volume', fontsize=14, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Volume', fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        return fig, ax
    
    def create_comprehensive_chart(self, data: pd.DataFrame, symbol: str = "XAUUSD") -> plt.Figure:
        """
        Create a comprehensive chart with price, RSI, MACD, and volume
        
        Args:
            data (pd.DataFrame): Price data with indicators
            symbol (str): Trading symbol
            
        Returns:
            plt.Figure: Comprehensive chart figure
        """
        # Create subplots
        fig, axes = plt.subplots(4, 1, figsize=(15, 12), 
                                gridspec_kw={'height_ratios': [3, 1, 1, 1]})
        
        # Main price chart
        ax_price = axes[0]
        ax_price.plot(data.index, data['Close'], color=self.colors['price'], 
                     linewidth=1.5, label='Close Price')
        
        # Add indicators to price chart
        self.add_indicators_to_chart(ax_price, data)
        self.add_signals_to_chart(ax_price, data)
        
        ax_price.set_title(f'{symbol} Comprehensive Analysis', fontsize=16, fontweight='bold')
        ax_price.set_ylabel('Price (USD)', fontsize=12)
        ax_price.grid(True, alpha=0.3)
        ax_price.legend()
        
        # RSI chart
        ax_rsi = axes[1]
        rsi_columns = [col for col in data.columns if col.startswith('RSI_')]
        if rsi_columns:
            rsi_col = rsi_columns[0]
            ax_rsi.plot(data.index, data[rsi_col], color=self.colors['rsi'], linewidth=1.5)
            ax_rsi.axhline(y=70, color='red', linestyle='--', alpha=0.7)
            ax_rsi.axhline(y=30, color='green', linestyle='--', alpha=0.7)
            ax_rsi.axhline(y=50, color='gray', linestyle='-', alpha=0.5)
            ax_rsi.set_ylabel('RSI', fontsize=12)
            ax_rsi.set_ylim(0, 100)
            ax_rsi.grid(True, alpha=0.3)
        
        # MACD chart
        ax_macd = axes[2]
        macd_columns = [col for col in data.columns if col.startswith('MACD_')]
        if len(macd_columns) >= 2:
            macd_line = [col for col in macd_columns if 'Signal' not in col and 'Histogram' not in col][0]
            signal_line = [col for col in macd_columns if 'Signal' in col][0]
            
            ax_macd.plot(data.index, data[macd_line], color=self.colors['macd'], linewidth=1.5)
            ax_macd.plot(data.index, data[signal_line], color='orange', linewidth=1.5)
            ax_macd.axhline(y=0, color='black', linestyle='-', alpha=0.5)
            ax_macd.set_ylabel('MACD', fontsize=12)
            ax_macd.grid(True, alpha=0.3)
        
        # Volume chart
        ax_volume = axes[3]
        if 'Volume' in data.columns:
            colors = ['green' if close > open else 'red' 
                     for close, open in zip(data['Close'], data['Open'])]
            ax_volume.bar(data.index, data['Volume'], color=colors, alpha=0.6)
            ax_volume.set_ylabel('Volume', fontsize=12)
            ax_volume.grid(True, alpha=0.3)
        
        # Format x-axis for all subplots
        for ax in axes:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        return fig
    
    def plot_signal_statistics(self, data: pd.DataFrame, symbol: str = "XAUUSD") -> plt.Figure:
        """
        Create a chart showing signal statistics
        
        Args:
            data (pd.DataFrame): Price data with signals
            symbol (str): Trading symbol
            
        Returns:
            plt.Figure: Statistics chart
        """
        if 'signal' not in data.columns:
            print("No signal data found")
            return None
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Signal distribution
        signal_counts = data['signal'].value_counts()
        colors = ['gray', 'green', 'red']
        labels = ['No Signal', 'Buy', 'Sell']
        
        ax1.pie(signal_counts.values, labels=labels, colors=colors, autopct='%1.1f%%')
        ax1.set_title('Signal Distribution')
        
        # Signal over time
        buy_signals = data[data['signal'] == 1]
        sell_signals = data[data['signal'] == -1]
        
        ax2.scatter(buy_signals.index, buy_signals['Close'], 
                   color='green', marker='^', s=50, alpha=0.7, label='Buy Signals')
        ax2.scatter(sell_signals.index, sell_signals['Close'], 
                   color='red', marker='v', s=50, alpha=0.7, label='Sell Signals')
        ax2.plot(data.index, data['Close'], color='blue', alpha=0.5, label='Price')
        
        ax2.set_title(f'{symbol} Signals Over Time')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Price')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
