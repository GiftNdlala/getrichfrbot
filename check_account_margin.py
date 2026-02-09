#!/usr/bin/env python3
"""
Check if your account has enough margin to trade XAUUSDm.
This will tell you definitively if you can trade with your current balance.
"""

import sys

try:
    import MetaTrader5 as mt5
except Exception:
    mt5 = None

from src.mt5_connector import MT5Connector

def check_margin():
    if mt5 is None:
        print("❌ MetaTrader5 module not installed. pip install MetaTrader5")
        sys.exit(1)
    
    # Initialize MT5
    conn = MT5Connector()
    if not conn.initialize():
        print("❌ MT5 initialize failed - ensure MT5 terminal is running and credentials are set")
        sys.exit(2)
    
    symbol = conn.symbol or "XAUUSDm"
    mt5.symbol_select(symbol, True)
    
    # Get account info
    acc = mt5.account_info()
    if not acc:
        print("❌ Could not get account info")
        sys.exit(3)
    
    # Get symbol info
    info = mt5.symbol_info(symbol)
    if not info:
        print(f"❌ Could not get symbol info for {symbol}")
        sys.exit(4)
    
    tick = mt5.symbol_info_tick(symbol)
    if not tick:
        print(f"❌ Could not get tick for {symbol}")
        sys.exit(5)
    
    # Account details
    balance = float(acc.balance)
    equity = float(acc.equity)
    margin_free = float(acc.margin_free)
    margin = float(acc.margin)
    leverage = acc.leverage
    
    print("\n" + "="*60)
    print("📊 ACCOUNT ANALYSIS")
    print("="*60)
    print(f"Account Type: {acc.trade_mode}")
    print(f"Balance: ${balance:.2f}")
    print(f"Equity: ${equity:.2f}")
    print(f"Free Margin: ${margin_free:.2f}")
    print(f"Used Margin: ${margin:.2f}")
    print(f"Leverage: 1:{leverage}")
    
    # Symbol details
    min_lot = float(info.volume_min)
    max_lot = float(info.volume_max)
    lot_step = float(info.volume_step)
    point = float(info.point)
    contract_size = float(getattr(info, 'trade_contract_size', 100))
    
    current_price = float(tick.ask or tick.bid)
    
    print("\n" + "="*60)
    print(f"📈 SYMBOL: {symbol}")
    print("="*60)
    print(f"Current Price: ${current_price:.2f}")
    print(f"Minimum Lot Size: {min_lot}")
    print(f"Maximum Lot Size: {max_lot}")
    print(f"Lot Step: {lot_step}")
    print(f"Contract Size: {contract_size}")
    
    # Check margin for minimum lot
    print("\n" + "="*60)
    print("💰 MARGIN ANALYSIS")
    print("="*60)
    
    # BUY order
    margin_buy = mt5.order_calc_margin(mt5.ORDER_TYPE_BUY, symbol, min_lot, current_price)
    # SELL order
    margin_sell = mt5.order_calc_margin(mt5.ORDER_TYPE_SELL, symbol, min_lot, current_price)
    
    if margin_buy is not None:
        margin_buy = float(margin_buy)
        can_afford_buy = margin_buy <= margin_free * 0.95
        print(f"Margin required for {min_lot} lots BUY: ${margin_buy:.2f}")
        if can_afford_buy:
            print(f"✅ CAN AFFORD BUY: ${margin_free:.2f} free margin > ${margin_buy:.2f} required")
        else:
            print(f"❌ CANNOT AFFORD BUY: Need ${margin_buy:.2f} but only have ${margin_free:.2f} free margin")
            shortfall = margin_buy - margin_free
            print(f"   Shortfall: ${shortfall:.2f}")
    
    if margin_sell is not None:
        margin_sell = float(margin_sell)
        can_afford_sell = margin_sell <= margin_free * 0.95
        print(f"Margin required for {min_lot} lots SELL: ${margin_sell:.2f}")
        if can_afford_sell:
            print(f"✅ CAN AFFORD SELL: ${margin_free:.2f} free margin > ${margin_sell:.2f} required")
        else:
            print(f"❌ CANNOT AFFORD SELL: Need ${margin_sell:.2f} but only have ${margin_free:.2f} free margin")
            shortfall = margin_sell - margin_free
            print(f"   Shortfall: ${shortfall:.2f}")
    
    # Try smaller lot if minimum doesn't fit
    if margin_buy is not None and margin_buy > margin_free:
        print("\n" + "="*60)
        print("🔍 CHECKING SMALLER POSITION SIZES")
        print("="*60)
        
        # Try 0.001 lots if that's possible
        test_lots = [0.001, 0.005] if lot_step <= 0.001 else []
        for test_lot in test_lots:
            if test_lot < min_lot:
                continue
            test_margin = mt5.order_calc_margin(mt5.ORDER_TYPE_BUY, symbol, test_lot, current_price)
            if test_margin is not None:
                test_margin = float(test_margin)
                if test_margin <= margin_free * 0.95:
                    print(f"✅ Could trade {test_lot} lots (requires ${test_margin:.2f} margin)")
                else:
                    print(f"❌ {test_lot} lots still too large (requires ${test_margin:.2f} margin)")
    
    # Final verdict
    print("\n" + "="*60)
    print("🎯 VERDICT")
    print("="*60)
    
    can_trade = False
    if margin_buy is not None and margin_buy <= margin_free * 0.95:
        can_trade = True
        print(f"✅ YES - Your bot CAN trade {symbol} with this account!")
        print(f"   You can open positions of {min_lot} lots or more")
    elif margin_buy is not None:
        print(f"❌ NO - Your bot CANNOT trade {symbol} with this account")
        print(f"   You need at least ${margin_buy:.2f} free margin")
        print(f"   But you only have ${margin_free:.2f} free margin")
        print(f"\n💡 RECOMMENDATION:")
        print(f"   - Switch to a cent account (may have lower margin requirements)")
        print(f"   - Or deposit more funds (need ${margin_buy - margin_free + 1:.2f} minimum)")
    else:
        print("❓ Could not calculate margin requirements")
    
    print("="*60 + "\n")
    
    return 0 if can_trade else 1

if __name__ == "__main__":
    sys.exit(check_margin())
