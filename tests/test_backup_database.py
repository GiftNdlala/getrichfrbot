import tempfile
from pathlib import Path
import sqlite3
import unittest
from analysis.backup_database import backup


class BackupTests(unittest.TestCase):
    def test_live_wal_is_included_without_changing_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, destination = Path(tmp)/'live.sqlite',Path(tmp)/'snapshot.sqlite'
            conn=sqlite3.connect(source)
            try:
                conn.execute('PRAGMA journal_mode=WAL')
                conn.execute('CREATE TABLE trades(ticket INTEGER)')
                conn.execute('INSERT INTO trades VALUES (123)')
                conn.commit()
                backup(source,destination)
                replica=sqlite3.connect(destination)
                try:
                    self.assertEqual(replica.execute('SELECT ticket FROM trades').fetchone()[0],123)
                finally: replica.close()
                self.assertEqual(conn.execute('SELECT COUNT(*) FROM trades').fetchone()[0],1)
                with self.assertRaises(FileExistsError): backup(source,destination)
                with self.assertRaises(FileExistsError): backup(source,source)
            finally: conn.close()


if __name__ == '__main__': unittest.main()
