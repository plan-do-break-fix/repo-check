#!/bin/python3
from nltk.tokenize import word_tokenize


class Pedant:

    def __init__(self):
        with open("typos.txt", "r") as _f:
            lines = _f.readlines()
            self.corrections = {line.split("->")[0].strip():
                                line.split("->")[1].strip()
                                for line in lines}

    def check(self, text):
        words = word_tokenize(text)
        typos = [(word, self.corrections[word]) for word in words
                 if word in self.corrections.keys()]
        return list(set(typos))
