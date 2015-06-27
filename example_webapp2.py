# This is (almost) the same as test_webapp.py, but uses app.route().
import picoweb


app = picoweb.WebApp(__name__)

@app.route("/")
def index(req, resp):
    yield from picoweb.start_response(resp)
    yield from resp.awrite("I can show you a table of <a href='squares'>squares</a>.")

@app.route("/squares")
def squares(req, resp):
    yield from picoweb.start_response(resp)
    yield from app.render_template(resp, "squares.tpl", (req,))


import logging
logging.basicConfig(level=logging.INFO)

app.run(debug=True)
