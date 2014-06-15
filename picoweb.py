import re
import asyncio_micro as asyncio
import utemplate.source


template_loader = utemplate.source.Loader(".")

def render(writer, tmpl_name, args=()):
    tmpl = template_loader.load(tmpl_name)
    for s in tmpl(*args):
        yield from writer.awrite(s)

def start_html(writer):
    yield from writer.awrite("HTTP/1.0 200 OK\r\n")
    yield from writer.awrite("Content-Type: text/html\r\n")
    yield from writer.awrite("\r\n")


class HTTPRequest:

    def __init__(self, method, path, headers):
        self.method = method
        self.path = path
        self.headers = headers


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
        for pattern, handler in self.routes:
            if path == pattern:
                found = True
                break
            elif not isinstance(pattern, str) and pattern.search(path):
                found = True
                break
        if found:
            yield from handler(writer, req)
        print("After response write")
        yield from writer.close()
        print("Finished processing request")

    def serve(self):
        loop = asyncio.get_event_loop()
        loop.call_soon(asyncio.start_server(self._handle, "127.0.0.1", 8081))
        loop.run_forever()
        loop.close()
