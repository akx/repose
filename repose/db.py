import json
import sqlite3
from datetime import datetime


class ReposeDB:
    def __init__(self, filename):
        self.db = sqlite3.connect(filename)
        self.db.execute('CREATE TABLE IF NOT EXISTS revision_data (hash TEXT UNIQUE, ts INT, data BLOB)')

    def has_hash(self, hash):
        cur = self.db.cursor()
        cur.execute('SELECT COUNT(*) FROM revision_data WHERE hash = ?', [hash])
        n, = cur.fetchone()
        return (n > 0)

    def add_data(self, hash, timestamp, data):
        if isinstance(timestamp, datetime):
            timestamp = int(timestamp.timestamp())
        assert isinstance(timestamp, int)
        self.db.execute('INSERT INTO revision_data (hash, ts, data) VALUES (?, ?, ?)', [
            hash,
            timestamp,
            json.dumps(data, sort_keys=True),
        ])

    def commit(self):
        self.db.commit()
