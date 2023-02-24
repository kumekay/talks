from machine import Pin
import time

button = Pin(9, Pin.IN)

while True:
    if button.value() == 0:
        print("Button pressed")
    else:
        print("Button released")

    time.sleep(0.1)
