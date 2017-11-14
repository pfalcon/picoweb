#
# This is a picoweb example showing various header parsing modes.
#
import ure as re
import picoweb


def index(req, resp):
    yield from resp.awrite("HTTP/1.0 200 OK\r\n")
    yield from resp.awrite("Content-Type: text/html\r\n")
    yield from resp.awrite("\r\n")
    yield from resp.awrite('<li><a href="mode_parse">header_mode="parse"</a>')
    yield from resp.awrite('<li><a href="mode_skip">header_mode="skip"</a>')
    yield from resp.awrite('<li><a href="mode_leave">header_mode="leave"</a>')


def headers_parse(req, resp):
    yield from picoweb.start_response(resp)
    yield from resp.awrite("<table border='1'>")
    for h, v in req.headers.items():
        yield from resp.awrite("<tr><td>%s</td><td>%s</td></tr>\r\n" % (h, v))
    yield from resp.awrite("</table>")

def headers_skip(req, resp):
    yield from picoweb.start_response(resp)
    assert not hasattr(req, "headers")
    yield from resp.awrite("No <tt>req.headers</tt>.")

def headers_leave(req, resp):
    yield from picoweb.start_response(resp)
    assert not hasattr(req, "headers")
    yield from resp.awrite("Reading headers directly from input request:")
    yield from resp.awrite("<pre>")
    while True:
        l = yield from req.reader.readline()
        if l == b"\r\n":
            break
        yield from resp.awrite(l)
    yield from resp.awrite("</pre>")


ROUTES = [
    ("/", index),
    ("/mode_parse", headers_parse, {"headers": "parse"}),
    ("/mode_skip", headers_skip, {"headers": "skip"}),
    ("/mode_leave", headers_leave, {"headers": "leave"}),
]


import logging
logging.basicConfig(level=logging.INFO)
#logging.basicConfig(level=logging.DEBUG)

app = picoweb.WebApp(__name__, ROUTES)
# You could set the default header parsing mode here like this:
# app.headers_mode = "skip"
app.run(debug=True)
