#
# This is an example of a (sub)application, which can be made a part of
# bigger site using "app mount" feature, see example_app_router.py.
#
import picoweb


app = picoweb.WebApp(__name__)

@app.route("/")
def index(req, resp):
    yield from picoweb.start_response(resp)
    yield from resp.awrite("This is webapp #2")


if __name__ == "__main__":
    app.run(debug=True)
