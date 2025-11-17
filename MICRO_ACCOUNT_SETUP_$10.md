# Micro Account Setup Guide for $10 USD Account

## Current Status
✅ **Good News:** The bot ALREADY has micro account support built-in!

The bot uses:
- **Micro lots (0.01 lots)** - supported via XAUUSDm symbol
- **Dynamic lot sizing** - calculates based on account equity
- **Risk-based position sizing** - scales to account size

---

## What NEEDS to be Modified for $10 Account

### 1. ⚠️ CRITICAL: Risk Per Trade Settings
**Current Config (Too High for $10):**
```json
"risk_percent_per_trade": 0.25   // 0.25% per trade
```

**Recommended for $10 Account:**
```json
"risk_percent_per_trade": 0.1    // 0.1% per trade = $0.01 risk per trade
```

**Why:** 
- At 0.25%, each losing trade = $0.025
- At 0.1%, each losing trade = $0.01
- You need to survive 10+ consecutive losses with a $10 account

---

### 2. ⚠️ CRITICAL: Loss Limiter Settings
**Current Config:**
```json
"loss_minimizer": {
  "soft_loss_dollars": 3.0,      // STOP after -$3 loss
  "max_loss_dollars": 11.0        // FORCE CLOSE at -$11 loss
}
```

**Recommended for $10 Account:**
```json
"loss_minimizer": {
  "soft_loss_dollars": 1.0,       // STOP after -$1 loss (10%)
  "max_loss_dollars": 2.0         // FORCE CLOSE at -$2 loss (20%)
}
```

**Why:** 
- With $10 account, -$3 = 30% drawdown
- -$11 = 110% (account blown)
- Recommended: Never risk >10-20% daily

---

### 3. ⚠️ HIGH IMPACT: Campaign Trade Limits
**Current Config:**
```json
"campaign_max_trades": {
  "LOW": 6,
  "MEDIUM": 6,
  "HIGH": 30,           // 30 trades per 5-min window!
  "HIGH_SWING": 30,
  "HIGH_ATM": 30
}
```

**Recommended for $10 Account:**
```json
"campaign_max_trades": {
  "LOW": 2,
  "MEDIUM": 2,
  "HIGH": 5,            // Max 5 trades per 5-min window
  "HIGH_SWING": 5,
  "HIGH_ATM": 5
}
```

**Why:**
- 30 trades with 0.1% risk = 3% total risk per window
- 5 trades with 0.1% risk = 0.5% risk per window (safer)
- Prevents account blowup from cascading losses

---

### 4. IMPORTANT: Lot Size Constraints
**Good News:** Already handled by broker minimum!

Exness MT5 XAUUSDm minimum lot:
- 0.01 lots = $1 per pip movement
- Already supports micro accounts ✅

**But verify in terminal:**
```
Account Balance: $10
Free Margin: $10
Min Lot: 0.01
Min Distance: 2 points
Risk per trade: 0.1% = $0.01
```

---

### 5. MEDIUM IMPACT: Farmer Settings
**Current Config:**
```json
"farmer": {
  "enabled": true,
  "tp_pips": 2,
  "sl_pips": 18,
  "trades_per_cycle": 3,
  "cycle_seconds": 30
}
```

**Recommended for $10 Account:**
```json
"farmer": {
  "enabled": true,
  "tp_pips": 2,
  "sl_pips": 18,
  "trades_per_cycle": 1,        // Only 1 trade per cycle instead of 3
  "cycle_seconds": 60            // Slower cycle (60s instead of 30s)
}
```

**Why:**
- 3 trades per 30s = aggressive for $10
- 1 trade per 60s = conservative, safer approach
- Still captures scalp opportunities

---

### 6. LOW IMPACT: Spread Filter
**Current Config:**
```json
"max_spread_points": 200        // Allows 200-point spread
```

**Status:** Already good for $10 - no change needed
- 200 points = $2.00 spread cost
- Acceptable for the symbol

---

## Complete Configuration for $10 Account

