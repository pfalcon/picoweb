Intro
=====
picoweb is a "micro" web micro-framework (thus, "pico-framework") for
radically unbloated web applications using radically unbloated Python
implementation, MicroPython, https://github.com/micropython/micropython.

Features:

* Asynchronous from the start, using unbloated asyncio-like library
  for MicroPython ([uasyncio](https://github.com/micropython/micropython-lib/tree/master/uasyncio)).
* Modest memory usage. I would say radically small memory usage, but
  with the initial version, a trivial web app used to require 64K (yes,
  kilobytes) of heap, which is much more than I expected. Optimizing
  that on all the levels (MicroPython and up) is underway.
* Has API affinity with well-known Python web micro-framework(s),
  thus it should be easy start if you have experience with that, and
  existing applications can be potentially ported, instead of requiring
  complete rewrite.


Requirements and optional modules
=================================
`picoweb` depends on `uasyncio` for asynchronous networking
(https://github.com/micropython/micropython-lib/tree/asyncio).

It is also indended to be used with `utemplate`
(https://github.com/pfalcon/utemplate) for templating, but this is
a "soft" dependency - picoweb offers convenience functions to use
`utemplate` templates, but if you don't them or will handle templating
in your app (e.g. with a different library), it won't be imported.

For database access, there are following options (`picoweb` does
not depend on any of them, up to your application to choose):

* `uorm`, for Sqlite3 database access
  https://github.com/pfalcon/uorm
* `filedb`, for a simple database using files in a filesystem
  https://github.com/pfalcon/filedb
* `btree` builtin MicroPython module. It is expected that a simple
  ORM will be developed for this module and it will be a recommended
  way to do a database for `picoweb`, as this module allows portability
  across all MicroPython targets, starting with very memory- and
  storage-limited baremetal systems.


Details
=======
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


API reference
=============
The best API reference currently are examples (see below) and the `picoweb`
source code itself. It's under 10K, so enjoy:
https://github.com/pfalcon/picoweb/blob/master/picoweb/__init__.py

Note that API is experimental and may undergo changes.


Examples
========
* `example_webapp.py` - A simple webapp showing you how to generate a
  complete HTTP response yourself, use `picoweb` convenience functions
  for HTTP headers generation, and use of templates. Mapping from
  URLs to webapp view functions ("web routes" or just "routes") is done
  Django-style, using a centralized route list.
* `example_webapp2.py` - like above, but uses `app.route()` decorator
  for route specification, Flask-style.


Running under CPython
=====================

Initial versions on picoweb could run under CPython, but later it was
further optimized for MicroPython, and ability to run under CPython
regressed. It's still on TODO to fix it, instructions below tell how
it used to work.

At least CPython 3.4.2 is required (for asyncio loop.create_task() support).
To run under CPython, uasyncio compatibility module for CPython is required
(micropython-cpython-uasyncio). This and other dependencies can be installed
using requirements-cpython.txt:

    pip install -r requirements-cpython.txt
