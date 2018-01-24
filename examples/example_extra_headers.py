#
# This is a picoweb example showing the usage of
# extra headers for encoded content and caching.
#
import picoweb
import ure as re

app = picoweb.WebApp(__name__)

@app.route("/")
def index(req, resp):
    yield from picoweb.start_response(resp)
    yield from resp.awrite("""\
<!DOCTYPE html>
<html>
<head>
<link href="style.css" rel="stylesheet">
</head>
<body>
<p>The style.css should be cached and might be encoded.</p>
<p class="green">Check out your webdev tool!</p>
</body>
</html>""")

# Send gzipped content if available
@app.route(re.compile('^\/(.+\.css)$'))
def styles(req, resp):
    file_path = req.url_match.group(1)
    header = b"Cache-Control: max-age=86400\r\n"

    if b"gzip" in req.headers[b"Accept-Encoding"]:
        file_path_gzip = file_path + ".gz"
        import os
        if file_path_gzip in os.listdir("examples/static"):
            file_path = file_path_gzip
            header += b"Content-Encoding: gzip\r\n"

    print("sending " + file_path)
    yield from app.sendfile(resp, "static/" + file_path, b"text/css", header)


import logging
logging.basicConfig(level=logging.INFO)

app.run(debug=True)
