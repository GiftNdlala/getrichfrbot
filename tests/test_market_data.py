import unittest
import pandas as pd
from src.market_data import broker_frame, closed_bars
from src.strategies.farmer import FarmerStrategy


def rates(n=120):
    idx = pd.date_range('2026-10-27T08:00Z', periods=n, freq='min')
    return [{'time': t.timestamp(), 'open': 100., 'high': 102., 'low': 99., 'close': 101., 'tick_volume': 10} for t in idx]


class MarketDataTests(unittest.TestCase):
    def test_only_completed_m1_in_history(self):
        bars = broker_frame(rates(), '2026-10-27T09:59:30Z')
        self.assertEqual(len(bars), 119)
        self.assertEqual(str(bars.index.tz), 'UTC')
        self.assertEqual(bars.iloc[-1].High, 102.)
    def test_repeated_snapshot_replaces_not_duplicates(self):
        r = rates()
        r.append(dict(r[-1], high=103.))
        bars = broker_frame(r, '2026-10-27T10:00Z')
        self.assertEqual(len(bars), 120)
        self.assertEqual(bars.iloc[-1].High, 103.)
    def test_stale_history_raises(self):
        with self.assertRaisesRegex(ValueError, 'STALE'):
            broker_frame(rates(), '2026-10-27T10:10Z')
    def test_forming_h1_and_future_input_excluded(self):
        bars = broker_frame(rates(), '2026-10-27T10:00Z')
        h1 = closed_bars(bars, '1h', '2026-10-27T09:30Z')
        self.assertEqual(len(h1), 1)
        self.assertEqual(h1.index[-1].hour, 8)
    def test_complete_boundary_bar_retained(self):
        bars = broker_frame(rates(), '2026-10-27T10:00Z')
        self.assertEqual(len(closed_bars(bars, '15min', '2026-10-27T10:00Z')), 8)
    def test_incomplete_higher_timeframe_bar_rejected(self):
        bars = broker_frame(rates(), '2026-10-27T10:00Z').drop(pd.Timestamp('2026-10-27T08:15Z'))
        self.assertEqual(len(closed_bars(bars, '1h', '2026-10-27T10:00Z')), 1)
    def test_farmer_does_not_force_trades_in_flat_market(self):
        f = FarmerStrategy()
        self.assertIsNone(f.evaluate(broker_frame(rates(), '2026-10-27T10:00Z')))
        self.assertEqual(f.diagnostics['reason'], 'no_confirmed_pullback')
    def test_farmer_checks_a_bar_once(self):
        f = FarmerStrategy()
        bars = broker_frame(rates(), '2026-10-27T10:00Z')
        f.evaluate(bars)
        self.assertIsNone(f.evaluate(bars))

    def test_farmer_accepts_completed_trend_pullback_confirmation(self):
        index = pd.date_range('2026-10-27T08:00Z',periods=60,freq='min')
        closes = [100+i*.1 for i in range(60)]
        bars = pd.DataFrame({'Open':closes,'High':[x+.2 for x in closes],'Low':[x-.2 for x in closes],'Close':closes,'Volume':10},index=index)
        bars.loc[index[-2],['Open','High','Low','Close']] = [104,105,103,104]
        bars.loc[index[-1],['Open','High','Low','Close']] = [104.5,107.2,104.4,107]
        candidate=FarmerStrategy().evaluate(bars)
        self.assertIsNotNone(candidate)
        self.assertEqual(candidate['direction'],1)
        self.assertLess(candidate['sl'],103)


if __name__ == '__main__': unittest.main()
