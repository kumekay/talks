import espnow
import network
from machine import Pin
import json
import neopixel


LED_PIN = 18


def set_color(led, rgb):
    led[0] = rgb
    led.write()
    print("RGB: ", rgb)


def main():
    # Init LED
    led_pin = Pin(LED_PIN, Pin.OUT)
    led = neopixel.NeoPixel(led_pin, 1)

    # Init espnow with broadcast
    sta = network.WLAN(network.STA_IF)
    sta.active(True)

    enow = espnow.ESPNow()
    enow.active(True)

    while True:
        _host, msg = enow.recv()
        if msg:  # msg == None if timeout in recv()
            rgb = json.loads(msg.decode("utf-8"))
            set_color(led, rgb)


main()
