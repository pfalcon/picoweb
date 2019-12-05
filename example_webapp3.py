#
# This is a picoweb example showing a web page route
# specification using view decorators (Flask style)
# with an external asyncio event loop.
#
import logging
import picoweb
import uasyncio as asyncio

app = picoweb.WebApp(__name__)

@app.route("/")
def index(req, resp):
    yield from picoweb.start_response(resp)
    yield from resp.awrite("I can show you a table of <a href='squares'>squares</a>.\r\n")

@app.route("/squares")
def squares(req, resp):
    yield from picoweb.start_response(resp)
    yield from resp.awrite("Oh well, I lied\r\n")

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("picoweb")

print("creating server task")
app_server = app.get_server(debug = True, host = "0.0.0.0", port = 80, log = log)
loop = asyncio.get_event_loop()
loop.create_task(asyncio.start_server(*app_server))

print("run_forever()")
try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.close()
