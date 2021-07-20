import json
import sqlite3
from datetime import datetime
from typing import Iterator, Tuple


class ReposeDB:
    def __init__(self, filename: str) -> None:
        self.db = sqlite3.connect(filename)
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS revision_data (hash TEXT UNIQUE, ts INT, data BLOB)"
        )

    def has_hash(self, hash: str) -> bool:
        cur = self.db.cursor()
        cur.execute("SELECT COUNT(*) FROM revision_data WHERE hash = ?", [hash])
        (n,) = cur.fetchone()
        return n > 0

    def add_data(self, hash: str, timestamp: datetime, data: dict) -> None:
        if isinstance(timestamp, datetime):
            timestamp = int(timestamp.timestamp())
        assert isinstance(timestamp, int)
        self.db.execute(
            "INSERT INTO revision_data (hash, ts, data) VALUES (?, ?, ?)",
            [
                hash,
                timestamp,
                json.dumps(data, sort_keys=True),
            ],
        )

    def commit(self) -> None:
        self.db.commit()

    def get_hashes_and_times(self) -> Iterator[Tuple[str, datetime]]:
        cur = self.db.cursor()
        cur.execute("SELECT hash, ts FROM revision_data ORDER BY ts ASC")
        for hash, ts in cur:
            yield (hash, datetime.utcfromtimestamp(ts))

    def get_data(self, hash: str) -> dict:
        cur = self.db.cursor()
        cur.execute("SELECT data FROM revision_data WHERE hash = ? LIMIT 1", [hash])
        (data,) = cur.fetchone()
        return json.loads(data)
