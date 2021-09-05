# Practical micropython with uasyncio for ESP32

## Let's connect to WiFi

```python
import gc
import network
import uasyncio as asyncio

gc.collect()

async def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            asyncio.sleep_ms(10)

async def main():
    await connect_wifi("SSID", "WIFI_PASS")

try:
    asyncio.run(main())
except (KeyboardInterrupt, Exception) as e:
    sys.print_exception(e)
finally:
    asyncio.stop()
```
