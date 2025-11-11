# Get Trades - Last 7 Days
# Retrieves and analyzes all trades from the last 7 days (168 hours)
# Can be run standalone without the Flask dashboard

Write-Host "`n🚀 Get Rich FR Bot - Trade History Analyzer" -ForegroundColor Cyan
Write-Host "📅 Retrieving trades from the last 7 days...`n" -ForegroundColor Yellow

# Check if Python is available
$pythonCmd = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $pythonCmd = "python3"
} else {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "   Please install Python 3.7+ from https://www.python.org/" -ForegroundColor Yellow
    exit 1
}

# Check if the script exists
$scriptPath = Join-Path $PSScriptRoot "get_trade_history.py"
if (-not (Test-Path $scriptPath)) {
    Write-Host "❌ Script not found: $scriptPath" -ForegroundColor Red
    exit 1
}

# Run the Python script for 7 days (168 hours)
try {
    & $pythonCmd $scriptPath 168 text
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "`n⚠️ Script exited with code $LASTEXITCODE" -ForegroundColor Yellow
    } else {
        Write-Host "✅ Report generated successfully!" -ForegroundColor Green
    }
} catch {
    Write-Host "`n❌ Error running script: $_" -ForegroundColor Red
    exit 1
}

Write-Host "`n💡 TIP: You can also:" -ForegroundColor Cyan
Write-Host "   • Export to JSON: $pythonCmd get_trade_history.py 168 json > trades_7d.json" -ForegroundColor Gray
Write-Host "   • Check custom timeframes: $pythonCmd get_trade_history.py 48 text (for 2 days)`n" -ForegroundColor Gray
