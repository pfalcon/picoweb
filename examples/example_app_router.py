#
# This is an example of running several sub-applications in one bigger
# application, by "mounting" them under specific URLs.
#
import picoweb
import app1, app2


site = picoweb.WebApp(__name__)
site.mount("/app1", app1.app)
site.mount("/app2", app2.app)


@site.route("/")
def index(req, resp):
    yield from picoweb.start_response(resp)
    yield from resp.awrite("<a href='app1'>app1<a> or <a href='app2'>app2</a>")


site.run(debug=True)
