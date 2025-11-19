#!/usr/bin/env python3
"""
Quick configuration updater for $10 micro account setup
This script safely updates the config.json with recommended settings for small accounts
"""

import json
import shutil
from datetime import datetime
from pathlib import Path

def backup_config(config_path="config.json"):
    """Create a timestamped backup of config.json"""
    backup_path = f"config.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    shutil.copy(config_path, backup_path)
    print(f"✅ Backup created: {backup_path}")
    return backup_path

def update_config_for_micro(config_path="config.json", account_size=10):
    """Update config for micro account trading"""
    
    # Load current config
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Calculate adjustments based on account size
    if account_size <= 10:
        risk_percent = 0.1
        soft_loss = 1.0
        max_loss = 2.0
        campaign_trades = 5
        farmer_trades = 1
        farmer_cycle = 60
        daily_loss_limit = 10.0
        max_open_risk = 2.0
    elif account_size <= 50:
        risk_percent = 0.15
        soft_loss = 2.5
        max_loss = 5.0
        campaign_trades = 8
        farmer_trades = 2
        farmer_cycle = 45
        daily_loss_limit = 15.0
        max_open_risk = 3.0
    else:  # >= $100
        risk_percent = 0.25  # Keep original
        soft_loss = 3.0
        max_loss = 11.0
        campaign_trades = 30
        farmer_trades = 3
        farmer_cycle = 30
        daily_loss_limit = 90.0
        max_open_risk = 5.0
    
    # Update settings
    print(f"\n📊 Updating config.json for ${account_size} micro account...")
    print("=" * 60)
    
    # Risk settings
    old_risk = config['risk']['risk_percent_per_trade']
    config['risk']['risk_percent_per_trade'] = risk_percent
    print(f"✏️  Risk per trade: {old_risk}% → {risk_percent}%")
    
    # Symbol caps
    old_daily = config['risk']['symbol_caps']['XAUUSDm']['daily_loss_limit_pct']
    old_max_open = config['risk']['symbol_caps']['XAUUSDm']['max_open_risk_pct']
    config['risk']['symbol_caps']['XAUUSDm']['daily_loss_limit_pct'] = daily_loss_limit
    config['risk']['symbol_caps']['XAUUSDm']['max_open_risk_pct'] = max_open_risk
    print(f"✏️  Daily loss limit: {old_daily}% → {daily_loss_limit}%")
    print(f"✏️  Max open risk: {old_max_open}% → {max_open_risk}%")
    
    # Campaign trades
    for level in ['LOW', 'MEDIUM', 'HIGH', 'HIGH_SWING', 'HIGH_ATM']:
        old_val = config['execution']['campaign_max_trades'][level]
        if level in ['LOW', 'MEDIUM']:
            config['execution']['campaign_max_trades'][level] = 2
        else:
            config['execution']['campaign_max_trades'][level] = campaign_trades
        if old_val != config['execution']['campaign_max_trades'][level]:
            print(f"✏️  {level} trades per window: {old_val} → {config['execution']['campaign_max_trades'][level]}")
    
    # Loss minimizer
    old_soft = config['execution']['loss_minimizer']['soft_loss_dollars']
    old_max = config['execution']['loss_minimizer']['max_loss_dollars']
    config['execution']['loss_minimizer']['soft_loss_dollars'] = soft_loss
    config['execution']['loss_minimizer']['max_loss_dollars'] = max_loss
    print(f"✏️  Soft loss limit: ${old_soft} → ${soft_loss}")
    print(f"✏️  Max loss limit: ${old_max} → ${max_loss}")
    
    # Farmer settings
    old_farmer_trades = config['execution']['farmer']['trades_per_cycle']
    old_farmer_cycle = config['execution']['farmer']['cycle_seconds']
    config['execution']['farmer']['trades_per_cycle'] = farmer_trades
    config['execution']['farmer']['cycle_seconds'] = farmer_cycle
    print(f"✏️  Farmer trades/cycle: {old_farmer_trades} → {farmer_trades}")
    print(f"✏️  Farmer cycle time: {old_farmer_cycle}s → {farmer_cycle}s")
    
    print("=" * 60)
    
    # Save updated config
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Config updated successfully!")
    print(f"📁 File: {config_path}")
    return config

def validate_config(config_path="config.json"):
    """Validate the updated config"""
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    print("\n🔍 Validating configuration...")
    print("=" * 60)
    
    checks = [
        ("Symbol", config['broker']['symbol'], "XAUUSDm"),
        ("Risk %", config['risk']['risk_percent_per_trade'], 0.1),
        ("Soft loss", config['execution']['loss_minimizer']['soft_loss_dollars'], 1.0),
        ("Max loss", config['execution']['loss_minimizer']['max_loss_dollars'], 2.0),
        ("HIGH trades", config['execution']['campaign_max_trades']['HIGH'], 5),
        ("Farmer trades", config['execution']['farmer']['trades_per_cycle'], 1),
        ("Farmer cycle", config['execution']['farmer']['cycle_seconds'], 60),
    ]
    
    all_pass = True
    for name, actual, expected in checks:
        status = "✅" if actual == expected else "⚠️"
        print(f"{status} {name}: {actual} (expected: {expected})")
        if actual != expected:
            all_pass = False
    
    print("=" * 60)
    return all_pass

if __name__ == "__main__":
    import sys
    
    account_size = 10  # Default
    if len(sys.argv) > 1:
        try:
            account_size = float(sys.argv[1])
        except ValueError:
            print(f"Invalid account size: {sys.argv[1]}")
            sys.exit(1)
    
    # Backup config
    backup_config()
    
    # Update config
    update_config_for_micro(account_size=account_size)
    
    # Validate
    if validate_config():
        print("\n✅ All settings validated! Ready to trade on $10 account.")
    else:
        print("\n⚠️ Some settings need attention. Check the values above.")
    
    print("\n📖 See MICRO_ACCOUNT_SETUP_$10.md for detailed information.")
