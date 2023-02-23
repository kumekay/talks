from machine import Pin


def button_callback(pin):
    print("Button pressed - IRQ")


button = Pin(9, Pin.IN)
button.irq(trigger=Pin.IRQ_FALLING, handler=button_callback)
