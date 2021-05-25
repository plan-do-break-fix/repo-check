#!/bin/python3
import requests

from bs4 import BeautifulSoup

TOPICS = [
    "awesome",
    "aws",
    "cli",
    "collections",
    "community",
    "console",
    "containers",
    "css",
    "curriculum",
    "database",
    "debugging",
    "demo",
    "deployment",
    "devops",
    "docker",
    "editor",
    "education",
    "example",
    "framework",
    "git",
    "guide",
    "hackathon",
    "learning",
    "linux",
    "list",
    "lists",
    "logging",
    "math",
    "monitoring",
    "programming",
    "resource",
    "security",
    "style-guide",
    "styleguide",
    "tensorflow",
    "test",
    "tutorial",
    "tutorials",
    "utilities",
    "web"
]
MIN_STARS = 5
TRENDING = "https://gitlogs.com/most_popular?from={}&topic={}"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36",
    "Upgrade-Insecure-Requests": "1",
    "DNT": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate"
}

def get_trending_repos():
    repo_urls = []
    for topic in TOPICS:
        page_url = TRENDING.format("last-week", topic)
        resp = requests.get(page_url, headers=HEADERS)
        if not resp or resp.status_code != 200:
            raise RuntimeError
        soup = BeautifulSoup(resp.content, features="html5lib")
        repo_urls += collect_repo_urls(soup)
        sleep(2)
    return list(set(output))

def collect_repo_urls(soup):
    repo_tags = soup.find_all("div", {"class": "resource"})
    repo_tags = filter(has_min_stars, repo_tags)
    return [_rt.find("a", {"target": "preview"}).attrs["href"]
            for _rt in repo_tags]

def has_min_stars(repo_tag) -> bool:
    stars = repo_tag.find("span", {"class": "badge"}).find("span").text
    return int(stars) >= MIN_STARS
