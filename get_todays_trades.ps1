# Get Today's Trades by Strategy
# Copy and paste this entire script into PowerShell

Write-Host "`n📊 Fetching today's trades..." -ForegroundColor Cyan

# Get today's date in UTC (for filtering)
$today = Get-Date -Format "yyyy-MM-dd"
$todayStart = "$today 00:00:00"

# Fetch trades from last 24 hours (to ensure we get all of today)
$resp = Invoke-RestMethod "http://localhost:5000/api/recent_trades?hours=24&limit=2000"

if ($null -eq $resp -or $null -eq $resp.trades -or $resp.trades.Count -eq 0) {
    Write-Host "❌ No trades found in the last 24 hours" -ForegroundColor Red
    exit
}

# Filter for today's trades (support ISO strings with timezone)
$todaysTrades = $resp.trades | Where-Object {
    $rawTs = $_.timestamp
    if ($null -eq $rawTs -or $rawTs -eq '') {
        return $false
    }
    if ($rawTs -match '^\s*(\d{4}-\d{2}-\d{2})') {
        $tradeDate = $matches[1]
        return $tradeDate -eq $today
    }
    $false
}

if ($todaysTrades.Count -eq 0) {
    Write-Host "❌ No trades found for today ($today)" -ForegroundColor Yellow
    Write-Host "Total trades in last 24h: $($resp.trades.Count)" -ForegroundColor Gray
    exit
}

Write-Host "✅ Found $($todaysTrades.Count) trades for today ($today)`n" -ForegroundColor Green

# Group by strategy/engine
$byStrategy = $todaysTrades | Group-Object -Property engine

Write-Host ("=" * 80) -ForegroundColor Cyan
Write-Host "📈 TODAY'S TRADES BY STRATEGY" -ForegroundColor Cyan
Write-Host ("=" * 80) -ForegroundColor Cyan
Write-Host ""

# Process each strategy
$totalProfit = 0
$totalTrades = 0

foreach ($group in $byStrategy | Sort-Object Name) {
    $strategy = $group.Name
    $trades = $group.Group
    $count = $trades.Count
    
    Write-Host "🔹 Strategy: $strategy" -ForegroundColor Yellow
    Write-Host "   Total Trades: $count" -ForegroundColor White
    
    # Calculate profit/loss
    $closedTrades = $trades | Where-Object { $_.status -eq 'CLOSED' }
    $openTrades = $trades | Where-Object { $_.status -eq 'OPEN' }
    
    if ($closedTrades.Count -gt 0) {
        # Calculate PnL for closed trades
        $profits = @()
        $wins = 0
        $losses = 0
        
        foreach ($trade in $closedTrades) {
            $pnl = $null
            $closePrice = $null
            if ($null -ne $trade.close_price -and $trade.close_price -ne '' -and $trade.close_price -ne '-') {
                $closePrice = [double]$trade.close_price
            }

            if ($null -ne $trade.pnl -and $trade.pnl -ne '' -and $trade.pnl -ne '-') {
                $pnl = [double]$trade.pnl
            } elseif ($null -ne $closePrice) {
                $dir = [int]$trade.direction
                $entry = [double]$trade.entry
                $lots = if ($null -ne $trade.lots -and $trade.lots -ne '') { [double]$trade.lots } else { 0.01 }
                if ($dir -eq 1) {
                    $pnl = ($closePrice - $entry) * $lots * 100
                } else {
                    $pnl = ($entry - $closePrice) * $lots * 100
                }
            }

            if ($null -ne $pnl) {
                $profits += $pnl
                if ($pnl -gt 0) { $wins++ }
                elseif ($pnl -lt 0) { $losses++ }
            }
        }
        
        $totalPnL = ($profits | Measure-Object -Sum).Sum
        $avgPnL = if ($profits.Count -gt 0) { ($profits | Measure-Object -Average).Average } else { 0 }
        $winRate = if ($closedTrades.Count -gt 0) { [math]::Round(100 * $wins / $closedTrades.Count, 1) } else { 0 }
        
        Write-Host "   Closed: $($closedTrades.Count) | Wins: $wins | Losses: $losses | Win Rate: $winRate%" -ForegroundColor $(if ($winRate -ge 50) { "Green" } else { "Red" })
        Write-Host "   Total P&L: `$$([math]::Round($totalPnL, 2))" -ForegroundColor $(if ($totalPnL -ge 0) { "Green" } else { "Red" })
        Write-Host "   Avg P&L: `$$([math]::Round($avgPnL, 2))" -ForegroundColor Gray
        
        $totalProfit += $totalPnL
    }
    
    if ($openTrades.Count -gt 0) {
        Write-Host "   Open: $($openTrades.Count)" -ForegroundColor Cyan
    }
    
    Write-Host ""
    $totalTrades += $count
}

Write-Host ("=" * 80) -ForegroundColor Cyan
Write-Host "📊 SUMMARY" -ForegroundColor Cyan
Write-Host ("=" * 80) -ForegroundColor Cyan
Write-Host "Total Trades Today: $totalTrades" -ForegroundColor White
Write-Host "Total Profit Today: `$$([math]::Round($totalProfit, 2))" -ForegroundColor $(if ($totalProfit -ge 0) { "Green" } else { "Red" })
Write-Host ""

