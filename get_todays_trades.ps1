# Get Today's Trades by Strategy
Write-Host ""
Write-Host -ForegroundColor Cyan "Fetching today's trades..."

$today = Get-Date -Format "yyyy-MM-dd"
$todayStart = "$today 00:00:00"
$divider = "=" * 80

$resp = Invoke-RestMethod "http://localhost:5000/api/recent_trades?hours=24&limit=2000"

if ($null -eq $resp -or $null -eq $resp.trades -or $resp.trades.Count -eq 0) {
    Write-Host -ForegroundColor Red "No trades found in the last 24 hours"
    exit
}

$todaysTrades = $resp.trades | Where-Object {
    $rawTs = $_.timestamp
    if ($null -eq $rawTs -or $rawTs -eq "") { return $false }
    if ($rawTs -match "^\s*(\d{4}-\d{2}-\d{2})") {
        return $matches[1] -eq $today
    }
    return $false
}

if ($todaysTrades.Count -eq 0) {
    Write-Host -ForegroundColor Yellow "No trades found for today ($today)"
    Write-Host -ForegroundColor Gray "Total trades in last 24h: $($resp.trades.Count)"
    exit
}

Write-Host -ForegroundColor Green "Found $($todaysTrades.Count) trades for today ($today)"
Write-Host ""

$byStrategy = $todaysTrades | Group-Object -Property engine

Write-Host -ForegroundColor Cyan $divider
Write-Host -ForegroundColor Cyan "TODAY'S TRADES BY STRATEGY"
Write-Host -ForegroundColor Cyan $divider
Write-Host ""

$totalProfit = 0
$totalTrades = 0

foreach ($group in $byStrategy | Sort-Object Name) {

    $strategy = $group.Name
    $trades = $group.Group
    $count = $trades.Count
    
    Write-Host -ForegroundColor Yellow "Strategy: $strategy"
    Write-Host -ForegroundColor White "   Total Trades: $count"
    
    $closedTrades = $trades | Where-Object { $_.status -eq "CLOSED" }
    $openTrades   = $trades | Where-Object { $_.status -eq "OPEN" }

    if ($closedTrades.Count -gt 0) {
        $profits = @()
        $wins = 0
        $losses = 0
        
        foreach ($trade in $closedTrades) {
            $pnl = $null
            $closePrice = $null

            if ($trade.close_price -notin @($null, "", "-")) {
                $closePrice = [double]$trade.close_price
            }

            if ($trade.pnl -notin @($null, "", "-")) {
                $pnl = [double]$trade.pnl
            }
            elseif ($null -ne $closePrice) {
                $dir = [int]$trade.direction
                $entry = [double]$trade.entry
                $lots = if ($trade.lots -notin @($null, "")) { [double]$trade.lots } else { 0.01 }

                if ($dir -eq 1) { $pnl = ($closePrice - $entry) * $lots * 100 }
                else { $pnl = ($entry - $closePrice) * $lots * 100 }
            }

            if ($null -ne $pnl) {
                $profits += $pnl
                if ($pnl -gt 0) { $wins++ } elseif ($pnl -lt 0) { $losses++ }
            }
        }

        $totalPnL = ($profits | Measure-Object -Sum).Sum
        $avgPnL   = if ($profits.Count -gt 0) { ($profits | Measure-Object -Average).Average } else { 0 }
        $winRate  = if ($closedTrades.Count -gt 0) { [math]::Round(100 * $wins / $closedTrades.Count, 1) } else { 0 }

        $color = if ($winRate -ge 50) { "Green" } else { "Red" }
        Write-Host -ForegroundColor $color "   Closed: $($closedTrades.Count) | Wins: $wins | Losses: $losses | Win Rate: $winRate%"

        $pnlColor = if ($totalPnL -ge 0) { "Green" } else { "Red" }
        Write-Host -ForegroundColor $pnlColor ("   Total PL: $" + [math]::Round($totalPnL, 2))
        Write-Host -ForegroundColor Gray ("   Avg PL: $" + [math]::Round($avgPnL, 2))

        $totalProfit += $totalPnL
    }

    if ($openTrades.Count -gt 0) {
        Write-Host -ForegroundColor Cyan "   Open: $($openTrades.Count)"
    }
    
    Write-Host ""
    $totalTrades += $count
}

Write-Host -ForegroundColor Cyan $divider
Write-Host -ForegroundColor Cyan "SUMMARY"
Write-Host -ForegroundColor Cyan $divider

Write-Host -ForegroundColor White "Total Trades Today: $totalTrades"
$col = if ($totalProfit -ge 0) { "Green" } else { "Red" }
Write-Host -ForegroundColor $col ("Total Profit Today: $" + [math]::Round($totalProfit, 2))
Write-Host ""

Write-Host "Done."
