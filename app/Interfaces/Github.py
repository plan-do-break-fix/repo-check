#!/bin/python3
from os import environ
import requests
from time import sleep


def download_repo(repo_url) -> bool:
    url = f"{repo_url}/archive/refs/heads/master.zip"
    resp = requests.get(url, stream=True)
    if resp.status_code == 200:
        with open(f"/tmp/master.zip", "wb") as _f:
            for chunk in resp.iter_content(chunk_size=128):
                _f.write(chunk)
    return True

# Filename utilities
def repo_name_to_url(repo_name: str) -> str:
    return f"https://github.com/{repo_name}"

def repo_url_to_name(repo_url: str) -> str:
    return "/".join(repo_url.split("/")[-2:])

# Trending repo methods
from bs4 import BeautifulSoup
LANGUAGES = [
    "asp.net",
    "assembly",
    "c",
    "c++",
    "c%23",
    "clojure",
    "cobol",
    "common-lisp",
    "cuda",
    "dart",
    "elixir",
    "f%23",
    "go",
    "graphql",
    "groovy",
    "haskell",
    "html",
    "jinja",
    "java",
    "javascript",
    "julia",
    "jupyter-notebook",
    "kotlin",
    "lua",
    "markdown",
    "nginx",
    "numpy",
    "perl",
    "php",
    "powershell",
    "puppet",
    "python",
    "r",
    "ruby",
    "rust",
    "scala",
    "shell",
    "typescript",
    "webassembly"
]
GITHUB = "https://github.com"
TRENDING = "https://github.com/trending/{}?since={}"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36",
    "Upgrade-Insecure-Requests": "1",
    "DNT": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate"
}

def get_trending_repos():
    """Return trending repo URLs for each langauge in LANGUAGES."""
    repo_urls = []
    for lang in LANGUAGES:
        page_url = TRENDING.format(lang, "daily")
        resp = requests.get(page_url, headers=HEADERS)
        if not resp or resp.status_code != 200:
            raise RuntimeError
        soup = BeautifulSoup(resp.content, features="html5lib")
        repo_urls += collect_repo_urls(soup)
        sleep(2)
    return list(set(output))

def collect_repo_urls(soup: BeautifulSoup) -> List[str]:
    repo_hrefs = [_l.find("a").attrs["href"] for _l in
                     soup.find_all("article", {"class": "Box-row"})]
    repo_hrefs = filter(is_not_sponsored, repo_hrefs)
    repo_hrefs = map(remove_login_redirect, repo_hrefs)
    return [f"{GITHUB}{_l}" for _l in repo_hrefs]

def remove_login_redirect(href: str) -> str:
    return href.replace("/login?return_to=", "").replace("%2F", "/")

def is_not_sponsored(href: str) -> bool:
    return False if href.startswith("https://github.com/sponsors/") else True

