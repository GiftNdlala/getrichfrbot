"""
Backtesting Framework for XAUUSD Trading Signal Engine
Implements comprehensive backtesting with performance metrics and risk analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

class BacktestEngine:
    """
    Comprehensive backtesting engine for trading strategies
    """
    
    def __init__(self, initial_capital: float = 10000, commission: float = 0.001, slippage: float = 0.0005):
        """
        Initialize the backtesting engine
        
        Args:
            initial_capital (float): Starting capital for backtesting
            commission (float): Commission rate per trade (default: 0.1%)
            slippage (float): Slippage rate per trade (default: 0.05%)
        """
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage
        self.trades = []
        self.portfolio_value = []
        self.positions = []
        
    def execute_backtest(self, data: pd.DataFrame, signals: pd.Series) -> Dict:
        """
        Execute backtesting on historical data with signals
        
        Args:
            data (pd.DataFrame): Price data with OHLCV
            signals (pd.Series): Trading signals (-1, 0, 1)
            
        Returns:
            Dict: Comprehensive backtesting results
        """
        print("Starting backtesting...")
        
        # Initialize variables
        capital = self.initial_capital
        position = 0  # 0: no position, 1: long, -1: short
        shares = 0
        entry_price = 0
        portfolio_values = []
        trades = []
        positions = []
        
        # Process each day
        for i, (date, row) in enumerate(data.iterrows()):
            current_price = row['Close']
            signal = signals.iloc[i] if i < len(signals) else 0
            
            # Calculate current portfolio value
            if position == 0:
                portfolio_value = capital
            elif position == 1:  # Long position
                portfolio_value = capital + shares * (current_price - entry_price)
            else:  # Short position (position == -1)
                portfolio_value = capital - shares * (current_price - entry_price)
            
            portfolio_values.append({
                'Date': date,
                'Portfolio_Value': portfolio_value,
                'Price': current_price,
                'Position': position,
                'Signal': signal
            })
            
            # Execute trades based on signals
            if signal == 1 and position != 1:  # Buy signal
                if position == -1:  # Close short position
                    profit = shares * (entry_price - current_price) * (1 - self.commission - self.slippage)
                    capital += profit
                    trades.append({
                        'Date': date,
                        'Type': 'Cover',
                        'Price': current_price,
                        'Shares': shares,
                        'Value': shares * current_price,
                        'Profit': profit,
                        'Capital': capital
                    })
                
                # Open long position
                shares = int(capital * 0.95 / current_price)  # Use 95% of capital, leave some for fees
                if shares > 0:
                    entry_price = current_price * (1 + self.slippage)
                    cost = shares * entry_price * (1 + self.commission)
                    capital -= cost
                    position = 1
                    
                    trades.append({
                        'Date': date,
                        'Type': 'Buy',
                        'Price': entry_price,
                        'Shares': shares,
                        'Value': shares * entry_price,
                        'Profit': 0,
                        'Capital': capital
                    })
            
            elif signal == -1 and position != -1:  # Sell signal
                if position == 1:  # Close long position
                    profit = shares * (current_price - entry_price) * (1 - self.commission - self.slippage)
                    capital += profit
                    trades.append({
                        'Date': date,
                        'Type': 'Sell',
                        'Price': current_price,
                        'Shares': shares,
                        'Value': shares * current_price,
                        'Profit': profit,
                        'Capital': capital
                    })
                
                # Open short position
                shares = int(capital * 0.95 / current_price)
                if shares > 0:
                    entry_price = current_price * (1 - self.slippage)
                    capital_used = shares * entry_price * (1 + self.commission)
                    position = -1
                    
                    trades.append({
                        'Date': date,
                        'Type': 'Short',
                        'Price': entry_price,
                        'Shares': shares,
                        'Value': shares * entry_price,
                        'Profit': 0,
                        'Capital': capital
                    })
        
        # Close any remaining position
        if position != 0:
            final_price = data['Close'].iloc[-1]
            if position == 1:  # Close long
                profit = shares * (final_price - entry_price) * (1 - self.commission - self.slippage)
                trades.append({
                    'Date': data.index[-1],
                    'Type': 'Sell',
                    'Price': final_price,
                    'Shares': shares,
                    'Value': shares * final_price,
                    'Profit': profit,
                    'Capital': capital + profit
                })
            else:  # Close short
                profit = shares * (entry_price - final_price) * (1 - self.commission - self.slippage)
                trades.append({
                    'Date': data.index[-1],
                    'Type': 'Cover',
                    'Price': final_price,
                    'Shares': shares,
                    'Value': shares * final_price,
                    'Profit': profit,
                    'Capital': capital + profit
                })
        
        # Store results
        self.trades = trades
        self.portfolio_value = pd.DataFrame(portfolio_values).set_index('Date')
        
        # Calculate performance metrics
        results = self.calculate_performance_metrics()
        
        print(f"Backtesting completed! Final portfolio value: ${results['Final_Value']:,.2f}")
        return results
    
    def calculate_performance_metrics(self) -> Dict:
        """
        Calculate comprehensive performance metrics
        
        Returns:
            Dict: Performance metrics
        """
        if not self.trades or self.portfolio_value.empty:
            return {}
        
        # Basic metrics
        initial_value = self.initial_capital
        final_value = self.portfolio_value['Portfolio_Value'].iloc[-1]
        total_return = (final_value - initial_value) / initial_value
        
        # Returns series
        portfolio_returns = self.portfolio_value['Portfolio_Value'].pct_change().dropna()
        
        # Trading metrics
        trades_df = pd.DataFrame(self.trades)
        profitable_trades = trades_df[trades_df['Profit'] > 0]
        losing_trades = trades_df[trades_df['Profit'] < 0]
        
        # Calculate metrics
        total_trades = len(trades_df)
        winning_trades = len(profitable_trades)
        losing_trades_count = len(losing_trades)
        win_rate = winning_trades / total_trades if total_trades > 0 else 0
        
        avg_win = profitable_trades['Profit'].mean() if not profitable_trades.empty else 0
        avg_loss = losing_trades['Profit'].mean() if not losing_trades.empty else 0
        profit_factor = abs(profitable_trades['Profit'].sum() / losing_trades['Profit'].sum()) if not losing_trades.empty and losing_trades['Profit'].sum() != 0 else float('inf')
        
        # Risk metrics
        volatility = portfolio_returns.std() * np.sqrt(252) if len(portfolio_returns) > 1 else 0
        
        # Drawdown analysis
        running_max = self.portfolio_value['Portfolio_Value'].expanding().max()
        drawdown = (self.portfolio_value['Portfolio_Value'] - running_max) / running_max
        max_drawdown = drawdown.min()
        
        # Sharpe ratio (assuming 0% risk-free rate)
        sharpe_ratio = (portfolio_returns.mean() * 252) / volatility if volatility > 0 else 0
        
        # Time-based metrics
        start_date = self.portfolio_value.index[0]
        end_date = self.portfolio_value.index[-1]
        days = (end_date - start_date).days
        annualized_return = (final_value / initial_value) ** (365 / days) - 1 if days > 0 else 0
        
        metrics = {
            # Basic Performance
            'Initial_Capital': initial_value,
            'Final_Value': final_value,
            'Total_Return': total_return,
            'Annualized_Return': annualized_return,
            
            # Trading Metrics
            'Total_Trades': total_trades,
            'Winning_Trades': winning_trades,
            'Losing_Trades': losing_trades_count,
            'Win_Rate': win_rate,
            'Average_Win': avg_win,
            'Average_Loss': avg_loss,
            'Profit_Factor': profit_factor,
            
            # Risk Metrics
            'Volatility': volatility,
            'Max_Drawdown': max_drawdown,
            'Sharpe_Ratio': sharpe_ratio,
            
            # Time Metrics
            'Start_Date': start_date,
            'End_Date': end_date,
            'Days': days,
            
            # Raw Data
            'Portfolio_Value': self.portfolio_value,
            'Trades': pd.DataFrame(self.trades)
        }
        
        return metrics
    
    def print_performance_report(self, results: Dict):
        """
        Print a comprehensive performance report
        
        Args:
            results (Dict): Backtesting results from calculate_performance_metrics
        """
        print("\n" + "="*60)
        print("📊 BACKTESTING PERFORMANCE REPORT")
        print("="*60)
        
        print("\n💰 FINANCIAL PERFORMANCE")
        print("-" * 30)
        print(f"Initial Capital:     ${results['Initial_Capital']:>12,.2f}")
        print(f"Final Value:         ${results['Final_Value']:>12,.2f}")
        print(f"Total Return:        {results['Total_Return']:>12.2%}")
        print(f"Annualized Return:   {results['Annualized_Return']:>12.2%}")
        
        print("\n📈 TRADING STATISTICS")
        print("-" * 30)
        print(f"Total Trades:        {results['Total_Trades']:>12}")
        print(f"Winning Trades:      {results['Winning_Trades']:>12}")
        print(f"Losing Trades:       {results['Losing_Trades']:>12}")
        print(f"Win Rate:            {results['Win_Rate']:>12.2%}")
        print(f"Average Win:         ${results['Average_Win']:>12.2f}")
        print(f"Average Loss:        ${results['Average_Loss']:>12.2f}")
        print(f"Profit Factor:       {results['Profit_Factor']:>12.2f}")
        
        print("\n⚠️ RISK ANALYSIS")
        print("-" * 30)
        print(f"Volatility:          {results['Volatility']:>12.2%}")
        print(f"Max Drawdown:        {results['Max_Drawdown']:>12.2%}")
        print(f"Sharpe Ratio:        {results['Sharpe_Ratio']:>12.2f}")
        
        print("\n📅 TIME PERIOD")
        print("-" * 30)
        print(f"Start Date:          {results['Start_Date'].strftime('%Y-%m-%d')}")
        print(f"End Date:            {results['End_Date'].strftime('%Y-%m-%d')}")
        print(f"Total Days:          {results['Days']:>12}")
        
        print("\n" + "="*60)
        
        # Performance summary
        if results['Total_Return'] > 0:
            print("🎉 STRATEGY PERFORMANCE: PROFITABLE")
        else:
            print("⚠️ STRATEGY PERFORMANCE: UNPROFITABLE")
            
        if results['Win_Rate'] > 0.5:
            print("✅ Win Rate: Above 50%")
        else:
            print("❌ Win Rate: Below 50%")
            
        if results['Sharpe_Ratio'] > 1.0:
            print("✅ Sharpe Ratio: Excellent (>1.0)")
        elif results['Sharpe_Ratio'] > 0.5:
            print("⚠️ Sharpe Ratio: Good (>0.5)")
        else:
            print("❌ Sharpe Ratio: Poor (<0.5)")
            
        print("="*60)
    
    def create_performance_charts(self, results: Dict, save_path: str = None) -> plt.Figure:
        """
        Create comprehensive performance visualization charts
        
        Args:
            results (Dict): Backtesting results
            save_path (str): Path to save the chart
            
        Returns:
            plt.Figure: The created figure
        """
        # Create figure with subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Backtesting Performance Analysis', fontsize=16, fontweight='bold')
        
        # 1. Portfolio Value Over Time
        portfolio_df = results['Portfolio_Value']
        ax1.plot(portfolio_df.index, portfolio_df['Portfolio_Value'], 
                linewidth=2, color='blue', label='Portfolio Value')
        ax1.axhline(y=self.initial_capital, color='red', linestyle='--', alpha=0.7, label='Initial Capital')
        ax1.set_title('Portfolio Value Over Time')
        ax1.set_ylabel('Value ($)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Drawdown Chart
        running_max = portfolio_df['Portfolio_Value'].expanding().max()
        drawdown = (portfolio_df['Portfolio_Value'] - running_max) / running_max * 100
        ax2.fill_between(drawdown.index, drawdown.values, 0, 
                        color='red', alpha=0.3, label='Drawdown')
        ax2.plot(drawdown.index, drawdown.values, color='red', linewidth=1)
        ax2.set_title('Drawdown Analysis')
        ax2.set_ylabel('Drawdown (%)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Monthly Returns Heatmap
        if len(portfolio_df) > 30:  # Only if we have enough data
            monthly_returns = portfolio_df['Portfolio_Value'].resample('M').last().pct_change().dropna() * 100
            
            if len(monthly_returns) > 0:
                # Create a simple bar chart instead of heatmap for simplicity
                monthly_returns.plot(kind='bar', ax=ax3, color=['green' if x > 0 else 'red' for x in monthly_returns])
                ax3.set_title('Monthly Returns')
                ax3.set_ylabel('Return (%)')
                ax3.tick_params(axis='x', rotation=45)
        else:
            ax3.text(0.5, 0.5, 'Insufficient data for\nmonthly analysis', 
                    horizontalalignment='center', verticalalignment='center', 
                    transform=ax3.transAxes, fontsize=12)
            ax3.set_title('Monthly Returns')
        
        # 4. Trade Analysis
        if results['Trades'] is not None and not results['Trades'].empty:
            trades_df = results['Trades']
            profits = trades_df['Profit'].dropna()
            
            if len(profits) > 0:
                profits.hist(bins=20, ax=ax4, color='lightblue', edgecolor='black', alpha=0.7)
                ax4.axvline(x=0, color='red', linestyle='--', alpha=0.7)
                ax4.set_title('Trade Profit Distribution')
                ax4.set_xlabel('Profit/Loss ($)')
                ax4.set_ylabel('Frequency')
        else:
            ax4.text(0.5, 0.5, 'No completed trades\nto analyze', 
                    horizontalalignment='center', verticalalignment='center', 
                    transform=ax4.transAxes, fontsize=12)
            ax4.set_title('Trade Analysis')
        
        plt.tight_layout()
        
        # Save chart if path provided
        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Performance charts saved to: {save_path}")
        
        return fig