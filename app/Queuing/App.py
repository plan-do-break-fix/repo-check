#~/bin/python3
# Queueing v1.0
from datetime import datetime
from hashlib import md5
import json
from os import environ
from time import sleep
from typing import List, Tuple

from MySql import Interface as MySql
from RabbitMq import Interface as RabbitMq

from AbstractApp import AbstractApp
from Github import repo_url_to_name
import GithubApi
import LocalRepo


class App(AbstractApp):

    def __init__(self):
        super().__init__()
        self.log = self.get_logger("Queueing")
        self.log.debug("Starting Queueing...")
        self.mq = RabbitMq(environ["RMQ_HOST"],
                           environ["RMQ_USER"],
                           environ["RMQ_PASSWORD"])
        self.log.debug("Inspection queue connection established.")
        self.sql = MySql(environ["MYSQL_HOST"],
                         environ["MYSQL_USER"],
                         environ["MYSQL_PASSWORD"])
        self.log.debug("MySQL server connection established.")
        self.cycle_interval = int(environ["QUEUING_CYCLE_INTERVAL"])
        #self.repo_watch_interval = int(environ["REPO_WATCH_INTERVAL"])
        self.doc_exts = ["html", "md"]
        self.full_queue_size = int(environ["FULL_QUEUE_SIZE"])
        self.log.debug("Repo Check Queueing initialized.")

    def run_loop(self):
        while True:
            timestamp = int(datetime.now().timestamp())
            n_jobs = self.mq.message_count('inspection')
            self.log.debug(f"Currently {n_jobs} jobs in inspections queue.")
            if n_jobs >= self.full_queue_size:
                self.log.debug(f"Inspection queue is full.")
                self.idle(duration=self.cycle_interval)
            else:
                self.fill_queue()
            # Run loop throttling
            delta = self.cycle_interval - (datetime.now().timestamp() - timestamp)
            if delta > 0:
                self.idle(duration=int(delta))

    def fill_queue(self):
        #_count = self.find_watched_repo_jobs()
        #self.log.debug(f"{_count} watched repo jobs added to inspection queue.")
        for job in self.make_new_repo_jobs():
            self.submit_job(job)
        if self.mq.message_count("inspection") < 10:
            self.log.debug(f"Inspection queue running low after filling.")
        
    def make_watched_repo_jobs(self) -> int:
        jobs_added = 0
        cutoff_time = int(datetime.now().timestamp() - self.repo_watch_interval)
        repo_visits: List[Tuple] = self.sql.get_watched_repo_visit_times(cutoff=cutoff_time)
        for repo_url, timestamp in repo_visits:
            new_prs = GithubApi.get_prs_since(repo_url_to_name(repo_url), timestamp)
            if not new_prs:
                self.sql.record_inspection(repo_url, datetime.now().timestamp(), "none")
                break
            file_list = [_f for _pr in new_prs for _f in GithubApi.get_files_in_pr(_r)]
            file_list = LocalRepo.filter_by_type(file_list, self.doc_exts)
            if not file_list:
                self.sql.record_inspection(repo_url, datetime.now().timestamp(), "none")
                break
            job = {"repo_url": repo_url,
                   #"repo_type": None,  # overridden by file_list
                   "file_list": file_list}
            self.submit_job(job)
            jobs_added += 1
        return jobs_added

    def make_new_repo_jobs(self) -> int:
        self.log.debug("Checking database for unvisited repositories.")
        unvisited_repos = self.sql.get_unvisited_repos()
        self.log.debug(f"{len(unvisited_repos)} unvisited repositories found.")
        return [{"repo_url": repo_url,
                #"repo_type": None,
                "file_list": None}
                for repo_url in unvisited_repos]

    def submit_job(self, job) -> bool:
        """
        Submits job to inspection queue and marks the repo as checked out.
        Check out prevents duplication of jobs in the inspection queue.
        """
        job["created"] = int(datetime.now().timestamp())
        self.mq.enqueue(json.dumps(job), "inspection")
        self.sql.check_out(job["repo_url"])
        self.log.debug(f"{job['repo_url']} submitted to inspection queue.")
        return True


if __name__ == "__main__":
    app = App()
    app.run_loop()
