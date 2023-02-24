from machine import Pin
import uasyncio as asyncio


async def button_task():
    button = Pin(9, Pin.IN)
    while True:
        if button.value() == 0:
            print("Button pressed - Async")
            await asyncio.sleep(0.1)


asyncio.run(button_task())
