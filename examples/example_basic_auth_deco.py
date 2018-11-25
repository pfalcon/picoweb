#
# This is a picoweb example showing handling of HTTP Basic authentication
# using a decorator. Note: using decorator is cute, bit isn't the most
# memory-efficient way. Prefer calling functions directly if you develop
# for memory-constrained device.
#
import ubinascii

import picoweb


app = picoweb.WebApp(__name__)


def require_auth(func):

    def auth(req, resp):
        auth = req.headers.get(b"Authorization")
        if not auth:
            yield from resp.awrite(
                'HTTP/1.0 401 NA\r\n'
                'WWW-Authenticate: Basic realm="Picoweb Realm"\r\n'
                '\r\n'
            )
            return

        auth = auth.split(None, 1)[1]
        auth = ubinascii.a2b_base64(auth).decode()
        req.username, req.passwd = auth.split(":", 1)
        yield from func(req, resp)

    return auth


@app.route("/")
@require_auth
def index(req, resp):
    yield from picoweb.start_response(resp)
    yield from resp.awrite("You logged in with username: %s, password: %s" % (req.username, req.passwd))


import logging
logging.basicConfig(level=logging.INFO)

app.run(debug=True)
