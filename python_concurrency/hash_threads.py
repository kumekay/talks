#! /usr/bin/env python

import timeit
import hashlib
import concurrent.futures
from uuid import uuid4


def hash_me(n=500_000):
    data = uuid4().bytes
    for _ in range(n):
        data = hashlib.sha256(data).digest()


def calc_them_all():
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as runner:
        [runner.submit(hash_me) for _ in range(20)]


if __name__ == "__main__":
    time = timeit.timeit(calc_them_all, number=1)
    print(f"Duration {time} seconds")
