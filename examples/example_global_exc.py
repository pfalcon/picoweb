#
# This is a picoweb example showing a how to "globally" handle exceptions
# during request processing. Note that you can always handle
# exceptions in a particular request using normal try/except/finally.
# That's actually the recommended way. Of course, if you have a
# webapp with many request handlers, that becomes less practical
# and global exception handler may make sense. A common action of
# global handler would be to send a "500" page, but mind the cuprit
# shown below.
#
import picoweb


class ExcWebApp(picoweb.WebApp):

    async def handle_exc(self, req, resp, exc):
        try:
            # Do you already see a problem - what happens if your action
            # already started output before exception happened? Resolving
            # that issue is wholy up to your webapp, picoweb doesn't limit
            # you to any particular method, use whatever suits you better!
            await picoweb.start_response(resp, status="500")
            await resp.awrite("We've got 500, cap!")
        except Exception as e:
            # Per API contract, handle_exc() must not raise exceptions
            # (unless we want the whole webapp to terminate).
            print(repr(e))


app = ExcWebApp(__name__)


@app.route("/")
def index(req, resp):
    yield from picoweb.start_response(resp)
    yield from resp.awrite(
        "<a href='case1'>good exception case</a> "
        "<a href='case2'>less good exception case</a>"
    )


@app.route("/case1")
def case1(req, resp):
    1/0


@app.route("/case2")
def case2(req, resp):
    yield from picoweb.start_response(resp)
    yield from resp.awrite(
        "Here, I started to write something to response, and suddenly..."
    )
    1/0


import ulogging as logging
logging.basicConfig(level=logging.INFO)

app.run(debug=True)