```json
{
  "broker": {
    "name": "Exness",
    "platform": "MT5",
    "server": "Exness-MT5Trial9",
    "symbol": "XAUUSDm"  
  },
  "risk": {
    "risk_percent_per_trade": 0.1,      // ✅ CHANGED: 0.25% → 0.1%
    "max_concurrent_trades": 1,
    "sl_min_atr": 0.5,
    "tp_atr_multipliers": [0.3, 0.6, 1.0],
    "move_sl_to_be_after_tp1": true,
    "symbol_caps": {
      "XAUUSDm": { "daily_loss_limit_pct": 10.0, "max_open_risk_pct": 2.0 }  // ✅ CHANGED
    }
  },
  "sessions": {
    "timezone": "Africa/Johannesburg",
    "trade_start": "08:00",
    "trade_end": "03:00",
    "days": ["Mon", "Tue", "Wed", "Thu", "Fri"]
  },
  "blackout": {
    "events": ["NFP", "CPI", "FOMC"],
    "buffer_minutes": 30,
    "source": "manual"
  },
  "filters": {
    "max_spread_points": 200,
    "min_tick_volume_ratio": 0.5,
    "consolidation_max_range_atr": 0.4,
    "min_atr_pips": 0
  },
  "data_feed": {
    "primary": "MT5",
    "backups": [],
    "startup_history": {
      "mt5_m1_bars": 7200,
      "min_rows": 4800,
      "hydrate_csv": null,
      "auto_cache": false
    },
    "history_limits": {
      "indicator_m1": 400,
      "nyupip_m1": 7200
    }
  },
  "execution": {
    "enabled": true,
    "demo_only": false,
    "slippage_points": 100,
    "deviation_points": 180,
    "campaign_window_minutes": 5,
    "min_seconds_between_entries": 10,
    "campaign_max_trades": {
      "LOW": 2,             // ✅ CHANGED: 6 → 2
      "MEDIUM": 2,          // ✅ CHANGED: 6 → 2
      "HIGH": 5,            // ✅ CHANGED: 30 → 5
      "HIGH_SWING": 5,      // ✅ CHANGED: 30 → 5
      "HIGH_ATM": 5         // ✅ CHANGED: 30 → 5
    },
    "max_position_minutes": {
      "LOW": 10,
      "MEDIUM": 10,
      "HIGH": 20
    },
    "high_tier_tp_pips": {
      "tier1_count": 1, 
      "tier1_pips": 4,
      "tier2_count": 0,
      "tier2_pips": 0
    },
    "low_tp_pips": 4,
    "medium_tp_primary_pips": 7,
    "farmer": {
      "enabled": true,
      "tp_pips": 2,
      "sl_pips": 18,
      "trades_per_cycle": 1,    // ✅ CHANGED: 3 → 1
      "cycle_seconds": 60,      // ✅ CHANGED: 30 → 60
      "dynamic_tp": true
    },
    "loss_minimizer": {
      "enabled": true,
      "soft_loss_dollars": 1.0,   // ✅ CHANGED: 3.0 → 1.0
      "max_loss_dollars": 2.0,    // ✅ CHANGED: 11.0 → 2.0
      "retrace_points": 10,
      "improvement_window_seconds": 20
    }
  },
  "notifications": {
    "telegram_enabled": false,
    "telegram_bot_token_env": "TELEGRAM_BOT_TOKEN",
    "telegram_chat_id_env": "TELEGRAM_CHAT_ID"
  },
  "logging": {
    "json_logs": true,
    "directory": "logs",
    "rotate_megabytes": 10,
    "retain_days": 7,
    "heartbeat_minutes": 5
  },
  "secrets_env": {
    "mt5_password_env": "MT5_PASSWORD"
  }
}
```

---

## Summary of Changes for $10 Account

| Setting | Original | Micro $10 | Reason |
|---------|----------|-----------|--------|
| Risk % per trade | 0.25% | 0.1% | Survival - smaller losses |
| Soft loss limit | $3.00 | $1.00 | Stop at 10% drawdown |
| Max loss limit | $11.00 | $2.00 | Prevent account blowup |
| LOW trades/window | 6 | 2 | Reduce cascading risk |
| MEDIUM trades/window | 6 | 2 | Reduce cascading risk |
| HIGH trades/window | 30 | 5 | Much safer scaling |
| Farmer trades/cycle | 3 | 1 | Slower scalping |
| Farmer cycle time | 30s | 60s | Less aggressive |

---

## Implementation Steps

1. **Backup current config:**
   ```bash
   cp config.json config.json.backup
   ```

2. **Update the 8 settings above in config.json**

3. **Verify the changes:**
   ```bash
   python3 -c "import json; print(json.load(open('config.json'))['risk']['risk_percent_per_trade'])"
   ```
   Should print: `0.1`

4. **Test with demo account first:**
   ```bash
   python start_live_signals.py
   ```
   Watch for lot sizing in the logs

5. **Monitor first few trades:**
   - Check that lots are 0.01-0.02 (micro lots)
   - Check that each trade risk is ~$0.01
   - Check that stops trigger at -$1 and -$2 as configured

---

## Expected Behavior with $10 Account

**With These Settings:**
- Average lot: 0.01-0.02 per trade
- Risk per trade: $0.01
- Risk per trading window: ~$0.05
- Daily soft stop: -$1.00 (10%)
- Daily hard stop: -$2.00 (20%)
- Farmer scalps: 1 per 60 seconds

**Realistic Outcomes:**
- ✅ Account survives 10+ consecutive losses
- ✅ Profits compound slowly but safely
- ✅ No catastrophic blowups
- ⚠️ Growth is slow (need consistency to reach $100)

---

## What NOT to Change

❌ **Don't modify these:**
- Symbol: Keep `XAUUSDm` (micro lots)
- Timezone: Keep `Africa/Johannesburg` (SAST)
- Minimum distance: Keep broker defaults
- Tick size: Keep broker defaults

**The bot handles all of these automatically!**

---

## Final Checklist

- [ ] Backup original config.json
- [ ] Update 8 settings as shown above
- [ ] Verify config.json syntax is valid JSON
- [ ] Test bot with demo account first
- [ ] Monitor first 10 trades for lot sizing
- [ ] Verify loss limiter triggers at correct levels
- [ ] Start with first real trade only after 100% confidence
- [ ] Track daily P&L and stop if -$2 is hit

---

**Bottom Line:** The bot IS micro account ready! Just need to dial down the risk settings. With these recommendations, your $10 account should be protected from blowup while still capturing profits from the SWING_HIGH strategy! 🎯
