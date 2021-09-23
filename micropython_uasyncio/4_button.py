from machine import PWM, Pin
import uasyncio as asyncio

EN_L = Pin(27, Pin.OUT)
EN_R = Pin(25, Pin.OUT)
PWM_L = Pin(32, Pin.OUT)
PWM_R = Pin(26, Pin.OUT)
BUTTON_DOWN = Pin(18, Pin.IN, Pin.PULL_UP)
BUTTON_UP = Pin(19, Pin.IN, Pin.PULL_UP)


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


async def down():
    PWM_L.off()
    PWM_R.on()


async def up():
    PWM_L.on()
    PWM_R.off()


async def stop():
    PWM_L.off()
    PWM_R.off()


async def main():
    # Enable motors
    EN_L.on()
    EN_R.on()

    Button(BUTTON_DOWN, on_press=down, on_release=stop, off_state=True)
    Button(BUTTON_UP, on_press=up, on_release=stop, off_state=True)

    # Keep alive
    while True:
        await asyncio.sleep(1)


try:
    asyncio.run(main())
except (KeyboardInterrupt, Exception) as e:
    print("Exception {}".format(e))
finally:
    asyncio.new_event_loop()
