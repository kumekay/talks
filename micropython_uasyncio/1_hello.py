try:
    import asyncio

    print("I'm big one")
except ImportError:
    import uasyncio as asyncio

    print("I'm micro")


async def main():
    while True:
        print("Hello Espressif!")
        await asyncio.sleep(1)


try:
    asyncio.run(main())
except (KeyboardInterrupt, Exception) as e:
    print("Exception {}".format(type(e).__name__))
finally:
    asyncio.new_event_loop()
