#! /usr/bin/env python

import timeit
import urllib.request


def download_cat(cat_id, n=5):
    for _ in range(n):
        with urllib.request.urlopen(f"http://localhost:8000/{cat_id}.jpg") as response:
            response.read()


def naive():
    [download_cat(n + 1) for n in range(20)]


if __name__ == "__main__":
    time = timeit.timeit(naive, number=1)
    print(f"Duration {time} seconds")
