#
# This is a picoweb example showing how to handle form data.
#
import picoweb


app = picoweb.WebApp(__name__)


@app.route("/form_url")
def index(req, resp):
    if req.method == "POST":
        yield from req.read_form_data()
    else:  # GET, apparently
        # Note: parse_qs() is not a coroutine, but a normal function.
        # But you can call it using yield from too.
        req.parse_qs()

    # Whether form data comes from GET or POST request, once parsed,
    # it's available as req.form dictionary

    yield from picoweb.start_response(resp)
    yield from resp.awrite("Hello %s!" % req.form["name"])


@app.route("/")
def index(req, resp):
    yield from picoweb.start_response(resp)
    yield from resp.awrite("POST form:<br>")
    yield from resp.awrite("<form action='form_url' method='POST'>"
        "What is your name? <input name='name' /> "
        "<input type='submit'></form>")

    yield from resp.awrite("GET form:<br>")
    # GET is the default
    yield from resp.awrite("<form action='form_url'>"
        "What is your name? <input name='name' /> "
        "<input type='submit'></form>")


import ulogging as logging
logging.basicConfig(level=logging.INFO)

app.run(debug=True)
