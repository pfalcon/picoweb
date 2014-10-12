import re
import uasyncio as asyncio
import utemplate.source

from .utils import parse_qs



def sendfd(writer, f):
    while True:
        buf = f.read(512)
        if not buf:
            break
        yield from writer.awrite(buf)

def sendfile(writer, fname, content_type="text/plain"):
    yield from start_response(writer, content_type)
    with open(fname) as f:
        yield from sendfd(writer, f)

def jsonify(writer, dict):
    import ujson
    yield from start_response(writer, "application/json")
    yield from writer.awrite(ujson.dumps(dict))

def start_response(writer, content_type="text/html", status="200"):
    yield from writer.awrite("HTTP/1.0 %s NA\r\n" % status)
    yield from writer.awrite("Content-Type: %s\r\n" % content_type)
    yield from writer.awrite("\r\n")


class HTTPRequest:

    def __init__(self):
        pass

    def read_form_data(self):
        size = int(self.headers["Content-Length"])
        data = yield from self.reader.read(size)
        form = parse_qs(data)
        self.form = form


class WebApp:

    def __init__(self, routes=None, static="static"):
        if routes:
            self.url_map = routes
        else:
            self.url_map = []
        if static:
            self.url_map.append((re.compile("^/static(/.+)"),
                lambda req, resp: (yield from sendfile(resp, static + req.url_match.group(1)))))
        self.mounts = []
        self.inited = False
        self.template_loader = utemplate.source.Loader("templates")

    def _handle(self, reader, writer):
        request_line = yield from reader.readline()
        # TODO: bytes vs str
        request_line = request_line.decode()
        method, path, proto = request_line.split()
        headers = {}
        req = HTTPRequest()
        while True:
            l = yield from reader.readline()
            # TODO: bytes vs str
            l = l.decode()
            if l == "\r\n":
                break
            k, v = l.split(":", 1)
            headers[k] = v.strip()
        print("================")
        print(req, writer)
        print(req, (method, path, proto), headers)

        # Find which mounted subapp (if any) should handle this request
        app = self
        while True:
            found = False
            for subapp in app.mounts:
                root = subapp.url
                print(path, "vs", root)
                if path[:len(root)] == root:
                    app = subapp
                    found = True
                    path = path[len(root):]
                    if not path or path[0] != "/":
                        path = "/" + path
                    break
            if not found:
                break

        # We initialize apps on demand, when they really get requests
        if not app.inited:
            app.init()

        # Find handler to serve this request in app's url_map
        found = False
        for pattern, handler, *extra in app.url_map:
            if path == pattern:
                found = True
                break
            elif not isinstance(pattern, str):
                # Anything which is non-string assumed to be a ducktype
                # pattern matcher, whose .match() method is called. (Note:
                # Django uses .search() instead, but .match() is more
                # efficient and we're not exactly compatible with Django
                # URL matching anyway.)
                m = pattern.match(path)
                if m:
                    req.url_match = m
                    found = True
                    break
        if found:
            req.method = method
            req.path = path
            req.headers = headers
            req.reader = reader
            yield from handler(req, writer)
        else:
            yield from start_response(writer, status="404")
            yield from writer.awrite("404\r\n")
        print(req, "After response write")
        yield from writer.close()
        print(req, "Finished processing request")

    def mount(self, url, app):
        "Mount a sub-app at the url of current app."
        # Inspired by Bottle. It might seem that dispatching to
        # subapps would rather be handled by normal routes, but
        # arguably, that's less efficient. Taking into account
        # that paradigmatically there's difference between handing
        # an action and delegating responisibilities to another
        # app, Bottle's way was followed.
        app.url = url
        self.mounts.append(app)

    def route(self, url, **kwargs):
        def _route(f):
            self.url_map.append((url, f, kwargs))
            return f
        return _route

    def add_url_rule(self, url, func, **kwargs):
        # Note: this method skips Flask's "endpoint" argument,
        # because it's alleged bloat.
        self.url_map.append((url, func, kwargs))

    def render_template(self, writer, tmpl_name, args=()):
        tmpl = self.template_loader.load(tmpl_name)
        for s in tmpl(*args):
            yield from writer.awrite(s)

    def render_str(self, tmpl_name, args=()):
        #TODO: bloat
        tmpl = self.template_loader.load(tmpl_name)
        return ''.join(tmpl(*args))

    def init(self):
        """Initialize a web application. This is for overriding by subclasses.
        This is good place to connect to/initialize a database, for example."""
        self.inited = True

    def run(self, host="127.0.0.1", port=8081, debug=False, lazy_init=False):
        self.init()
        if not lazy_init:
            for app in self.mounts:
                app.init()
        loop = asyncio.get_event_loop()
        if debug:
            print("* Running on http://%s:%s/" % (host, port))
        loop.call_soon(asyncio.start_server(self._handle, host, port))
        loop.run_forever()
        loop.close()
