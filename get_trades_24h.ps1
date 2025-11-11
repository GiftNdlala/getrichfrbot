# Get Trades - Last 24 Hours
# Retrieves and analyzes all trades from the last 24 hours
# Can be run standalone without the Flask dashboard

Write-Host "`n🚀 Get Rich FR Bot - Trade History Analyzer" -ForegroundColor Cyan
Write-Host "📅 Retrieving trades from the last 24 hours...`n" -ForegroundColor Yellow

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

# Run the Python script
try {
    & $pythonCmd $scriptPath 24 text
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "`n⚠️ Script exited with code $LASTEXITCODE" -ForegroundColor Yellow
    } else {
        Write-Host "✅ Report generated successfully!" -ForegroundColor Green
    }
} catch {
    Write-Host "`n❌ Error running script: $_" -ForegroundColor Red
    exit 1
}

Write-Host "`n💡 TIP: You can also export to JSON format by running:" -ForegroundColor Cyan
Write-Host "   $pythonCmd get_trade_history.py 24 json > trades_24h.json`n" -ForegroundColor Gray
