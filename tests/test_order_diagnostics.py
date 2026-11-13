import contextlib
import io
from types import SimpleNamespace as NS
import unittest
from unittest.mock import patch
import test_execution_safety as safety


class OrderDiagnosticsTests(unittest.TestCase):
    def setUp(self):
        self.fixture=safety.ExecutionSafetyTests()
        self.fixture.setUp()

    def test_guard_reason_survives_quiet_stdout(self):
        f=self.fixture
        f.cfg['news']={'enabled':True,'calendar_file':'missing-calendar-for-test.json'}
        visible,hidden=io.StringIO(),io.StringIO()
        with patch('sys.__stdout__',visible),contextlib.redirect_stdout(hidden):
            self.assertIsNone(f.order())
        self.assertIn('NEWS_CALENDAR_UNAVAILABLE',visible.getvalue())
        self.assertNotIn('NEWS_CALENDAR_UNAVAILABLE',hidden.getvalue())
        self.assertEqual(f.trader.last_outcome,'blocked')

    def test_broker_rejection_has_retcode_and_is_not_a_policy_block(self):
        f=self.fixture
        f.api.order_send=lambda request:NS(retcode=10027,comment='AutoTrading disabled')
        self.assertIsNone(f.order())
        self.assertEqual(f.trader.last_outcome,'rejected')
        self.assertIn('10027',f.trader.last_rejection)
        self.assertIn('AutoTrading disabled',f.trader.last_rejection)

    def test_missing_margin_has_explicit_reason(self):
        f=self.fixture
        f.api.account.margin_free=0
        self.assertIsNone(f.order())
        self.assertEqual(f.trader.last_rejection,'INSUFFICIENT_MARGIN_FOR_MINIMUM_LOT')


if __name__ == '__main__': unittest.main()
