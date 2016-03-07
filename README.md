Intro
=====
picoweb is "micro" web micro-framework (thus, "pico-framework") for radically
unbloated web applications using radically unbloated Python implementation,
MicroPython, https://github.com/micropython/micropython .

Features:

* Asynchronous from the start, using unbloated asyncio-like library
for MicroPython (uasyncio).
* Modest memory usage (I would say radically small memory usage, but
so far, trivial web app requires 64K (yes, kilobytes) of heap, which
is much more than I expected).
* Has API affinity with well-known Python web micro-framework(s),
thus it should be easy start if you have experience with that, and
existing applications can be potentially ported, instead of requiring
complete rewrite.


Details
=======
picoweb depends on:

* uasyncio for asynchronous networking
https://github.com/micropython/micropython-lib/tree/asyncio
* utemplate, for templating
https://github.com/pfalcon/utemplate
* uorm, for database access (optional, no direct dependency in framework)
https://github.com/pfalcon/uorm

picoweb API is roughly based on APIs of other well-known Python web
frameworks. The strongest affinity is Flask, http://flask.pocoo.org, as
arguably the most popular micro-framework. Some features are also based on
Bottle and Django. Note that this does not mean particular "compatibility"
with Flask, Bottle, or Django: most existing web frameworks are synchronous
(and threaded), while picoweb is async framework, so its architecture is
quite different. However, there is an aim to save porting efforts from
repeatitive search & replace trials, for example, when methods do similar
things, they are likely named the same (but they may take slightly different
parameters, return different values, and behave slightly differently).

The biggest difference is async, non-threaded nature of picoweb. That means
that the same code may handle multiple requests at the same time, but unlike
threaded environment, there's no external context (like thread and thread
local storage) to associate with each request. Thus, there're no "global"
(or thread-local "global") request and response objects, like Flask,
Bottle, Django have. Instead, all picoweb functions explicitly pass current
request and response objects around.

Also, picoweb, being unbloated framework, tries to avoid avoidable
abstractions. For example, HTTP at the lowest level has just read and write
endpoints of a socket. To dispatch request, picoweb needs to pre-parse
some request data from input stream, and it saves that partially (sic!)
parsed data as a "request" object, and that's what passed to application
handlers. However, there's no unavoidable need to have "response"
abstraction - the most efficient/lightweight application may want to
just write raw HTTP status line, headers, and body to the socket. Thus,
raw write stream is passed to application handlers as "response" object.
(But high-level convenience functions to construct an HTTP response are
provided).

Last point is questionable conveniences. For example, both Flask and Bottle
provide special objects to handle form/get parameters, with features
like "if request variable has only one value, the value is returned directly;
otherwise, list of values is returned". However, Python standard library
provides function parse_qs(), which always returns array of values (based
on the fact that any request variable may have more than one value). Given
2 choices, picoweb follows the interface of the standard library, instead of
providing extra wrapper class on top of it.


Running under CPython
=====================

At least CPython 3.4.2 is required (for asyncio loop.create_task() support).
To run under CPython, uasyncio compatibility module for CPython is required
(micropython-cpython-uasyncio). This and other dependencies can be installed
using requirements-cpython.txt:

    pip install -r requirements-cpython.txt
