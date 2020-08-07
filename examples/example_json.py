#
# This is a picoweb example showing how to handle form data.
#
import picoweb


app = picoweb.WebApp(__name__)


@app.route("/json_url")
def index(req, resp):
    if req.method == "POST":
        yield from req.read_json()
        yield from picoweb.jsonify(resp, {'json_received': req.json})

@app.route("/")
def index(req, resp):
    yield from picoweb.start_response(resp)
    yield from resp.awrite("<script>\n" 
        "function post_json() {\n"
            "fetch('json_url', {\n"
                "method: 'POST',\n"
                "body: JSON.stringify({foo: 'bar'})\n"
            "})\n"
                ".then(response => response.json())\n"
                ".then(data => console.log(data));\n"
            "}\n"
        "</script>\n")
    yield from resp.awrite("<button onclick='post_json()'>Post JSON</button>")

import ulogging as logging
logging.basicConfig(level=logging.INFO)

app.run(debug=True)
