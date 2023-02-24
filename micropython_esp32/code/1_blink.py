import time
import neopixel
from machine import Pin
from math import sin, pi

led_pin = Pin(2, Pin.OUT)
led = neopixel.NeoPixel(led_pin, 1)


def main():
    while True:
        print(time.time())
        for i in range(360):
            led[0] = (
                abs(int(sin(i * pi / 180) * 64)),
                abs(int(sin((i + 45) * pi / 180) * 64)),
                abs(int(sin((i + 90) * pi / 180) * 64)),
            )
            led.write()
            time.sleep(0.01)


main()
