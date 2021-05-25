#~/bin/python3
# MNDatus RepoFinder v1.0
from datetime import datetime
from os import environ
from random import randint
from MySql import Interface as MySql

from AbstractApp import AbstractApp
from FinderDb import Interface as FinderDb
import Github


class App(AbstractApp):

    def __init__(self):
        super().__init__()
        self.log = self.get_logger("Finder")
        self.log.debug("Starting MNDatus RepoFinder...")
        self.db = FinderDb()
        self.log.debug("Embedded database connection established.")
        self.sql = MySql(environ["MYSQL_HOST"],
                         environ["MYSQL_USER"],
                         environ["MYSQL_PASSWORD"])
        self.log.debug("MySQL server connection established.")
        self.sources = {
            "Github": Github
        }
        self.log.debug("Repository source interfaces loaded.")
        self.cycle_interval = int(environ["FINDER_CYCLE_INTERVAL"])
        self.check_interval = int(environ["TRENDING_REPO_CHECK_INTERVAL"])
        self.log.debug("MNDatus RepoFinder initialized.")

    def run_loop(self):
        while True:
            timestamp = datetime.now().timestamp()
            self.run()
            # Run loop throttling
            delta = datetime.now().timestamp() - timestamp
            if delta < self.cycle_interval:
                self.idle(duration=(self.cycle_interval - delta))
                
    def run(self):
        for source in self.sources.keys():
            timestamp = datetime.now().timestamp()
            delta = timestamp - self.db.time_since_last_check(source)
            if delta >= self.check_interval:
                self.log.debug(f"Checking {source} for new trending repos.")
                self.get_new_trending_repos(source)
                self.db.update_last_check(source, int(timestamp))

    def get_new_trending_repos(self, source):
        for repo in self.sources[source].get_trending_repos():
            if self.sql.repo_exists(repo):
                continue
            timestamp = int(datetime.now().timestamp())
            self.sql.add_repo(repo, timestamp)
            self.log.debug("New trending repo added to database.")


if __name__ == "__main__":
    app = App()
    app.run_loop()
