import unittest
from analysis.performance_report import summarize


class PerformanceTests(unittest.TestCase):
    def test_unknown_results_are_not_wins(self):
        result = summarize([{'status':'CLOSED','pnl':None,'tp':123}, {'status':'CLOSED','pnl':-2}, {'status':'CLOSED','pnl':2}])
        self.assertEqual(result['known_outcomes'], 2)
        self.assertEqual(result['missing_closed_outcomes'], 1)
        self.assertEqual(result['win_rate_known_pct'], 50)
        self.assertEqual(result['recorded_pnl'], 0)
    def test_sixty_percent_wins_can_still_lose_money(self):
        result = summarize([{'status':'CLOSED','pnl':x} for x in [1]*6+[-2]*4])
        self.assertEqual(result['win_rate_known_pct'], 60)
        self.assertEqual(result['recorded_pnl'], -2)
        self.assertEqual(result['profit_factor_known'], .75)
    def test_no_history_is_not_perfect_performance(self):
        self.assertIsNone(summarize([])['win_rate_known_pct'])


if __name__ == '__main__': unittest.main()
