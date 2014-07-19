import re
import asyncio_micro as asyncio
import utemplate.source

from .utils import parse_qs


template_loader = utemplate.source.Loader(".")

def render(writer, tmpl_name, args=()):
    tmpl = template_loader.load(tmpl_name)
    for s in tmpl(*args):
        yield from writer.awrite(s)

def render_str(tmpl_name, args=()):
    #TODO: bloat
    tmpl = template_loader.load(tmpl_name)
    return ''.join(tmpl(*args))

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
    import json
    yield from start_response(writer, "application/json")
    yield from writer.awrite(json.dumps(dict))

def start_response(writer, content_type="text/html"):
    yield from writer.awrite("HTTP/1.0 200 OK\r\n")
    yield from writer.awrite("Content-Type: %s\r\n" % content_type)
    yield from writer.awrite("\r\n")


class HTTPRequest:

    def __init__(self, method, path, headers):
        self.method = method
        self.path = path
        self.headers = headers

    def read_form_data(self):
        size = int(self.headers["Content-Length"])
        data = yield from self.reader.read(size)
        form = parse_qs(data)
        self.form = form


class WebApp:

    def __init__(self, routes):
        self.routes = routes

    def _handle(self, reader, writer):
        print(reader, writer)
        print("================")
        request_line = yield from reader.readline()
        method, path, proto = request_line.split()
        headers = {}
        while True:
            l = yield from reader.readline()
            if l == "\r\n":
                break
            k, v = l.split(":", 1)
            headers[k] = v.strip()
        print((method, path, proto), headers)
        req = HTTPRequest(method, path, headers)
        found = False
        for pattern, handler, *extra in self.routes:
            if path == pattern:
                found = True
                break
            elif not isinstance(pattern, str):
                m = pattern.search(path)
                if m:
                    req.url_match = m
                    found = True
                    break
        if found:
            req.reader = reader
            yield from handler(writer, req)
        print("After response write")
        yield from writer.close()
        print("Finished processing request")

    def route(self, url, **kwargs):
        def _route(f):
            self.routes.append((url, f, kwargs))
            return f
        return _route

    def run(self, host="127.0.0.1", port=8081, debug=False):
        loop = asyncio.get_event_loop()
        if debug:
            print("* Running on http://%s:%s/" % (host, port))
        loop.call_soon(asyncio.start_server(self._handle, host, port))
        loop.run_forever()
        loop.close()
