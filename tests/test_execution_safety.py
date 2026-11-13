import copy
import time
import unittest
from datetime import datetime, timezone
from types import SimpleNamespace as NS
from unittest.mock import patch

from src.executor import AutoTrader
from src.risk_controls import execution_snapshot, floor_volume, news_reason, ACKNOWLEDGED_ORDERS


class Broker:
    ACCOUNT_TRADE_MODE_DEMO = 0
    ORDER_TYPE_BUY = 0
    ORDER_TYPE_SELL = 1
    ORDER_FILLING_IOC = 1
    TRADE_ACTION_DEAL = 1
    TRADE_RETCODE_DONE = 10009

    def __init__(self):
        self.info = NS(point=.01, trade_tick_size=.01, digits=2, volume_min=.01, volume_step=.01, volume_max=10, trade_stops_level=0)
        self.account = NS(login=1, balance=1000., equity=1000., margin_free=1000., trade_mode=0, currency='USD')
        self.tick = NS(bid=100., ask=100.02, time=time.time())
        self.positions, self.orders, self.deals, self.sent = [], [], [], []

    def symbol_info(self, symbol): return self.info
    def symbol_info_tick(self, symbol): return self.tick
    def account_info(self): return self.account
    def positions_get(self): return self.positions
    def orders_get(self): return self.orders
    def history_deals_get(self, *args, **kwargs): return self.deals
    def order_calc_margin(self, side, symbol, lots, price): return lots * 100
    def order_calc_profit(self, side, symbol, lots, entry, close): return (close-entry) * (1 if side == 0 else -1) * lots * 100
    def order_send(self, request):
        self.sent.append(request)
        return NS(retcode=10009, order=123, deal=456, price=request['price'])


