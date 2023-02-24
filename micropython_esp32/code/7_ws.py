from microdot_asyncio import Microdot
import network
import uasyncio as asyncio
import gc

gc.collect()

ssid = "brnenske-pyvo"
password = "pyvopyvo"
a = 1
app = Microdot()


@app.route("/")
async def hello(request):
    return "<html><body>{}</body></html>".format(a), 200, {"Content-Type": "text/html"}


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

    asyncio.create_task(app.start_server(port=5000))

    while True:
        await asyncio.sleep(1)


asyncio.run(main())
