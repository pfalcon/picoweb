#
# This is a picoweb example showing rendering of template
# with Unicode (UTF-8) characters.
#
import picoweb


app = picoweb.WebApp(__name__)

@app.route("/")
def index(req, resp):
    yield from picoweb.start_response(resp)
    data = {"chars": "абвгд", "var1": "α", "var2": "β", "var3": "γ"}
    yield from app.render_template(resp, "unicode.tpl", (data,))

import ulogging as logging
logging.basicConfig(level=logging.INFO)

app.run(debug=True)
