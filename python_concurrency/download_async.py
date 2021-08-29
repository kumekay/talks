#! /usr/bin/env python

import time
import asyncio
import aiohttp

# async/await is python 3.5+
async def download_cat(cat_id, n=5):
    async def download_one():
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://localhost:8000/{cat_id}.jpg") as response:
                await response.read()

    await asyncio.gather(*[download_one() for _ in range(n)])


async def down_them_all():
    await asyncio.gather(*[download_cat(n + 1) for n in range(20)])


if __name__ == "__main__":
    start = time.time()
    # python 3.7+

    asyncio.run(down_them_all())

    # python 3.4+
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())

    duration = time.time() - start
    print(f"Duration {duration} seconds")
