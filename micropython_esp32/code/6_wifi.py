import network
import uasyncio as asyncio
import gc

gc.collect()

ssid = "brnenske-pyvo"
password = "pyvopyvo"


async def connect_wifi(ssid, password):
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    # 3 – WPA2-PSK
    ap.config(essid=ssid, password=password, authmode=3)
    return ap


async def main():
    await asyncio.sleep(5)
    ap = await connect_wifi(ssid, password)
    print("IP:", ap.ifconfig()[0])

    while True:
        await asyncio.sleep(1)


asyncio.run(main())
