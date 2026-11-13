import unittest
from types import SimpleNamespace as NS
import test_execution_safety as safety
from src.risk_controls import ACKNOWLEDGED_ORDERS, execution_snapshot


class SharedRiskTests(unittest.TestCase):
    def setUp(self):
        self.f = safety.ExecutionSafetyTests()
        self.f.setUp()
        self.f.cfg['risk'].update(max_concurrent_trades=4, farmer_reserve={'slots':1, 'risk_pct':.1})

    def position(self, ticket=7, symbol='XAUUSDm', volume=.02):
        return NS(ticket=ticket, identifier=ticket, symbol=symbol, volume=volume, type=0, price_open=100., sl=99., comment='OTHER')

    def snapshot(self, strategy='TEST'):
        f = self.f
        return execution_snapshot(f.api, f.cfg, 'XAUUSDm', f.context, f.api.tick, f.api.account, strategy)

    def test_multiple_positions_share_budget_and_farmer_reserve(self):
        self.f.api.positions = [self.position()]
        budget, _ = self.snapshot()
        self.assertAlmostEqual(budget, 2.)  # $5 cap - $2 open - $1 reserved.
        self.assertAlmostEqual(self.snapshot('FARMER')[0], 1.)

    def test_farmer_slot_remains_available(self):
        self.f.api.positions = [self.position(i, volume=.001) for i in range(3)]
        with self.assertRaisesRegex(ValueError, 'FARMER_RESERVED'):
            self.snapshot()
        self.assertGreater(self.snapshot('FARMER')[0], 0)

    def test_account_cap_includes_other_symbols(self):
        self.f.api.positions = [self.position(symbol='US30m', volume=.05)]
        with self.assertRaisesRegex(ValueError, 'RISK_BUDGET_EXHAUSTED'):
            self.snapshot('FARMER')

    def test_netting_account_cannot_merge_independent_strategy_positions(self):
        self.f.api.account.margin_mode = 0
        self.f.api.positions = [self.position(volume=.001)]
        with self.assertRaisesRegex(ValueError, 'NETTING_POSITION_EXISTS'):
            self.snapshot()

    def test_mismatched_order_id_released_after_confirmed_close(self):
        ACKNOWLEDGED_ORDERS[(1,123)] = {'volume':.02, 'risk':2., 'deal':456, 'symbol':'XAUUSDm'}
        opening = NS(order=123, ticket=456, position_id=789, entry=0, volume=.02)
        closing = NS(position_id=789, entry=1, volume=.02)
        self.f.api.history_deals_get = lambda *a, **kw: [opening,closing]
        self.snapshot()
        self.assertNotIn((1,123), ACKNOWLEDGED_ORDERS)

    def test_partial_close_and_missing_history_keep_reservation(self):
        ACKNOWLEDGED_ORDERS[(1,123)] = {'volume':.02, 'risk':2., 'symbol':'XAUUSDm'}
        self.f.api.deals = [NS(position_id=123, entry=1, volume=.01)]
        self.snapshot()
        self.assertIn((1,123), ACKNOWLEDGED_ORDERS)

    def test_visible_position_identifier_is_not_counted_twice(self):
        self.f.api.positions = [self.position(ticket=789)]
        ACKNOWLEDGED_ORDERS[(1,123)] = {'volume':.02, 'risk':2., 'deal':456, 'symbol':'XAUUSDm'}
        self.f.api.deals = [NS(order=123, ticket=456, position_id=789, entry=0)]
        self.assertAlmostEqual(self.snapshot()[0], 2.)
