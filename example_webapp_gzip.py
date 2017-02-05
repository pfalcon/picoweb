import ure as re
import picoweb


def index(req, resp):
    yield from resp.awrite("HTTP/1.0 200 OK\r\n")
    yield from resp.awrite("Content-Type: text/html\r\n")
    yield from resp.awrite("\r\n")
    yield from resp.awrite("I can show you a table of <a href='squares'>squares</a>.")

def squares(req, resp):
    yield from picoweb.start_response(resp)
    yield from app.render_template(resp, "squares.tpl", (req,))


ROUTES = [
    ("/", index),
    ("/squares", squares),
    ("/file", lambda req, resp: (yield from picoweb.sendfile(resp, "picoweb.py"))),
    (re.compile("^/sq"), index),
]


import logging
logging.basicConfig(level=logging.INFO)
#logging.basicConfig(level=logging.DEBUG)

app = picoweb.WebApp(None, routes=ROUTES,gzip_ext='.gz')
app.run(debug=True)
