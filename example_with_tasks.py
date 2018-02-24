#
# This is a picoweb example showing a web page and async task
#
import picoweb
import uasyncio

app = picoweb.WebApp(__name__)
data = {'counter': 0}


@app.route("/")
def index(req, resp):
    yield from picoweb.start_response(resp)
    yield from resp.awrite("seconds timer: %d" % data['counter'])


def click_clock():
    # or async def click_clock(): in python 3.5
    while True:
        data['counter'] += 1
        yield from uasyncio.sleep(1) 
        # or await uasyncio.sleep(1) in python3.5


import logging
logging.basicConfig(level=logging.INFO)

loop = uasyncio.get_event_loop()
loop.create_task(click_clock())
loop.create_task(app.init_as_task(host='0.0.0.0', port=80))
loop.run_forever()
loop.close()
