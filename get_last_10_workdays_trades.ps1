Write-Host "`n📊 Fetching last 10 workdays' trades..." -ForegroundColor Cyan

$daysToFetch = 10
$maxHours = ($daysToFetch + 2) * 24   # include buffer
$limit = 5000
$resp = Invoke-RestMethod "http://localhost:5000/api/recent_trades?hours=$maxHours&limit=$limit"

if ($null -eq $resp -or $null -eq $resp.trades -or $resp.trades.Count -eq 0) {
    Write-Host "❌ No trades returned from API" -ForegroundColor Red
    exit
}

function Get-RecentWorkdays($count) {
    $dates = @()
    $cursor = Get-Date
    while ($dates.Count -lt $count) {
        if ($cursor.DayOfWeek -ne 'Saturday' -and $cursor.DayOfWeek -ne 'Sunday') {
            $dates += $cursor.ToString('yyyy-MM-dd')
        }
        $cursor = $cursor.AddDays(-1)
    }
    return ($dates | Sort-Object)
}

$workdays = Get-RecentWorkdays -count $daysToFetch
$workdaySet = @{}
foreach ($d in $workdays) { $workdaySet[$d] = $true }

function Get-TradeDate($timestamp) {
    if ($null -eq $timestamp -or $timestamp -eq '') { return $null }
    if ($timestamp -match '^\s*(\d{4}-\d{2}-\d{2})') { return $matches[1] }
    return $null
}

function Get-TradePnl($trade) {
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
    return [pscustomobject]@{
        PnL = $pnl
        ClosePrice = $closePrice
    }
}

$tradesByDate = @{}
foreach ($t in $resp.trades) {
    $date = Get-TradeDate $t.timestamp
    if ($null -eq $date) { continue }
    if (-not $workdaySet.ContainsKey($date)) { continue }
    if (-not $tradesByDate.ContainsKey($date)) {
        $tradesByDate[$date] = @()
    }
    $tradesByDate[$date] += $t
}

if ($tradesByDate.Count -eq 0) {
    Write-Host "❌ No trades found for the last 10 workdays." -ForegroundColor Yellow
    exit
}

Write-Host "✅ Found trades for $($tradesByDate.Count) of the last 10 workdays.`n" -ForegroundColor Green

$engineTotals = @{}
$missingCloseOverall = 0

foreach ($date in $workdays) {
    if (-not $tradesByDate.ContainsKey($date)) {
        Write-Host ("-" * 80)
        Write-Host "$date — no trades" -ForegroundColor DarkGray
        continue
    }

    $dayTrades = $tradesByDate[$date]
    $missingClose = ($dayTrades | Where-Object { $_.status -eq 'CLOSED' -and ($null -eq $_.close_price -or $_.close_price -eq '' -or $_.close_price -eq '-') }).Count
    $missingCloseOverall += $missingClose

    Write-Host ("=" * 80) -ForegroundColor Cyan
    Write-Host "📅 $date" -ForegroundColor Cyan
    Write-Host ("=" * 80) -ForegroundColor Cyan
    Write-Host "Trades: $($dayTrades.Count)" -ForegroundColor White
    if ($missingClose -gt 0) {
        Write-Host "⚠️ $missingClose closed trade(s) missing close_price for this day." -ForegroundColor Yellow
    }

    $totalProfit = 0

    $byEngine = $dayTrades | Group-Object -Property engine
    foreach ($group in $byEngine | Sort-Object Name) {
        $engine = $group.Name
        $trades = $group.Group
        $closedTrades = $trades | Where-Object { $_.status -eq 'CLOSED' }
        $openTrades = $trades | Where-Object { $_.status -eq 'OPEN' }

        $profits = @()
        $wins = 0
        $losses = 0

        foreach ($trade in $closedTrades) {
            $calc = Get-TradePnl $trade
            if ($null -ne $calc.PnL) {
                $profits += $calc.PnL
                if ($calc.PnL -gt 0) { $wins++ }
                elseif ($calc.PnL -lt 0) { $losses++ }
            }
        }

        $totalPnL = ($profits | Measure-Object -Sum).Sum
        $avgPnL = if ($profits.Count -gt 0) { ($profits | Measure-Object -Average).Average } else { 0 }

        Write-Host ""
        Write-Host "🔹 Engine: $engine" -ForegroundColor Yellow
        Write-Host "   Trades: $($trades.Count) (Closed: $($closedTrades.Count), Open: $($openTrades.Count))" -ForegroundColor White
        Write-Host "   Wins: $wins | Losses: $losses | Win Rate: $(if ($closedTrades.Count -gt 0) { [math]::Round(100 * $wins / $closedTrades.Count, 1) } else { 0 })%" -ForegroundColor Gray
        Write-Host "   Total P&L: `$$([math]::Round($totalPnL, 2))" -ForegroundColor $(if ($totalPnL -ge 0) { "Green" } else { "Red" })
        Write-Host "   Avg P&L: `$$([math]::Round($avgPnL, 2))" -ForegroundColor Gray

        $totalProfit += $totalPnL

        if (-not $engineTotals.ContainsKey($engine)) {
            $engineTotals[$engine] = [pscustomobject]@{
                Trades = 0
                Closed = 0
                Wins = 0
                Losses = 0
                Profit = 0.0
            }
        }
        $engineTotals[$engine].Trades += $trades.Count
        $engineTotals[$engine].Closed += $closedTrades.Count
        $engineTotals[$engine].Wins += $wins
        $engineTotals[$engine].Losses += $losses
        $engineTotals[$engine].Profit += $totalPnL
    }

    Write-Host ""
    Write-Host "Day Total Profit: `$$([math]::Round($totalProfit, 2))" -ForegroundColor $(if ($totalProfit -ge 0) { "Green" } else { "Red" })
    Write-Host ""
}

Write-Host ("=" * 80) -ForegroundColor Cyan
Write-Host "🧮 10-Workday Engine Summary" -ForegroundColor Cyan
Write-Host ("=" * 80) -ForegroundColor Cyan

$engineTotals.GetEnumerator() | Sort-Object Key | ForEach-Object {
    $engine = $_.Key
    $data = $_.Value
    $winRate = if ($data.Closed -gt 0) { [math]::Round(100 * $data.Wins / $data.Closed, 1) } else { 0 }
    $avgPnL = if ($data.Closed -gt 0) { [math]::Round($data.Profit / $data.Closed, 2) } else { 0 }

    Write-Host "🔸 $engine" -ForegroundColor Yellow
    Write-Host "   Trades: $($data.Trades) (Closed: $($data.Closed))" -ForegroundColor White
    Write-Host "   Wins: $($data.Wins) | Losses: $($data.Losses) | Win Rate: $winRate%" -ForegroundColor Gray
    Write-Host "   Total P&L: `$$([math]::Round($data.Profit, 2))" -ForegroundColor $(if ($data.Profit -ge 0) { "Green" } else { "Red" })
    Write-Host "   Avg P&L per Closed Trade: `$$($avgPnL)" -ForegroundColor Gray
    Write-Host ""
}

if ($missingCloseOverall -gt 0) {
    Write-Host "⚠️ Note: $missingCloseOverall closed trade(s) across the period are missing close_price." -ForegroundColor Yellow
}

Write-Host "`nDone!`n" -ForegroundColor Green

