import unittest
from datetime import datetime, timedelta
from types import SimpleNamespace as NS
from unittest.mock import Mock
import pandas as pd

from src.market_data import confirmed_retest
from src.strategies.ict_swing_points import ICTSwingPointsStrategy
from src.strategies.nyupip import NYUPIPStrategy
from src.order_manager import OrderManager, ManagedOrder


class StrategyCorrectnessTests(unittest.TestCase):
    def test_bullish_ote_accepts_deep_pullback_not_shallow_progress(self):
        strategy = ICTSwingPointsStrategy()
        index = pd.to_datetime(['2026-10-26T20:00-04:00','2026-10-26T20:01-04:00','2026-10-26T20:02-04:00','2026-10-26T20:03-04:00','2026-10-27T02:30-04:00'],utc=True).tz_convert(strategy.timezone)
        frame = pd.DataFrame({'Open':[101]*4+[105],'High':[102]*4+[110],'Low':[100]*4+[104],'Close':[101]*4+[108],'Volume':[10]*5},index=index)
        sessions={'ASIA':frame.iloc[:4]}
        now=pd.Timestamp('2026-10-27T03:00-04:00')
        self.assertTrue(strategy._london_open_setups(sessions,frame,now,{'price':103.}))
        self.assertFalse(strategy._london_open_setups(sessions,frame,now,{'price':107.}))
    def test_new_york_session_clock_tracks_both_dst_transitions(self):
        strategy = ICTSwingPointsStrategy(timezone='Africa/Johannesburg')
        for ts, expected in [('2026-03-06T07:30Z', True), ('2026-03-09T06:30Z', True), ('2026-10-30T06:30Z', True), ('2026-11-02T07:30Z', True)]:
            local = pd.Timestamp(ts).tz_convert(strategy.timezone)
            self.assertEqual(strategy._is_active_trading_time(local), expected)
            self.assertEqual(local.hour, 2)

    def test_asia_range_comes_from_previous_new_york_evening(self):
        strategy = ICTSwingPointsStrategy(timezone='Africa/Johannesburg')
        index = pd.date_range('2026-10-26T23:00Z', periods=300, freq='min').tz_convert(strategy.timezone)
        frame = pd.DataFrame({'Close':100},index=index)
        sessions = strategy._extract_sessions(frame)
        self.assertEqual(len(sessions['ASIA']), 300)

    def test_mere_retest_touch_does_not_confirm_entry(self):
        idx = pd.date_range('2026-10-27T08:00Z',periods=5,freq='min')
        frame = pd.DataFrame({'Open':[100]*5,'High':[101]*5,'Low':[99]*5,'Close':[100]*5},index=idx)
        self.assertFalse(confirmed_retest(frame,'2026-10-27T08:05Z',100,1,.1))
        frame.loc[idx[-1], ['Close','High']] = [102,102]
        self.assertTrue(confirmed_retest(frame,'2026-10-27T08:05Z',100,1,.1))
        self.assertFalse(confirmed_retest(frame,'2026-10-27T08:04:30Z',100,1,.1))

    def test_nyupip_utc_context_keeps_last_completed_boundary(self):
        idx = pd.date_range('2026-10-20T00:00Z',periods=6000,freq='min')
        frame = pd.DataFrame({'Open':100.,'High':101.,'Low':99.,'Close':100.,'Volume':10.},index=idx)
        now = idx[-1] + pd.Timedelta(minutes=1)
        strategy = NYUPIPStrategy()
        ctx = strategy._build_context(frame,{'timestamp':now,'price':100.})
        self.assertIsNotNone(ctx)
        self.assertEqual(str(ctx['timestamp'].tz), 'UTC')
        self.assertEqual(ctx['m15_closed'].index[-1] + pd.Timedelta(minutes=15), now.floor('15min'))

    def test_atm_uses_explicit_holding_period(self):
        manager = OrderManager.__new__(OrderManager)
        manager.cfg = {'execution':{'max_position_minutes':{'ICT_ATM':120}}}
        manager.autotrader = NS(close_position=Mock(), modify_sl_tp=Mock())
        state = ManagedOrder(1,datetime.utcnow()-timedelta(minutes=11),100,99,102,1,'ICT_ATM')
        manager._apply_exit_rules(NS(price_current=100),state)
        manager.autotrader.close_position.assert_not_called()

    def test_failed_time_exit_retains_tracking_and_retries(self):
        manager = OrderManager.__new__(OrderManager)
        manager.cfg = {'execution':{'max_position_minutes':{'FARMER':10}}}
        manager.autotrader = NS(close_position=Mock(return_value=False), modify_sl_tp=Mock())
        manager.persistence = NS(update_trade=Mock())
        manager.loss_minimizer_enabled = False
        state = ManagedOrder(1,datetime.utcnow()-timedelta(minutes=11),100,99,102,1,'FARMER','FARMER')
        manager.managed = {1:state}
        manager._apply_exit_rules(NS(price_current=100),state)
        manager._apply_exit_rules(NS(price_current=100),state)
        self.assertIn(1,manager.managed)
        self.assertFalse(state.close_requested)
        self.assertEqual(manager.autotrader.close_position.call_count,2)
        self.assertNotIn('status',manager.persistence.update_trade.call_args.args[1])

    def test_restart_adopts_bot_position_with_original_open_time(self):
        manager = OrderManager.__new__(OrderManager)
        position = NS(ticket=123,magic=20250923,time=1700000000,price_open=100,sl=99,tp=102,type=0)
        manager.mt5 = NS(today_realized_pnl=lambda:0,get_equity=lambda:1000,get_positions=lambda _: [position])
        manager.persistence = NS(get_open_trades=lambda _: [{'ticket':123,'alert_level':'ICT_ATM'}])
        manager.symbol,manager.managed,manager.daily_loss_limit_pct='XAUUSDm',{},2
        manager._apply_exit_rules = Mock()
        manager.reconcile()
        self.assertEqual(manager.managed[123].open_time,datetime.utcfromtimestamp(position.time))
        self.assertEqual(manager.managed[123].alert_level,'ICT_ATM')

    def test_broker_read_failure_cannot_close_tracking(self):
        manager = OrderManager.__new__(OrderManager)
        manager.mt5 = NS(today_realized_pnl=lambda:0,get_equity=lambda:1000,get_positions=lambda _:None)
        manager.symbol,manager.daily_loss_limit_pct='XAUUSDm',2
        manager.managed={123:object()}
        manager.reconcile()
        self.assertIn(123,manager.managed)


if __name__ == '__main__': unittest.main()
