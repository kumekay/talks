import gc
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


class Motor:
    def __init__(self):
        self.direction = 0
        self.should_stop = asyncio.Event()
        self.moving_task = None
        asyncio.create_task(self.stop())

    async def move(self, up=False):
        self.moving_task = asyncio.current_task()
        if self.direction == 0:
            self.direction = 1 if up else -1
            for duty in range(400, 950, 50):
                PWMS[int(up)].duty(duty)
                print("moving {} @ {}".format("up" if up else "down", duty))
                await asyncio.sleep_ms(100)

    async def down(self):
        await self.move(up=False)

    async def up(self):
        await self.move(up=True)

    async def stop(self):
        while True:
            await self.should_stop.wait()
            print("stop")
            for pwm in PWMS:
                pwm.duty(0)
            self.direction = 0
            if self.moving_task:
                self.moving_task.cancel()
            self.should_stop.clear()

    async def stop_down(self):
        if self.direction == -1:
            self.should_stop.set()

    async def stop_up(self):
        if self.direction == 1:
            self.should_stop.set()


async def main():
    # Enable motors
    for pin in EN_PINS:
        pin.on()

    motor = Motor()
    Button(
        BUTTON_PINS[0], on_press=motor.down, on_release=motor.stop_down, off_state=True
    )
    Button(BUTTON_PINS[1], on_press=motor.up, on_release=motor.stop_up, off_state=True)

    # Keep alive
    while True:
        await asyncio.sleep(1)


try:
    asyncio.run(main())
except (KeyboardInterrupt, Exception) as e:
    print("Exception {}".format(e))
finally:
    asyncio.new_event_loop()
