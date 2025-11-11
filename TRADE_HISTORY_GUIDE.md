# Trade History Analyzer Guide

This guide explains how to retrieve and analyze your historical trade data.

## 📋 Overview

The trade history analyzer allows you to retrieve detailed information about your past trades including:
- Which signal/strategy placed the trade
- When the trade was opened and closed
- Entry and exit prices
- Profit/Loss for each trade
- Win rate and performance statistics
- Breakdown by strategy

## 🚀 Quick Start

### For Last 24 Hours
```powershell
.\get_trades_24h.ps1
```

### For Last 7 Days
```powershell
.\get_trades_7d.ps1
```

## 📊 What You'll See

The report includes:

### Summary Statistics
- Total number of trades
- Closed vs Open trades
- Win/Loss count and win rate
- Total P&L
- Average P&L per trade
- Average win and loss amounts
- Largest win and loss

### Performance by Strategy
Each strategy (FARMER, INTRADAY_LOW, INTRADAY_MED, SWING_HIGH, etc.) is analyzed separately showing:
- Number of trades
- Win rate
- Total P&L

### Detailed Trade List
Each trade shows:
- Timestamp
- Ticket number
- Strategy that placed it
- Direction (BUY/SELL)
- Entry price
- Close price
- P&L
- Status (OPEN/CLOSED)

## 🔧 Advanced Usage

### Custom Timeframes

You can check any custom timeframe using the Python script directly:

```powershell
# Last 2 days (48 hours)
python get_trade_history.py 48

# Last 12 hours
python get_trade_history.py 12

# Last 30 days (720 hours)
python get_trade_history.py 720
```

### Export to JSON

To export data in JSON format for further analysis:

```powershell
# 24 hours to JSON
python get_trade_history.py 24 json > trades_24h.json

# 7 days to JSON
python get_trade_history.py 168 json > trades_7d.json
```

The JSON output can be:
- Imported into Excel/Google Sheets
- Analyzed with custom scripts
- Used in other data analysis tools

### Import JSON to Excel

1. Export to JSON: `python get_trade_history.py 168 json > trades_7d.json`
2. Open Excel
3. Go to Data → Get Data → From File → From JSON
4. Select your `trades_7d.json` file
5. Click "Into Table" to convert the data
6. Expand the columns and analyze

## 📍 Database Location

Trade data is stored in: `/workspace/data/trades.sqlite`

This SQLite database contains:
- **signals** table: All trading signals generated
- **trades** table: All trades executed with full lifecycle data

## 🔍 Understanding Trade Data

### Trade Status
- **SENT**: Trade order was sent to broker
- **OPEN**: Trade is currently open
- **CLOSED**: Trade has been closed

### Close Reasons
- **TP**: Take profit hit
- **SL**: Stop loss hit
- **TIME**: Time-based exit
- **MANUAL**: Manually closed

### Strategies/Engines
- **FARMER**: Fast scalping strategy (2 pip targets)
- **INTRADAY_LOW**: Low confidence intraday signals
- **INTRADAY_MED**: Medium confidence intraday signals
- **SWING_HIGH**: High confidence swing trades
- **ICT_SWING**: ICT swing point strategy
- **ICT_ATM**: ICT ATM method strategy
- **NYUPIP**: NY session pip harvesting strategy

## 💡 Tips

1. **Run Reports Regularly**: Check your performance daily or weekly
2. **Compare Strategies**: See which strategies work best for your account
3. **Track Improvement**: Watch your win rate and avg P&L over time
4. **Identify Patterns**: Look for times of day or market conditions where you perform best
5. **Export for Analysis**: Use JSON exports to create charts and deeper analysis

## ⚠️ Troubleshooting

### "Database not found"
- No trades have been recorded yet
- Make sure the bot has been running and placing trades
- Check that `/workspace/data/trades.sqlite` exists

### "Python not found"
- Install Python 3.7 or higher from https://www.python.org/
- Make sure Python is added to your system PATH

### Empty Results
- Check that trades were placed in the timeframe you're querying
- The bot may have been paused or not running
- Verify your config has `execution.enabled: true`

## 📧 Support

For issues or questions about the trade history analyzer, check:
1. The database exists: `/workspace/data/trades.sqlite`
2. Python is installed and in PATH
3. The bot has been running and placing trades
4. Your config has execution enabled

## 🔒 Data Privacy

All trade data is stored locally on your machine in the SQLite database. No data is sent to external servers.
