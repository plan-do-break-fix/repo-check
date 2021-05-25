#!/bin/python3
import requests
import shutil
from typing import List
from zipfile import ZipFile

def clean_up():
    try:
        shutil.os.remove("/tmp/master.zip")
    except FileNotFoundError:
        pass
    try:
        shutil.rmtree("/tmp/master")
    except FileNotFoundError:
        pass
    return True

def expand_repo():
    try:
        with ZipFile("/tmp/master.zip") as _zip:
            _zip.extractall(path="/tmp/master")
        return True
    except FileNotFoundError:
        return False

def all_files():
    """Returns a list of all files in the working repo."""
    output = []
    for root, dirs, files in shutil.os.walk("/tmp/master"):
        for _f in files:
            output.append(shutil.os.path.join(root, _f))
    return output

def filter_by_type(files: List, exts: List) -> List[str]:
    return [_f for _f in files
            if _f.split(".")[-1].lower() in exts]

def filter_by_has_substring(files: List, substrings: List):
    return list(set([_f for _f in files 
                     for _string in substrings
                     if _string.lower() in _f.lower()]))

def filter_by_hasnt_substring(files: List, substrings: List):
    return list(set([_f for _f in files 
                     if not any(
                       [_string.lower() in _f.lower()
                       for _string in substrings])
                    ]))

def filter_by_max_depth(files: List, depth: int):
    """
    depth: Maximum depth of file in directory heirarchy. A depth of 0 is the
           repository's root folder.
    """
    return [_f for _f in files if len(_f.split("/")) <= 5 + depth] # 5 should be read dynamically from $APP_PATH

THIRD_PARTY_PATH = [
    "/vendor/"
]

def filter_third_party(files: List) -> List[str]:
    return [_f for _f in files if not any([word in _f for word in words])]



def lines(fpath):
    with open(fpath, "r") as _f:
        return _f.readlines()

def text(fpath):
    return " ".join(lines(fpath))

