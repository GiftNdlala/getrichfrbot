import time
import json
from pathlib import Path
import unittest
from types import SimpleNamespace as NS
import test_execution_safety as safety
from src.risk_controls import usd_account_rate, execution_snapshot


class CurrencyTests(unittest.TestCase):
    def broker(self, inverse=False, stale=False):
        api = safety.Broker()
        api.account.currency = 'ZAR'
        api.symbols_get = lambda: [NS(name='ZARUSDm' if inverse else 'USDZARm', currency_base='ZAR' if inverse else 'USD', currency_profit='USD' if inverse else 'ZAR')]
        api.symbol_select = lambda *args: True
        gold_tick = api.symbol_info_tick
        api.symbol_info_tick = lambda symbol: gold_tick(symbol) if symbol == 'XAUUSDm' else NS(bid=.05 if inverse else 18., ask=.051 if inverse else 18.1, time=time.time()-(120 if stale else 0))
        return api

    def test_direct_suffix_and_inverse(self):
        self.assertEqual(usd_account_rate(self.broker(), NS(currency='ZAR')), 18.)
        self.assertAlmostEqual(usd_account_rate(self.broker(inverse=True), NS(currency='ZAR')), 1/.051)

    def test_stale_conversion_blocks(self):
        with self.assertRaisesRegex(ValueError, 'USD_CONVERSION_UNAVAILABLE:ZAR'):
            usd_account_rate(self.broker(stale=True), NS(currency='ZAR'))

    def test_zar_farmer_target_and_risk_are_converted(self):
        fixture = safety.ExecutionSafetyTests()
        fixture.setUp()
        fixture.api = self.broker()
        fixture.api.account.balance = fixture.api.account.equity = fixture.api.account.margin_free = 18000.
        profit = fixture.api.order_calc_profit
        fixture.api.order_calc_profit = lambda *args: profit(*args)*18
        trade = fixture.order(sl=99.2, tag='FARMER')
        self.assertIsNotNone(trade)
        gross = fixture.api.order_calc_profit(0, 'XAUUSDm', trade['volume'], trade['price'], trade['tp'])
        risk = -fixture.api.order_calc_profit(0, 'XAUUSDm', trade['volume'], trade['price'], trade['sl'])
        self.assertGreaterEqual(gross+1e-8, (2+.15)*18)
        self.assertLessEqual(risk+.15*18, 18.+1e-8)

    def test_zar_daily_farmer_loss_cap(self):
        fixture = safety.ExecutionSafetyTests()
        fixture.setUp()
        fixture.api = self.broker()
        fixture.api.account.balance = fixture.api.account.equity = 18000.
        fixture.api.deals = [NS(magic=20250923, comment='FARMER', position_id=1, entry=1, time=time.time()-300, profit=-91)]
        fixture.blocked('FARMER_DAILY_LOSS_CAP', tag='FARMER')

    def test_ten_thousand_rand_profile_executes_affordable_minimum_gold_lot(self):
        fixture = safety.ExecutionSafetyTests()
        fixture.setUp()
        profile = json.loads((Path(__file__).resolve().parents[1]/'config.json').read_text())
        fixture.cfg['risk'] = profile['risk']
        fixture.cfg['execution']['farmer'] = profile['execution']['farmer']
        fixture.api = self.broker()
        fixture.api.account.balance = fixture.api.account.equity = fixture.api.account.margin_free = 10000.
        profit = fixture.api.order_calc_profit
        fixture.api.order_calc_profit = lambda *args: profit(*args)*18
        trade = fixture.order(sl=98., tag='TEST')
        self.assertIsNotNone(trade)
        risk = -fixture.api.order_calc_profit(0,'XAUUSDm',trade['volume'],trade['price'],trade['sl'])
        self.assertLessEqual(risk+.15*18, 50.)

    def test_ten_thousand_rand_profile_explains_unaffordable_minimum_lot(self):
        fixture = safety.ExecutionSafetyTests()
        fixture.setUp()
        fixture.cfg['risk'].update(risk_percent_per_trade=.5, max_open_risk_pct=1., cost_buffer_dollars=.15)
        fixture.api = self.broker()
        fixture.api.account.balance = fixture.api.account.equity = fixture.api.account.margin_free = 10000.
        profit = fixture.api.order_calc_profit
        fixture.api.order_calc_profit = lambda *args: profit(*args)*18
        fixture.blocked('MINIMUM_LOT_EXCEEDS_RISK', sl=95.)
        self.assertIn('currency=ZAR budget=50.00', fixture.trader.last_rejection)
        self.assertIn('required=', fixture.trader.last_rejection)

    def test_shared_rand_budget_includes_existing_costs_and_farmer_reserve(self):
        fixture = safety.ExecutionSafetyTests()
        fixture.setUp()
        profile = json.loads((Path(__file__).resolve().parents[1]/'config.json').read_text())
        fixture.cfg['risk'] = profile['risk']
        fixture.api = self.broker()
        fixture.api.account.balance = fixture.api.account.equity = 10000.
        profit = fixture.api.order_calc_profit
        fixture.api.order_calc_profit = lambda *args: profit(*args)*18
        fixture.api.positions = [NS(ticket=n, symbol='XAUUSDm', type=0, volume=.02, price_open=100., sl=99., comment='TEST') for n in (1,2)]
        budget, _ = execution_snapshot(fixture.api, fixture.cfg, 'XAUUSDm', fixture.context, fixture.api.tick, fixture.api.account, 'TEST')
        self.assertAlmostEqual(budget, 100.-20.-2*(36.+2.7))
