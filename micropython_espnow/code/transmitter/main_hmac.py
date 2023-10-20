from machine import Pin
import asyncio
from encoder import Encoder
import neopixel
import network
import json
import aioespnow

import hmac
import hashlib


BUTTON_PIN = 9
LED_PIN = 8
ENCODER_PIN_A = 6
ENCODER_PIN_B = 10

KEY = b"secret plaintext key"

# Broadcast address
PEER = b"\xbb\xbb\xbb\xbb\xbb\xbb"


class g:
    """Class used as a storage of global state"""

    # RGB
    # ^^^
    # 012
    current_color = 0
    rgb = [0, 0, 0]


async def next_color(led):
    # Set current color to the next one
    g.current_color = (g.current_color + 1) % 3
    # Set LED the color
    await set_color(led, [50 if i == g.current_color else 0 for i in range(3)])
    await asyncio.sleep(0.5)
    await set_color(led, g.rgb)


async def button_task(button, led):
    while True:
        if button.value() == 0:
            await asyncio.sleep(0.05)
            if button.value() == 0:
                await next_color(led)
                await asyncio.sleep(0.5)
        await asyncio.sleep(0.05)


async def set_color(led, rgb):
    led[0] = rgb
    led.write()
    print("RGB: ", rgb)


async def send_color(enow, rgb):
    rgb_json = json.dumps(rgb).encode("utf-8")
    digest = hmac.new(KEY, rgb_json, hashlib.sha256).hexdigest()
    await enow.asend(PEER, json.dumps({"rgb": rgb, "hmac": digest}))


def set_color_cb(_pos, delta, led, enow):
    g.rgb[g.current_color] = max(0, min(255, g.rgb[g.current_color] + delta))
    asyncio.create_task(send_color(enow, g.rgb))
    asyncio.create_task(set_color(led, g.rgb))


async def main():
    print("Starting...")

    led_pin = Pin(LED_PIN, Pin.OUT)
    led = neopixel.NeoPixel(led_pin, 1)

    py = Pin(ENCODER_PIN_A, Pin.IN, Pin.PULL_UP)
    px = Pin(ENCODER_PIN_B, Pin.IN, Pin.PULL_UP)

    button = Pin(BUTTON_PIN, Pin.IN)
    asyncio.create_task(button_task(button, led))

    # A WLAN interface must be active to send()/recv()
    network.WLAN(network.STA_IF).active(True)

    enow = aioespnow.AIOESPNow()  # Returns AIOESPNow enhanced with async support
    enow.active(True)
    enow.add_peer(PEER)

    Encoder(px, py, v=0, vmin=0, vmax=255, callback=set_color_cb, args=(led, enow))

    while True:
        await asyncio.sleep(1)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Interrupted")
finally:
    asyncio.new_event_loop()
