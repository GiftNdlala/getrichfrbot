"""Refresh verified-week provider data outside the trading/MT5 lock."""
from datetime import datetime, time, timedelta, timezone
import json
import os
from pathlib import Path
import tempfile
import threading
from urllib.request import Request, urlopen
import pytz

from .runtime_logging import emit
from .risk_controls import news_reason


FEED_URL = 'https://nfs.faireconomy.media/ff_calendar_thisweek.json'


def normalize_calendar(events, now):
    """Reject stale/empty/wrong-week feeds rather than blessing an empty calendar."""
    if not isinstance(events, list) or not events:
        raise ValueError('Empty or invalid provider calendar')
    if now.tzinfo is None:
        raise ValueError('Calendar clock must be timezone-aware')
    ny = pytz.timezone('America/New_York')
    local = now.astimezone(ny)
    sunday = local.date() - timedelta(days=(local.weekday()+1) % 7)
    start = ny.localize(datetime.combine(sunday, time()))
    end = ny.localize(datetime.combine(sunday+timedelta(days=7), time()))
    result = []
    for event in events:
        ts = datetime.fromisoformat(event['date'].replace('Z', '+00:00'))
        if ts.tzinfo is None or not start <= ts < end:
            raise ValueError('Provider calendar is not the current New York week')
        if event.get('country') == 'USD' and str(event.get('impact')).lower() == 'high':
            result.append({'name':event['title'], 'timestamp':ts.astimezone(timezone.utc).isoformat(), 'currency':'USD', 'impact':'HIGH'})
    return {
        'source': FEED_URL,
        'fetched_at': now.astimezone(timezone.utc).isoformat(),
        'valid_from': start.astimezone(timezone.utc).isoformat(),
        'valid_until': min(end.astimezone(timezone.utc), now.astimezone(timezone.utc)+timedelta(hours=6)).isoformat(),
        'events':result,
    }


def fetch_provider():
    request = Request(FEED_URL, headers={'User-Agent':'GetRichFRBot/1.0', 'Accept':'application/json'})
    with urlopen(request, timeout=12) as response:
        return json.loads(response.read(2_000_000).decode('utf-8'))


class CalendarRefresher:
    def __init__(self, config):
        self.config = dict(config)
        self.stop_event = threading.Event()
        self.thread = None
        self.lock = threading.Lock()
        self.status = {'state':'not_started'}

    def refresh_once(self, now=None, fetch=None):
        now = now or datetime.now(timezone.utc)
        path = Path(self.config.get('calendar_file','data/news_calendar.json'))
        if not path.is_absolute():
            path = Path(__file__).resolve().parents[1]/path
        # Respect an operator-maintained valid calendar; refresh our own cache.
        if path.exists() and news_reason(dict(self.config,enabled=True),now.timestamp()) not in ('NEWS_CALENDAR_STALE','NEWS_CALENDAR_UNAVAILABLE'):
            old = json.loads(path.read_text(encoding='utf-8'))
            if old.get('source') != FEED_URL:
                self.status = {'state':'manual_calendar_in_use','valid_until':old.get('valid_until')}
                return old
        payload = normalize_calendar((fetch or fetch_provider)(), now)
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',dir=path.parent,prefix='.news-calendar-',suffix='.tmp',delete=False) as output:
                temporary = Path(output.name)
                json.dump(payload,output,indent=2)
            os.replace(temporary,path)
        finally:
            if temporary is not None and temporary.exists():
                temporary.unlink()
        self.status = {'state':'ready','valid_until':payload['valid_until'],'event_count':len(payload['events'])}
        emit(f"NEWS CALENDAR READY: high_impact_usd_events={len(payload['events'])} valid_until={payload['valid_until']}")
        return payload

    def start(self):
        with self.lock:
            if not self.config.get('enabled',True) or not self.config.get('auto_refresh',True):
                self.status = {'state':'automatic_refresh_disabled'}
                return
            if self.thread and self.thread.is_alive():
                return
            self.stop_event.clear()
            def worker():
                while not self.stop_event.is_set():
                    try:
                        self.refresh_once()
                        delay = max(300,float(self.config.get('refresh_seconds',3600)))
                    except Exception as exc:
                        self.status = {'state':'refresh_failed','reason':str(exc)}
                        emit(f"NEWS CALENDAR REFRESH FAILED: {exc}; new entries require valid cached coverage")
                        delay = 300
                    self.stop_event.wait(delay)
            self.thread = threading.Thread(target=worker,name='news-calendar-refresh',daemon=True)
            emit('NEWS CALENDAR: starting automatic refresh; entries wait until coverage is ready')
            self.thread.start()

    def stop(self, timeout=15):
        self.stop_event.set()
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=timeout)
