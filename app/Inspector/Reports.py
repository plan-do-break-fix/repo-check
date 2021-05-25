#!/bin/python3

def summarize(findings: dict) -> dict:
    all_typos = list(set([_t for _doc in findings.keys()
                             for _t in findings[_doc]["typos"]]))
    all_bad_links = list(set([_t for _doc in findings.keys()
                        for _t in findings[_doc]["bad_links"]]))
    all_typos.sort()
    return {
        "count_typos": len(all_typos),
        "typos": all_typos,
        "count_bad_links": len(all_bad_links),
        "bad_links": all_bad_links
    }


def metadata(repo_url: str, timestamp: int, version: str, job, inspected_files):
    return {
        "repo_url": repo_url,
        "created": timestamp,
        "version": version,
        "status": "new",
        "last_viewed": None,
        "job": job,
        "inspected_files": inspected_files
    }


def details(findings: dict) -> dict:
    details = {}
    for _doc in findings.keys():
        _encoded = _doc.replace(".", "U+FF0E")        
        if findings[_doc]["typos"] or findings[_doc]["bad_links"]:
            details[_encoded] = {}
        if findings[_doc]["typos"]:
            details[_encoded]["typos"] = findings[_doc]["typos"]
        if findings[_doc]["bad_links"]:
            details[_encoded]["bad_links"] = findings[_doc]["bad_links"]
    return details


def prepare_report(metadata, summary, details):
    return {
        "metadata": metadata,
        "data": {
            "summary": summary,
            "details": details
        }
    }
    

