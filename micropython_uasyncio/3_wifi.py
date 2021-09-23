import time

import neopixel
import network
import uasyncio as asyncio
from machine import Pin

led_pin = Pin(33, Pin.OUT)
led = neopixel.NeoPixel(led_pin, 1)


async def blink():
    b = 10
    while True:
        led[0] = (0, b, 0)
        b = b ^ 10
        led.write()
        await asyncio.sleep_ms(20)


async def connect_wifi(ssid, password):
    start = time.ticks_us()
    wlan = network.WLAN(network.STA_IF)
    print(f"Create WLAN", time.ticks_us() - start)
    await asyncio.sleep_ms(0)
    wlan.active(True)
    print(f"WLAN active", time.ticks_us() - start)
    if not wlan.isconnected():
        wlan.connect(ssid, password)
        print(f"WLAN connect", time.ticks_us() - start)
        while not wlan.isconnected():
            await asyncio.sleep_ms(10)

    return wlan


async def main():
    asyncio.create_task(blink())
    await asyncio.sleep_ms(500)
    await connect_wifi("SSID", "WIFI_PASS")


try:
    asyncio.run(main())
except (KeyboardInterrupt, Exception) as e:
    print("Exception {}".format(type(e).__name__))
finally:
    asyncio.new_event_loop()
