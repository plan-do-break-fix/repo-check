#!/bin/python3
from datetime import datetime
from typing import List, Tuple, Union

import mysql.connector
from mysql.connector import errorcode

class Interface:

    def __init__(self, host, user, password):
        self.connection = mysql.connector.connect(user=user,
                                                  password=password,
                                                  host=host)
        self.c = self.connection.cursor()
        self.c.execute("USE mndatus;")

    def repo_exists(self, repo_url) -> Union[int,bool]:
        self.c.execute("SELECT id FROM repo WHERE url=%s;", (repo_url,))
        result = self.c.fetchone()
        return result[0] if result else False

    def add_repo(self, repo_url, timestamp, repo_type=None):
        self.c.execute("INSERT INTO repo (url, repo_type, added) VALUES (%s, %s, %s);",
                       (repo_url, repo_type, timestamp))
        self.connection.commit()

    def repo_is_watched(self, repo_pk):
        """Return repo pk if repo is watched else False."""
        self.c.execute("SELECT id FROM watch WHERE repo=%s;", (repo_pk,))
        result = self.c.fetchone()
        return bool(result)        

    def watch_repo(self, repo_url, timestamp):
        repo_pk = self.repo_exists(repo_url)
        if self.repo_is_watched(repo_pk):
            return True
        self.c.execute("INSERT INTO watch (repo, watched_since) VALUES (%s);",
                       (repo_pk, timestamp))
        self.connection.commit()
        return True

    def unwatch_repo(self, repo_url):
        repo_pk = self.repo_exists(repo_url)
        if not self.repo_is_watched(repo_pk):
            return True
        self.c.execute("DELETE FROM watch WHERE repo=%s;", (repo_pk,))
        self.connection.commit()
        return True

    def record_inspection(self, repo_url, timestamp, result):
        self.c.execute("UPDATE repo"
                       "  SET"
                       "    last_inspected=%s,"
                       "    last_result=%s"
                       "  WHERE"
                       "    url=%s;",
                       (timestamp, result, repo_url)) 
        self.connection.commit()
        return True

    def get_watched_repo_visit_times(self, cutoff=0) -> List[Tuple]:
        self.c.execute("SELECT a.url, a.last_inspected"
                       "  FROM repo a, watch b"
                       "  WHERE a.id = b.repo"
                       "  AND a.last_inspected >= %s"
                       "  AND a.check_out = 0;",
                       (cutoff,))
        return self.c.fetchall()

    def get_unvisited_repos(self) -> List[str]:
        self.c.execute("SELECT url FROM repo"
                       "  WHERE last_inspected IS NULL"
                       "  AND check_out=0;")
        return [_i[0] for _i in self.c.fetchall()]

    def count_unvisited_repos(self) -> int:
        self.c.execute("SELECT COUNT(url) FROM repo"
                       "  WHERE last_inspected IS NULL;")
        return self.c.fetchone()[0]

    def check_out(self, repo_url) -> bool:
        self.c.execute("UPDATE repo SET check_out=1 WHERE url=%s;",
                       (repo_url,))
        self.connection.commit()
        return True

    def check_in(self, repo_url) -> bool:
        self.c.execute("UPDATE repo SET check_out=0 WHERE url=%s",
                       (repo_url,))
        self.connection.commit()
        return True
