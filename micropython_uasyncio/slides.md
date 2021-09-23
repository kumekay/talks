---
marp: true
paginate: true
---

# Friday Technology talk - _Sergei Silnov_ - 24.09.2021

## Practical micropython with uasyncio for ESP32

---

## [Micropython](https://micropython.org/)

- light and efficient: 256k of code space and 16k of RAM
- core language: 3.4 + selected features from 3.5/3.6/3.7 (including async/await keywords)
- some parts of standard library
- micropython specific and port specific libraries

---

## Nice things

- Supports all Espressif chips: esp8266/esp32/s2/c3/s3
- EmbREPL / Web REPL / mpremote

---

## Let's hello blink

- Download from https://micropython.org/download/esp32/
- Flash
  `esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 esp32-20180511-v1.9.4.bin`
- `pip install mpremote`

---

## Let's solve a real problem

---

![bg fit](images/desk_0.png)

---

![bg fit](images/desk_1.png)

---

![bg fit](images/motor.jpg)

---

- micropython docs https://docs.micropython.org/en/latest/
- micropython forum https://forum.micropython.org/
