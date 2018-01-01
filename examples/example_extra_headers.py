#
# This is a picoweb example showing the usage of
# extra headers in responses.
#
import picoweb
import ure as re

app = picoweb.WebApp(__name__)

# Shows sending extra headers specified as a dictionary.
@app.route("/")
def index(req, resp):

    headers = {"X-MyHeader1": "foo", "X-MyHeader2": "bar"}

    # Passing headers as a positional param is more efficient,
    # but we pass by keyword here ;-)
    yield from picoweb.start_response(resp, headers=headers)
    yield from resp.awrite(b"""\
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


# Send gzipped content if supported by client.
# Shows specifying headers as a flat binary string -
# more efficient if such headers are static.
@app.route(re.compile('^\/(.+\.css)$'))
def styles(req, resp):
    file_path = req.url_match.group(1)
    headers = b"Cache-Control: max-age=86400\r\n"

    if b"gzip" in req.headers.get(b"Accept-Encoding", b""):
        file_path += ".gz"
        headers += b"Content-Encoding: gzip\r\n"

    print("sending " + file_path)
    yield from app.sendfile(resp, "static/" + file_path, "text/css", headers)


import logging
logging.basicConfig(level=logging.INFO)

app.run(debug=True)
