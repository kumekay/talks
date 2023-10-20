import aioespnow
import network

from machine import Pin
import asyncio
import json
import neopixel

import hmac
import hashlib

KEY = b"secret plaintext key"


LED_PIN = 18


def set_color(led, rgb):
    led[0] = rgb
    led.write()
    print("RGB: ", rgb)


async def listener(enow, led):
    async for _mac, msg in enow:
        data = json.loads(msg.decode("utf-8"))
        code = data.get("hmac")
        rgb = data.get("rgb")
        rgb_json = json.dumps(data.get("rgb")).encode("utf-8")
        if hmac.new(KEY, rgb_json, hashlib.sha256).hexdigest() != code:
            print("Invalid HMAC")
            continue

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
