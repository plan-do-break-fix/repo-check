#!/bin/python3

from pymongo import MongoClient

class Interface:

    def __init__(self, host):
        self.client = MongoClient(host, 27017)
        self.db = self.client.report
        self.collection = self.db.inspection

    def write_report(self, report):
        self.collection.insert_one(report).inserted_id

    def get_report(self, report_id):
        query = {"metadata": {"repo_url": repo_url, "timestamp": timestamp}}
        return self.collection.find_one(query)

    def update_report_status(self, repo_url, created, status, timestamp):
        query = {"metadata": {"repo_url": repo_url, "created": created}}
        data = {"metadata": {"status": new_status, "last_viewed": timestamp}}
        self.collection.update_one(query, data)

    