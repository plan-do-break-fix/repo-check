#!/bin/python3
import sqlite3


SCHEMA = [
    "CREATE TABLE IF NOT EXISTS repo ("
    "  url TEXT NOT NULL,"
    "  type TEXT DEFAULT NULL,"
    "  last_visit TEXT DEFAULT NULL,"
    "  result TEXT DEFAULT NULL"
    ");",
    "CREATE TABLE IF NOT EXISTS watch ("
    "  repo FOREIGN_KEY NOT NULL"
    ");"#,
    #"CREATE TABLE IF NOT EXISTS report ("
    #"  repo INTEGER FOREIGN_KEY NOT NULL,"
    #"  report TEXT NOT NULL,"
    #"  timestamp TEXT NOT NULL,"
    #"  viewed INTEGER DEFAULT 0,"
    #"  closed INTEGER DEFAULT 0"
    #");"
]


class Interface:

    def __init__(self, data_path):
        self.conn = sqlite3.connect(f"{data_path}/sqlite.db")
        self.c = self.conn.cursor()

    def add_repo(self, repo_url) -> int:
        self.c.execute("INSERT INTO repo (url) VALUES (?)", (repo_url,))
        self.conn.commit()
        return self.c.lastrowid

    def update_repo(self, repo_url, timestamp, result) -> bool:
        self.c.execute("UPDATE repo SET last_visit=?, result=? WHERE url=?",
                       (timestamp, result, repo_url))

    def watch_repo(self, repo_url) -> bool:
        repo_pk = self.repo_exists(repo_url)
        if not repo_pk:
            repo_pk = add_repo(repo_url)
        self.c.execute("INSERT INTO watch (repo) VALUES (?)", (repo_pk,))
        self.conn.commit()
        return True

    def unwatch_repo(self, repo_url) -> bool:
        repo_pk = self.repo_exists(repo_url)
        self.c.execute("DELETE FROM watch WHERE repo=?", (repo_pk,))
        self.conn.commit()
        return True
