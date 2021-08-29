#! /usr/bin/env python

import timeit
import urllib.request
import concurrent.futures


def download_cat(cat_id, n=5):
    for _ in range(n):
        with urllib.request.urlopen(f"http://localhost:8000/{cat_id}.jpg") as response:
            response.read()


def down_them_all():
    # python 3.2+
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as runner:
        runner.map(download_cat, range(1, 21))


if __name__ == "__main__":
    time = timeit.timeit(down_them_all, number=1)
    print(f"Duration {time} seconds")
