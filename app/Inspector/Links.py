#!/bin/python3
import os
import re
import requests
from time import sleep
from typing import List


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36",
    "Upgrade-Insecure-Requests": "1",
    "DNT": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate"
    }


def collect_urls(text):
    all_urls = re.findall("(?<=\()https?://[^\s\(\)\[\]]*(?=\))", text)
    urls = [url for url in all_urls
            if "github.com" not in url
            and "github.io" not in url
            and "localhost" not in url]
    return list(set(urls))


def check_link(url) -> str:
    sleep(1)
    try:
        resp = requests.get(url, headers=HEADERS, timeout=(5, 10))
        return str(resp.status_code)
    except:
        return "ERROR"


def check(text):
    return [(link, check_link(link)) for link in collect_urls(text)]
    

class Checker:

    def __init__(self):
        self.cache = {}

    def check(self, text):
        results = []
        urls = collect_urls(text)
        for url in urls:
            if url in self.cache.keys():
                result = self.cache[url]
            else:
                result = check_link(url)
                self.cache[url] = result
            results.append((url, result))
        return results

