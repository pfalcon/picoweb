import re
import picoweb


def index(writer, req):
    yield from writer.awrite("HTTP/1.0 200 OK\r\n")
    yield from writer.awrite("Content-Type: text/html\r\n")
    yield from writer.awrite("\r\n")
    yield from writer.awrite("I can show you a table of <a href='squares'>squares</a>.")

def squares(writer, req):
    yield from picoweb.start_response(writer)
    yield from picoweb.render(writer, "squares", (req,))


ROUTES = [
    ("/", index),
    ("/squares", squares),
    ("/file", lambda wr, req: (yield from picoweb.sendfile(wr, "picoweb.py"))),
    (re.compile("^/"), index),
]


import logging
logging.basicConfig(level=logging.INFO)
#logging.basicConfig(level=logging.DEBUG)

app = picoweb.WebApp(ROUTES)
mem_info()
app.run(debug=True)
