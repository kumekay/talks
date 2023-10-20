import aioespnow
import network

from machine import Pin
import asyncio
import json
import neopixel


LED_PIN = 18


def set_color(led, rgb):
    led[0] = rgb
    led.write()
    print("RGB: ", rgb)


async def listener(enow, led):
    async for _mac, msg in enow:
        rgb = json.loads(msg.decode("utf-8"))
        set_color(led, rgb)


async def main():
    # Init LED
    led_pin = Pin(LED_PIN, Pin.OUT)
    led = neopixel.NeoPixel(led_pin, 1)

    # Init espnow with broadcast
    sta = network.WLAN(network.STA_IF)
    sta.active(True)

    enow = aioespnow.AIOESPNow()
    enow.active(True)

    await asyncio.create_task(listener(enow, led))


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Interrupted")
finally:
    asyncio.new_event_loop()
