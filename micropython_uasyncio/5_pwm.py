import gc
import time
import uasyncio as asyncio
from machine import PWM, Pin

gc.collect()

EN_PINS = (
    Pin(27, Pin.OUT),
    Pin(25, Pin.OUT),
)
PWM_PINS = (
    Pin(32, Pin.OUT),
    Pin(26, Pin.OUT),
)

PWMS = [PWM(pin, freq=20000, duty=0) for pin in PWM_PINS]

BUTTON_PINS = (
    Pin(18, Pin.IN, Pin.PULL_UP),  # Down
    Pin(19, Pin.IN, Pin.PULL_UP),  # Up
)

duty = 400


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


async def move(up=False):
    print("moving {} @ {}".format("up" if up else "down", duty))
    PWMS[int(up)].duty(duty)


async def down():
    await move(up=False)


async def up():
    await move(up=True)


async def stop():
    print("stop")
    for pwm in PWMS:
        pwm.duty(0)


async def main():
    # Enable motors
    for pin in EN_PINS:
        pin.on()

    Button(BUTTON_PINS[0], on_press=down, on_release=stop, off_state=True)
    Button(BUTTON_PINS[1], on_press=up, on_release=stop, off_state=True)

    # Keep alive
    while True:
        await asyncio.sleep(1)


try:
    asyncio.run(main())
except (KeyboardInterrupt, Exception) as e:
    print("Exception {}".format(e))
finally:
    asyncio.new_event_loop()
