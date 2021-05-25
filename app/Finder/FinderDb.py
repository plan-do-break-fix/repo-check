#!/bin/python3
import sqlite3
from typing import List

SCHEMA = [
    "CREATE TABLE IF NOT EXISTS source ("
    "  name TEXT NOT NULL,"
    "  last_checked INTEGER NOT NULL"
    ");"
]

class Interface:

    def __init__(self):
        self.conn = sqlite3.connect(f"/data/nominis-finder.sqlite.db")
        self.c = self.conn.cursor()

    def add_repo_source(self, name) -> int:
        self.c.execute("INSERT INTO source (name) VALUES (?)", (name,))
        self.conn.commit()
        return self.c.lastrowid

    def update_last_check(self, name, timestamp) -> bool:
        self.c.execute("UPDATE source SET last_checked=? WHERE name=?",
                       (timestamp, name))
        self.conn.commit()

    #def get_source_to_check(self) -> str:
    #    self.c.execute("SELECT name, min(last_check) FROM source")
    #    return self.c.fetchone()[0][0]

    def list_sources(self) -> List[str]:
        self.c.execute("SELECT name FROM source")
        return self.c.fetchall()

    def time_since_last_check(self, source) -> int:
        self.c.execute("SELECT last_checked FROM source WHERE name=?",
                       (source,))
        result = self.c.fetchone()[0]
        return 0 if not result else int(result)
