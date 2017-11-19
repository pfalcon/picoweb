#
# This is a picoweb example showing a Server Side Events (SSE) aka
# EventSource handling. Each connecting client gets its own events,
# independent from other connected clients.
#
import uasyncio
import picoweb


def index(req, resp):
    yield from picoweb.start_response(resp)
    yield from resp.awrite("""\
<!DOCTYPE html>
<html>
<head>
<script>
var source = new EventSource("events");
source.onmessage = function(event) {
    document.getElementById("result").innerHTML += event.data + "<br>";
}
source.onerror = function(error) {
    console.log(error);
    document.getElementById("result").innerHTML += "EventSource error:" + error + "<br>";
}
</script>
</head>
<body>
<div id="result"></div>
</body>
</html>
""")

def events(req, resp):
    print("Event source connected")
    yield from resp.awrite("HTTP/1.0 200 OK\r\n")
    yield from resp.awrite("Content-Type: text/event-stream\r\n")
    yield from resp.awrite("\r\n")
    i = 0
    try:
        while True:
            yield from resp.awrite("data: %d\n\n" % i)
            yield from uasyncio.sleep(1)
            i += 1
    except OSError:
        print("Event source connection closed")
        yield from resp.aclose()


ROUTES = [
    ("/", index),
    ("/events", events),
]


import logging
logging.basicConfig(level=logging.INFO)
#logging.basicConfig(level=logging.DEBUG)

app = picoweb.WebApp(__name__, ROUTES)
app.run(debug=True)
