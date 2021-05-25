#!/bin/python3
from datetime import datetime
from os import environ
from typing import List

from github import Github
from github.PullRequest import PullRequest
from github.Repository import Repository

def authenticate():
    return Github(login_or_token=environ["GITHUB_TOKEN"],
                  password=environ["GITHUB_SECRET"])

def get_prs_since(repo_name, since: datetime) -> List[PullRequest]:
    g = authenticate()
    prs = g.get_repos(repo_name).get_pulls()
    return [pr for pr in prs if pr.created_at > since]

def get_files_in_pr(pr: PullRequest) -> List[str]:
    prs = get_prs_since(repo_url, since)
    return [_f.filename for pr in prs for _f in pr.get_files()]

def get_repos_changed_since(org_url, since: datetime) -> List[Repository]:
    g = authenticate()



