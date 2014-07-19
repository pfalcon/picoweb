# This is (almost) the same as test_webapp.py, but uses app.route().
import picoweb


app = picoweb.WebApp()

@app.route("/")
def index(writer, req):
    yield from picoweb.start_response(writer)
    yield from writer.awrite("I can show you a table of <a href='squares'>squares</a>.")

@app.route("/squares")
def squares(writer, req):
    yield from picoweb.start_response(writer)
    yield from picoweb.render(writer, "squares", (req,))


import logging
logging.basicConfig(level=logging.INFO)

app.run(debug=True)
