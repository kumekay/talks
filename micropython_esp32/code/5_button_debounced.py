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


async def press():
    print("Button pressed")


async def release():
    print("Button released")


async def main():
    button = Pin(9, Pin.IN)
    Button(button, on_press=press, on_release=release, off_state=True)

    # Keep alive
    while True:
        await asyncio.sleep(1)


try:
    asyncio.run(main())
except (KeyboardInterrupt, Exception) as e:
    print("Exception {}".format(e))
finally:
    asyncio.new_event_loop()
