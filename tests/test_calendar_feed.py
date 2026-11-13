from datetime import datetime, timezone
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock
from src.calendar_feed import CalendarRefresher, FEED_URL, normalize_calendar
from src.risk_controls import news_reason


class CalendarFeedTests(unittest.TestCase):
    def setUp(self):
        self.now=datetime(2026,10,27,10,tzinfo=timezone.utc)
        self.events=[{'title':'Test USD release','country':'USD','impact':'High','date':'2026-10-28T14:30:00+02:00'}, {'title':'Other event','country':'EUR','impact':'Low','date':'2026-10-26T12:00:00Z'}]

    def test_normalizes_provider_dates_and_does_not_invent_events(self):
        payload=normalize_calendar(self.events,self.now)
        self.assertEqual(payload['source'],FEED_URL)
        self.assertEqual(len(payload['events']),1)
        self.assertEqual(payload['events'][0]['timestamp'],'2026-10-28T12:30:00+00:00')
        self.assertEqual(payload['valid_until'],'2026-10-27T16:00:00+00:00')

    def test_wrong_week_and_empty_feeds_are_rejected(self):
        with self.assertRaises(ValueError): normalize_calendar([],self.now)
        self.events[0]['date']='2026-10-21T14:30:00+02:00'
        with self.assertRaisesRegex(ValueError,'current New York week'): normalize_calendar(self.events,self.now)

    def test_atomic_cache_unblocks_readiness_without_disabling_news(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'calendar.json'
            cfg={'enabled':True,'calendar_file':str(path)}
            refresher=CalendarRefresher(cfg)
            self.assertEqual(news_reason(cfg,self.now.timestamp()),'NEWS_CALENDAR_UNAVAILABLE')
            refresher.refresh_once(self.now,lambda:self.events)
            self.assertIsNone(news_reason(cfg,self.now.timestamp()))
            self.assertEqual(refresher.status['state'],'ready')
            self.assertEqual(list(Path(tmp).glob('*.tmp')),[])

    def test_stale_fetch_never_overwrites_a_valid_cache(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'calendar.json'
            cfg={'enabled':True,'calendar_file':str(path)}
            refresher=CalendarRefresher(cfg)
            refresher.refresh_once(self.now,lambda:self.events)
            before=path.read_bytes()
            with self.assertRaises(ValueError): refresher.refresh_once(self.now,lambda:[])
            self.assertEqual(path.read_bytes(),before)
            self.assertIsNone(news_reason(cfg,self.now.timestamp()))

    def test_valid_manual_calendar_is_preserved_even_during_blackout(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'manual.json'
            payload=normalize_calendar(self.events,self.now)
            payload['source']='operator'
            payload['events'][0]['timestamp']=self.now.isoformat()
            path.write_text(json.dumps(payload))
            fetch=Mock()
            CalendarRefresher({'enabled':True,'calendar_file':str(path)}).refresh_once(self.now,fetch)
            fetch.assert_not_called()

    def test_provider_week_boundaries_handle_dst(self):
        now=datetime(2026,3,9,12,tzinfo=timezone.utc)
        result=normalize_calendar([{'title':'test','country':'USD','impact':'High','date':'2026-03-10T12:00:00Z'}],now)
        self.assertEqual(result['valid_from'],'2026-03-08T05:00:00+00:00')


if __name__ == '__main__': unittest.main()
