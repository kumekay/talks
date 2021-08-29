#! /usr/bin/env python

import timeit
import concurrent.futures
import requests
import threading

thread_local = threading.local()


def download_cat(cat_id, n=5):
    try:
        session = thread_local.session
    except AttributeError:
        session = requests.Session()

    for _ in range(n):
        with session.get(f"http://localhost:8000/{cat_id}.jpg") as response:
            response.content


def down_them_all():
    # python 3.2+
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as runner:
        runner.map(download_cat, range(1, 21))


if __name__ == "__main__":
    time = timeit.timeit(down_them_all, number=1)
    print(f"Duration {time} seconds")
