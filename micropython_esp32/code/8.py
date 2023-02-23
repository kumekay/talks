from microdot_asyncio import Microdot
import network
import uasyncio as asyncio
import gc
import time
import neopixel
from machine import Pin
from math import sin, pi

gc.collect()

led_pin = Pin(2, Pin.OUT)
led = neopixel.NeoPixel(led_pin, 1)

ssid = "brnenske-pyvo"
password = "pyvopyvo"
a = 1
app = Microdot()


@app.route("/")
async def hello(request):
    return "<html><body>{}</body></html>".format(a), 200, {"Content-Type": "text/html"}


async def connect_wifi(ssid, password):
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    # 3 – WPA2-PSK
    ap.config(essid=ssid, password=password, authmode=3)
    return ap


from machine import Pin
import uasyncio as asyncio


class Button:
    def __init__(self, pin, on_press, on_release, debounce_ms=50, off_state=None):
        self.pin = pin
        self.on_press = on_press
        self.on_release = on_release
        self.debounce_ms = debounce_ms

        if off_state is None:
            off_state = pin.value()
        self.off_state = off_state

        self.state = self.raw_state()

        asyncio.create_task(self.update_state())

    def raw_state(self):
        return bool(self.pin.value() ^ self.off_state)

    async def update_state(self):
        while True:
            current_state = self.raw_state()

            if self.state != current_state:
                if current_state:
                    asyncio.create_task(self.on_press())
                else:
                    asyncio.create_task(self.on_release())
                self.state = current_state

            await asyncio.sleep_ms(self.debounce_ms)


async def add():
    global a
    a = a + 0.5


async def blink():
    while True:
        for i in range(360):
            led[0] = (
                abs(int(sin(i * pi / 180) * 64)),
                abs(int(sin((i + 45) * pi / 180) * 64)),
                abs(int(sin((i + 90) * pi / 180) * 64)),
            )
            led.write()
            await asyncio.sleep(0.01)


async def main():
    button = Pin(9, Pin.IN)
    Button(button, on_press=add, on_release=add, off_state=True)

    asyncio.create_task(blink())

    await asyncio.sleep(5)
    ap = await connect_wifi(ssid, password)
    print("IP:", ap.ifconfig()[0])

    asyncio.create_task(app.start_server(port=5000))

    while True:
        await asyncio.sleep(1)


asyncio.run(main())
