"""Create a consistent SQLite backup, including committed WAL data, without trading access."""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import sqlite3


def backup(source, destination):
    source, destination = Path(source).resolve(), Path(destination).resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    # Reserve the output without overwriting an earlier snapshot or the source.
    with destination.open('xb'):
        pass
    original = replica = None
    try:
        original = sqlite3.connect(source.as_uri()+'?mode=ro', uri=True)
        replica = sqlite3.connect(str(destination))
        original.backup(replica)
        result = replica.execute('PRAGMA integrity_check').fetchone()[0]
        if result != 'ok':
            raise ValueError('Backup integrity check failed: '+result)
    finally:
        if replica is not None: replica.close()
        if original is not None: original.close()
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', default='data/trades.sqlite')
    parser.add_argument('--output')
    args = parser.parse_args()
    output = args.output or 'data/backups/trades-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'.sqlite'
    print(backup(args.source, output))


if __name__ == '__main__': main()