class ExecutionSafetyTests(unittest.TestCase):
    def setUp(self):
        ACKNOWLEDGED_ORDERS.clear()
        self.api = Broker()
        self.cfg = {
            'broker': {'login': 1}, 'news': {'enabled': False},
            'filters': {'max_spread_points': 40},
            'risk': {'risk_percent_per_trade': .25, 'max_concurrent_trades': 1, 'max_open_risk_pct': .5, 'daily_loss_limit_pct': 2},
            'execution': {'enabled': True, 'demo_only': True, 'farmer': {
                'target_profit_dollars': 2, 'max_loss_dollars': 2,
                'risk_percent_per_trade': .1, 'estimated_round_trip_cost_dollars': .15,
            }},
        }
        self.context = {'source': 'MT5', 'history_ready': True, 'audit_ready': True, 'timestamp': datetime.now(timezone.utc)}
        self.trader = AutoTrader.__new__(AutoTrader)
        self.trader.cfg, self.trader.symbol, self.trader.enabled = self.cfg, 'XAUUSDm', True
        self.trader.market_context = self.context

    def order(self, side=1, sl=99., tp=103., tag='TEST'):
        with patch('src.executor.mt5', self.api):
            return self.trader.place_market_order(side, 100., sl, tp, tag)

    def blocked(self, reason, **kwargs):
        self.assertIsNone(self.order(**kwargs))
        self.assertIn(reason, self.trader.last_rejection)
        self.assertEqual(self.api.sent, [])

    def test_sizes_at_actual_market_entry(self):
        trade = self.order()
        self.assertIsNotNone(trade)
        r = self.api.sent[0]
        risk = -self.api.order_calc_profit(r['type'], r['symbol'], r['volume'], r['price'], r['sl'])
        self.assertLessEqual(risk, 2.5)
        self.assertEqual(r['price'], 100.02)

    def test_minimum_lot_is_rejected_instead_of_rounded_up(self): self.blocked('MINIMUM_LOT_EXCEEDS_RISK', sl=90.)
    def test_real_account_blocked(self):
        self.api.account.trade_mode = 2
        self.blocked('DEMO_ACCOUNT_REQUIRED')
    def test_wrong_account_blocked(self):
        self.api.account.login = 99
        self.blocked('ACCOUNT_MISMATCH')
    def test_synthetic_source_blocked(self):
        self.context['source'] = 'Realistic Mock'
        self.blocked('BROKER_DATA_REQUIRED')
    def test_missing_history_blocks_order(self):
        self.context['history_ready'] = False
        self.blocked('BROKER_DATA_REQUIRED')
    def test_stale_broker_tick_blocked(self):
        self.api.tick.time -= 60
        self.blocked('QUOTE_STALE')
    def test_stale_signal_quote_blocked(self):
        self.context['timestamp'] = self.api.tick.time - 60
        self.blocked('QUOTE_STALE')
    def test_spread_is_rechecked_at_submission(self):
        self.api.tick.ask = 101
        self.blocked('SPREAD_CAP')
    def test_positions_read_failure_blocks(self):
        self.api.positions = None
        self.blocked('EXPOSURE_UNAVAILABLE')
    def test_pending_orders_read_failure_blocks(self):
        self.api.orders = None
        self.blocked('EXPOSURE_UNAVAILABLE')
    def test_existing_other_engine_or_manual_position_blocks(self):
        self.api.positions = [NS(ticket=999, magic=0)]
        self.blocked('POSITION_CAP')
    def test_pending_order_reserves_capacity(self):
        self.api.orders = [NS()]
        self.blocked('POSITION_CAP')
    def test_floating_daily_loss_blocks(self):
        self.api.account.equity = 979
        self.blocked('DAILY_LOSS_CAP')
    def test_daily_history_read_failure_blocks(self):
        self.api.deals = None
        self.blocked('DAILY_HISTORY_UNAVAILABLE')
    def test_commission_is_in_daily_loss(self):
        self.api.account.balance = self.api.account.equity = 979
        self.api.deals = [NS(profit=-19, commission=-2)]
        self.blocked('DAILY_LOSS_CAP')
    def test_defense_tier_reduces_size(self):
        self.cfg['risk']['progressive_defense'] = {'enabled': True, 'loss_tiers': [{'realized_loss_pct': 1, 'position_size_mult': .5}]}
        self.api.account.balance = self.api.account.equity = 989
        self.api.deals = [NS(profit=-11)]
        self.assertEqual(self.order()['volume'], .01)
    def test_no_unknown_news_coverage(self):
        self.cfg['news'] = {'enabled': True, 'calendar_file': 'missing-calendar-for-test.json'}
        self.blocked('NEWS_CALENDAR_UNAVAILABLE')
    def test_farmer_target_is_account_dollars_after_sizing(self):
        trade = self.order(sl=99.2, tag='FARMER')
        self.assertIsNotNone(trade)
        gross = self.api.order_calc_profit(0, 'XAUUSDm', trade['volume'], trade['price'], trade['tp'])
        self.assertGreaterEqual(gross + 1e-8, 2.15)
        self.assertLessEqual(-self.api.order_calc_profit(0, 'XAUUSDm', trade['volume'], trade['price'], trade['sl']) + .15, 1.)
    def test_farmer_requires_live_currency_conversion(self):
        self.api.account.currency = 'ZAR'
        self.blocked('USD_CONVERSION_UNAVAILABLE:ZAR', tag='FARMER')
    def test_failed_signal_persistence_blocks_order(self):
        self.context['audit_ready'] = False
        self.blocked('AUDIT_STORAGE_REQUIRED')
    def test_relative_spread_spike_blocks_order(self):
        self.context['normal_spread_points'] = .5
        self.blocked('SPREAD_SPIKE')
    def test_broker_stop_constraints_do_not_silently_widen_risk(self):
        self.api.info.trade_stops_level = 500
        self.blocked('STOP_TOO_CLOSE')
    def test_session_gate_applies_to_event_orders_too(self):
        self.cfg['sessions'] = {'timezone':'UTC','trade_start':'00:00','trade_end':'23:59','days':[]}
        self.blocked('OUTSIDE_SESSION',tag='EVENT')
    def test_no_additional_risk_with_unprotected_existing_position(self):
        self.cfg['risk']['max_concurrent_trades'] = 3
        self.api.positions = [NS(ticket=999,sl=0)]
        self.blocked('UNPROTECTED_POSITION')
    def test_first_day_demo_deposit_is_not_trading_profit(self):
        self.api.deals = [NS(type=2,profit=1000)]
        self.assertIsNotNone(self.order())
    def test_unknown_account_balance_is_rejected(self):
        self.api.account.balance = float('nan')
        self.blocked('DAILY_BASELINE_INVALID')
    def test_final_quote_movement_rechecks_risk_and_entry(self):
        first = NS(**vars(self.api.tick))
        final = NS(**dict(vars(self.api.tick),ask=100.03,bid=100.01))
        calls = iter([first,final])
        self.api.symbol_info_tick = lambda symbol: next(calls)
        self.assertEqual(self.order()['price'],100.03)
    def test_large_final_quote_drift_does_not_submit(self):
        first = NS(**vars(self.api.tick))
        final = NS(**dict(vars(self.api.tick),ask=101.02,bid=101.))
        calls = iter([first,final])
        self.api.symbol_info_tick = lambda symbol: next(calls)
        self.blocked('QUOTE_MOVED_DURING_CHECKS')
    def test_nonfinite_order_blocked(self): self.blocked('INVALID_ORDER_LEVELS', sl=float('nan'))
    def test_sell_risk_and_target_sides(self):
        self.assertIsNotNone(self.order(side=-1, sl=101., tp=97.))
    def test_volume_floor_does_not_round_up(self):
        self.assertEqual(floor_volume(.009, self.api.info), 0)
        self.assertEqual(floor_volume(.019, self.api.info), .01)

    def test_acknowledged_order_reserves_slot_before_position_visibility(self):
        self.assertIsNotNone(self.order())
        with patch('src.executor.mt5', self.api):
            self.assertIsNone(self.trader.place_market_order(1, 100., 99., 103., 'OTHER_ENGINE'))
        self.assertEqual(len(self.api.sent), 1)
        self.assertIn('POSITION_CAP', self.trader.last_rejection)

    def test_farmer_daily_loss_includes_previous_day_entry(self):
        self.cfg['execution']['farmer']['cooldown_seconds'] = 0
        exit_deal = NS(position_id=12, entry=1, profit=-6, magic=20250923, comment='[sl]', time=time.time()-300)
        opening = NS(position_id=12, entry=0, profit=0, magic=20250923, comment='GetRichFR_FARMER', time=time.time()-90000)
        self.api.history_deals_get = lambda *a, **kw: [opening, exit_deal] if kw else [exit_deal]
        self.blocked('FARMER_DAILY_LOSS_CAP', tag='FARMER')


if __name__ == '__main__': unittest.main()
