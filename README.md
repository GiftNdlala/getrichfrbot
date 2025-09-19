# XAUUSD Trading Signal Engine

A comprehensive trading signal engine for XAUUSD (Gold) that generates buy/sell signals based on technical indicators and displays them on interactive charts.

## 🚀 Features

- **Real-time Data**: Fetches live XAUUSD data using Yahoo Finance API
- **Technical Indicators**: Implements SMA, RSI, MACD, Bollinger Bands, and more
- **Signal Generation**: Combines multiple indicators to generate trading signals
- **Visual Charts**: Creates beautiful charts with price data, indicators, and signals
- **Backtesting Ready**: Structured for easy backtesting and performance analysis

## 📋 Requirements

- Python 3.7+
- Internet connection for data fetching
- Required packages (see `requirements.txt`)

## 🛠️ Installation

### Quick Setup

1. **Clone or download the project**
2. **Run the setup script**:
   ```bash
   python setup.py
   ```

### Manual Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Create directories**:
   ```bash
   mkdir data charts logs
   ```

## 🎯 Usage

### Basic Usage

Run the main engine:
```bash
python main.py
```

This will:
- Load 6 months of daily XAUUSD data
- Calculate technical indicators
- Generate trading signals
- Display interactive charts
- Save results to the `charts/` directory

### Testing

Test the engine with a smaller dataset:
```bash
python test_engine.py
```

### Custom Parameters

You can modify the analysis parameters in `main.py`:

```python
data = engine.run_analysis(
    period="1y",        # Data period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
    interval="1d",      # Data interval: 1m, 5m, 15m, 30m, 1h, 1d, 1wk, 1mo
    save_chart=True     # Save chart to file
)
```

## 📊 Technical Indicators

The engine calculates the following indicators:

### Moving Averages
- **SMA (20, 50, 200)**: Simple Moving Averages
- **EMA (12, 26)**: Exponential Moving Averages

### Oscillators
- **RSI (14)**: Relative Strength Index
- **MACD**: Moving Average Convergence Divergence
- **Stochastic**: Stochastic Oscillator

### Volatility
- **Bollinger Bands (20)**: Price volatility bands
- **ATR (14)**: Average True Range

### Volume
- **Volume SMA**: Average volume
- **Volume Ratio**: Current vs average volume
- **OBV**: On-Balance Volume

## 🎯 Trading Signals

The engine generates signals based on:

1. **SMA Crossovers**: Fast SMA crossing above/below slow SMA
2. **RSI Levels**: Oversold (30) and overbought (70) conditions
3. **MACD Crossovers**: MACD line crossing signal line
4. **Bollinger Bands**: Price touching upper/lower bands
5. **Volume Confirmation**: High volume supporting price movement
6. **Trend Following**: Multiple indicator confirmation

### Signal Types
- **Buy Signal (1)**: Green triangle pointing up
- **Sell Signal (-1)**: Red triangle pointing down
- **No Signal (0)**: No clear direction

## 📈 Chart Features

### Main Price Chart
- Candlestick-like price visualization
- Moving average overlays
- Bollinger Bands
- Buy/Sell signal markers

### Additional Charts
- **RSI Chart**: With overbought/oversold levels
- **MACD Chart**: With signal line and histogram
- **Volume Chart**: With volume bars and SMA

### Comprehensive View
- 4-panel layout with price, RSI, MACD, and volume
- Synchronized time scales
- Interactive zoom and pan

## 🏗️ Project Structure

```
GetRichFrBot/
├── main.py                 # Main entry point
├── test_engine.py          # Test script
├── setup.py               # Setup script
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── src/                  # Source code
│   ├── __init__.py
│   ├── data_loader.py    # Data fetching and processing
│   ├── indicators.py     # Technical indicators
│   ├── signal_generator.py # Signal generation logic
│   └── visualizer.py     # Chart creation
├── data/                 # Saved data files
├── charts/               # Generated charts
└── logs/                 # Log files
```

## 🔧 Customization

### Adding New Indicators

1. Add indicator calculation in `src/indicators.py`
2. Add signal generation in `src/signal_generator.py`
3. Add visualization in `src/visualizer.py`

### Modifying Signal Logic

Edit the signal generation methods in `src/signal_generator.py`:
- `sma_crossover_signals()`
- `rsi_signals()`
- `macd_signals()`
- `combine_signals()`

### Changing Data Source

Modify `src/data_loader.py` to use different data sources:
- Alpha Vantage API
- Interactive Brokers
- MT4/MT5 data export

## 📊 Output Examples

The engine generates:
- **Interactive charts** with price and signals
- **Signal statistics** (buy/sell ratios)
- **Performance metrics** (optional backtesting)
- **Saved data files** for further analysis

## 🚨 Disclaimer

This is a **educational and research tool**. Trading involves risk, and past performance does not guarantee future results. Always:
- Test strategies thoroughly
- Use proper risk management
- Never invest more than you can afford to lose
- Consider consulting with financial advisors

## 🔄 Future Enhancements

### Phase 1.4 - Basic Backtesting
- [ ] Implement backtesting framework
- [ ] Calculate performance metrics
- [ ] Risk analysis tools

### Phase 2 - Real-time Trading
- [ ] Live data streaming
- [ ] Real-time signal generation
- [ ] Automated trading integration

### Phase 3 - Advanced Features
- [ ] Machine learning integration
- [ ] Multi-timeframe analysis
- [ ] News sentiment analysis
- [ ] Mobile dashboard

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is for educational purposes. Use at your own risk.

## 📞 Support

For questions or issues:
1. Check the documentation
2. Review the code comments
3. Test with `test_engine.py`
4. Create an issue with detailed information

---

**Happy Trading! 📈💰**
