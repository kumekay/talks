from math import pi, sin

import neopixel
import uasyncio as asyncio
from machine import Pin

led_pin = Pin(33, Pin.OUT)
led = neopixel.NeoPixel(led_pin, 1)


async def set_color():
    while True:
        for i in range(360):
            led[0] = (
                abs(int(sin(i * pi / 180) * 64)),
                abs(int(sin((i + 45) * pi / 180) * 64)),
                abs(int(sin((i + 90) * pi / 180) * 64)),
            )
            led.write()
            await asyncio.sleep_ms(50)


async def main():
    asyncio.create_task(set_color())
    while True:
        print("Hello Espressif!")
        await asyncio.sleep(5)


try:
    asyncio.run(main())
except (KeyboardInterrupt, Exception) as e:
    print("Exception {}".format(type(e).__name__))
finally:
    asyncio.new_event_loop()
