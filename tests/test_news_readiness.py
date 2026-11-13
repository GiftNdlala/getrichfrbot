from datetime import datetime,timezone
import json
from pathlib import Path
import tempfile
import unittest
from src.risk_controls import news_reason


class NewsReadinessTests(unittest.TestCase):
    def test_valid_coverage_and_blackout_boundaries(self):
        with tempfile.TemporaryDirectory() as tmp:
            calendar=Path(tmp)/'calendar.json'
            calendar.write_text(json.dumps({'valid_from':'2026-10-27T00:00:00Z','valid_until':'2026-10-27T23:59:59Z','events':[{'name':'VERIFIED_TEST_EVENT','timestamp':'2026-10-27T12:30:00Z','currency':'USD','impact':'HIGH'}]}))
            config={'enabled':True,'calendar_file':str(calendar),'pre_blackout_minutes':30,'post_blackout_minutes':15}
            def check(clock):
                return news_reason(config,datetime.fromisoformat(clock.replace('Z','+00:00')).timestamp())
            self.assertIsNone(check('2026-10-27T11:59:00Z'))
            self.assertIn('NEWS_BLACKOUT',check('2026-10-27T12:00:00Z'))
            self.assertIn('NEWS_BLACKOUT',check('2026-10-27T12:45:00Z'))
            self.assertIsNone(check('2026-10-27T12:46:00Z'))
            self.assertEqual(check('2026-10-28T00:00:00Z'),'NEWS_CALENDAR_STALE')


if __name__ == '__main__': unittest.main()