# Flag trades missing close price data
$missingClose = $todaysTrades | Where-Object { $_.status -eq 'CLOSED' -and ($null -eq $_.close_price -or $_.close_price -eq '' -or $_.close_price -eq '-') }
if ($missingClose.Count -gt 0) {
    Write-Host "⚠️ $($missingClose.Count) closed trade(s) missing close_price. Using stored PnL values where available." -ForegroundColor Yellow
    Write-Host ""
}

# Show detailed trade list with calculated P&L
Write-Host "`n📋 Detailed Trade List:" -ForegroundColor Cyan
$todaysTrades | ForEach-Object {
    $trade = $_
    $dir = [int]$trade.direction
    $entry = [double]$trade.entry
    $lots = if ($null -ne $trade.lots -and $trade.lots -ne '') { [double]$trade.lots } else { 0.01 }
    
    # Calculate effective close and P&L
    $effectiveClose = $null
    $pnl = $null
    
    if ($trade.status -eq 'CLOSED') {
        if ($null -ne $trade.close_price -and $trade.close_price -ne '' -and $trade.close_price -ne '-') {
            $effectiveClose = [double]$trade.close_price
        }
        if ($null -ne $trade.pnl -and $trade.pnl -ne '' -and $trade.pnl -ne '-') {
            $pnl = [double]$trade.pnl
        } elseif ($null -ne $effectiveClose) {
            if ($dir -eq 1) {
                $pnl = ($effectiveClose - $entry) * $lots * 100
            } else {
                $pnl = ($entry - $effectiveClose) * $lots * 100
            }
        }
    }
    
    [PSCustomObject]@{
        Time = $trade.timestamp
        Strategy = $trade.engine
        Direction = if ($dir -eq 1) {'BUY'} else {'SELL'}
        Entry = [math]::Round($entry, 2)
        Close = if ($null -ne $effectiveClose) {[math]::Round($effectiveClose, 2)} else {'-'}
        Status = $trade.status
        PnL = if ($null -ne $pnl) {"`$$([math]::Round($pnl, 2))"} else {'-'}
        Ticket = $trade.ticket
    }
} | Format-Table -AutoSize

# Calculate final summary from detailed list
Write-Host "`n💰 FINAL SUMMARY" -ForegroundColor Cyan
Write-Host ("=" * 80) -ForegroundColor Cyan

$allPnL = @()
$allWins = 0
$allLosses = 0

$todaysTrades | ForEach-Object {
    $trade = $_
    if ($trade.status -eq 'CLOSED') {
        $dir = [int]$trade.direction
        $entry = [double]$trade.entry
        $lots = if ($null -ne $trade.lots -and $trade.lots -ne '') { [double]$trade.lots } else { 0.01 }
        
        $closePrice = $null
        if ($null -ne $trade.close_price -and $trade.close_price -ne '' -and $trade.close_price -ne '-') {
            $closePrice = [double]$trade.close_price
        }

        $pnl = $null
        if ($null -ne $trade.pnl -and $trade.pnl -ne '' -and $trade.pnl -ne '-') {
            $pnl = [double]$trade.pnl
        } elseif ($null -ne $closePrice) {
            if ($dir -eq 1) {
                $pnl = ($closePrice - $entry) * $lots * 100
            } else {
                $pnl = ($entry - $closePrice) * $lots * 100
            }
        }

        if ($null -ne $pnl) {
            $allPnL += $pnl
            if ($pnl -gt 0) { $allWins++ }
            elseif ($pnl -lt 0) { $allLosses++ }
        }
    }
}

$grandTotal = ($allPnL | Measure-Object -Sum).Sum
$avgPnL = if ($allPnL.Count -gt 0) { ($allPnL | Measure-Object -Average).Average } else { 0 }
$totalTrades = $allWins + $allLosses
$winRate = if ($totalTrades -gt 0) { [math]::Round(100 * $allWins / $totalTrades, 1) } else { 0 }

Write-Host "Total Closed Trades: $totalTrades" -ForegroundColor White
Write-Host "Wins: $allWins" -ForegroundColor Green
Write-Host "Losses: $allLosses" -ForegroundColor Red
Write-Host "Win Rate: $winRate%" -ForegroundColor $(if ($winRate -ge 50) { "Green" } else { "Yellow" })
Write-Host "Average PnL per Trade: `$$([math]::Round($avgPnL, 2))" -ForegroundColor Gray
Write-Host ("=" * 80) -ForegroundColor Cyan
Write-Host "TOTAL PROFIT TODAY: `$$([math]::Round($grandTotal, 2))" -ForegroundColor $(if ($grandTotal -ge 0) { "Green" } else { "Red" })
Write-Host ("=" * 80) -ForegroundColor Cyan

Write-Host ""
Write-Host 'Done!' -ForegroundColor Green
Write-Host ""
