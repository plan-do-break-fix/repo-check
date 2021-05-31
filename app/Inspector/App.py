#!/bin/python3
# Repo Check - Inspector v1.0
VER = "1.0"  # Inspector version logged in report metadata
from datetime import datetime
import json
from os import environ
from typing import List, Tuple, Union

from Mongo import Interface as Mongo
from MySql import Interface as MySql
from RabbitMq import Interface as RabbitMq

from AbstractApp import AbstractApp
import Links
import LocalRepo
import Github
from Pedant import Pedant
import Reports


class App(AbstractApp):

    def __init__(self):
        super().__init__()
        self.log = self.get_logger("Inspector")
        self.log.debug("Starting Repo Check Inspector...")
        self.pedant = Pedant()
        self.mq = RabbitMq(environ["RMQ_HOST"],
                           environ["RMQ_USER"],
                           environ["RMQ_PASSWORD"])
        self.log.debug("Inspection queue connection established.")
        self.sql = MySql(environ["MYSQL_HOST"],
                         environ["MYSQL_USER"],
                         environ["MYSQL_PASSWORD"])
        self.log.debug("MySQL server connection established.")
        self.mongo = Mongo(environ["MONGO_HOST"])
        self.log.debug("MongoDB server connection established.")
        self.idle_interval = int(environ["INSPECTOR_IDLE_INTERVAL"])
        self.doc_exts = [   # file exts that are inspected
            "html",
            "md"
        ]
        self.third_party_paths = [  # ignored
            "/vendor/"
        ]
        self.log.debug("Starting Inspector...")

    def run_loop(self):
        while True:
            job = self.get_job()
            self.run(job) if job else self.idle()

    def run(self, job):
        repo_url, repo_name = job["repo_url"], Github.repo_url_to_name(job["repo_url"])
        self.log.debug(f"Inspecting {repo_name}.")
        timestamp = int(datetime.now().timestamp())
        if not self.make_local_repo(repo_url):
            self.log.error(f"Unable to make local copy of {repo_name}.")
            self.sql.record_inspection(repo_url, timestamp, "error")
            self.sql.check_in(repo_url)
            return None
        to_inspect = self.make_inspection_list(job)
        if to_inspect == []:
            self.log.debug(f"Found nothing to inspect.")
            self.sql.record_inspection(repo_url, timestamp, "none")
            self.sql.check_in(repo_url)
            return None
        findings = self.inspect_docs(to_inspect)
        self.log.debug(findings)
        if findings == False:
            self.log.error(f"Unable to inspect {repo_name}.")
            self.sql.record_inspection(repo_url, timestamp, "error")
            self.sql.check_in(repo_url)
            return None
        summary = Reports.summarize(findings)
        if summary["count_typos"] == summary["count_bad_links"] == 0:
            self.log.debug(f"Zero findings for {repo_name}.")
            self.sql.record_inspection(repo_url, timestamp, "none")
            self.sql.check_in(repo_url)
            return None
        metadata = Reports.metadata(repo_url, timestamp, VER, job, to_inspect) 
        details = Reports.details(findings)
        report = Reports.prepare_report(metadata, summary, details)
        self.mongo.write_report(report)
        self.log.debug(f"Report written for {repo_name}.")
        self.sql.record_inspection(repo_url, timestamp, "report")
        self.sql.check_in(repo_url)
        self.log.debug(f"Inspection of {repo_name} completed and logged.")
        return None

    def get_job(self) -> Union[dict, bool]:
        """Return an inspection job from the inspections queue or False if the
           queue is empty."""
        job = self.mq.dequeue("inspection")
        return False if not job else json.loads(job)

    def make_local_repo(self, repo_url) -> bool:
        """Downloads repo zip file to /tmp and expands."""
        repo_name = Github.repo_url_to_name(repo_url)
        LocalRepo.clean_up()
        if not Github.download_repo(repo_url):
            self.log.error(f"Failed to download {repo_name}.")
            return False
        self.log.debug(f"{repo_name} downloaded to local storage.")
        LocalRepo.expand_repo()
        return True

    def make_inspection_list(self, job: dict) -> List[str]:
        """Return list of files to inspect."""
        if not job["file_list"]:
            file_list = LocalRepo.filter_by_type(
                            LocalRepo.all_files(), self.doc_exts)
        else:
            file_list = job["file_list"]
        file_list = LocalRepo.filter_by_hasnt_substring(file_list, 
                                                        self.third_party_paths)
        return file_list

    def inspect_docs(self, file_list) -> Tuple[dict, List]:
        """Return findings dictionary for indicated files."""
        self.log.debug(f"Analyzing {len(file_list)} files.")
        link_checker = Links.Checker()
        findings = { _doc: {
                        "bad_links": link_checker.check(LocalRepo.text(_doc)),
                        "typos": self.pedant.check(LocalRepo.text(_doc))
                    } for _doc in file_list}
        return findings


if __name__ == "__main__":
    app = App()
    app.run_loop()
