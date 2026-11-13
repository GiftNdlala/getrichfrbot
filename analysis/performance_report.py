"""Read-only trade report. Unknown outcomes are never substituted with targets."""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3


def summarize(rows):
    closed = [r for r in rows if r.get('status') == 'CLOSED']
    known = [r for r in closed if r.get('pnl') is not None]
    values = [float(r['pnl']) for r in known]
    wins, losses = [x for x in values if x > 0], [x for x in values if x < 0]
    return {
        'records': len(rows), 'closed': len(closed), 'known_outcomes': len(known),
        'missing_closed_outcomes': len(closed)-len(known),
        'wins': len(wins), 'losses': len(losses), 'flat': sum(x == 0 for x in values),
        'win_rate_known_pct': round(100*len(wins)/len(known), 2) if known else None,
        'recorded_pnl': round(sum(values), 2) if known else None,
        'mean_pnl_known': round(sum(values)/len(known), 4) if known else None,
        'mean_win': round(sum(wins)/len(wins), 4) if wins else None,
        'mean_loss': round(sum(losses)/len(losses), 4) if losses else None,
        'profit_factor_known': round(sum(wins)/abs(sum(losses)), 4) if losses else None,
        'all_known_outcomes_positive': bool(values) and all(x > 0 for x in values),
    }


def report(database, since=None):
    path = Path(database).resolve()
    connection = sqlite3.connect(path.as_uri()+'?mode=ro', uri=True)
    connection.row_factory = sqlite3.Row
    try:
        rows = [dict(r) for r in connection.execute('SELECT * FROM trades')]
    finally:
        connection.close()
    if since:
        boundary = datetime.fromisoformat(since.replace('Z', '+00:00'))
        if boundary.tzinfo is None:
            boundary = boundary.replace(tzinfo=timezone.utc)
        selected = []
        for r in rows:
            ts = datetime.fromisoformat(r['timestamp'].replace('Z', '+00:00'))
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
            if ts >= boundary:
                selected.append(r)
        rows = selected
    groups = defaultdict(list)
    for r in rows:
        groups[r.get('engine') or 'UNKNOWN'].append(r)
    tickets = Counter(r.get('ticket') for r in rows if r.get('ticket') is not None)
    return {
        'database': str(path), 'since': since,
        'warning': 'Recorded subset only. Legacy P&L may omit costs. Unknown outcomes and duplicate tickets prevent a whole-account profitability conclusion. No account-return percentage is inferred.',
        'latest_trade': max((r['timestamp'] for r in rows), default=None),
        'duplicate_tickets': sum(n > 1 for n in tickets.values()),
        'overall': summarize(rows), 'engines': {k: summarize(v) for k,v in sorted(groups.items())},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('database')
    parser.add_argument('--since', help='ISO timestamp, UTC if offset is omitted')
    parser.add_argument('--output', help='Save JSON report; otherwise print it')
    args = parser.parse_args()
    result = json.dumps(report(args.database, args.since), indent=2)
    if args.output:
        Path(args.output).write_text(result+'\n', encoding='utf-8')
    else:
        print(result)


if __name__ == '__main__': main()
