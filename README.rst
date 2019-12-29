picoweb
=======

picoweb is a "micro" web micro-framework (thus, "pico-framework") for
radically unbloated web applications using radically unbloated Python
implementation, Pycopy, https://github.com/pfalcon/pycopy .

Features:

* Asynchronous from the start, using unbloated asyncio-like library
  for Pycopy (`uasyncio <https://github.com/pfalcon/pycopy-lib/tree/master/uasyncio>`_).
  This means that ``picoweb`` can process multiple concurrent requests
  at the same time (using I/O and/or CPU multiplexing).
* Small memory usage. Initial version required about 64K of heap for
  a trivial web app, and since then, it was optimized to allow run
  more or less realistic web app in ~36K of heap. More optimizations
  on all the levels (Pycopy and up) are planned (but may lead to
  API changes).
* Has API affinity with some well-known Python web micro-framework(s),
  thus it should be an easy start if you have experience with them, and
  existing applications can be potentially ported, instead of requiring
  complete rewrite.


Requirements and optional modules
---------------------------------

``picoweb`` depends on ``uasyncio`` for asynchronous networking
(https://github.com/pfalcon/pycopy-lib/tree/master/uasyncio).
``uasyncio`` itself requires `Pycopy <https://github.com/pfalcon/pycopy>`,
a minimalist, lightweight, and resource-efficient Python language
implementation.

It is also indended to be used with ``utemplate``
(https://github.com/pfalcon/utemplate) for templating, but this is
a "soft" dependency - picoweb offers convenience functions to use
``utemplate`` templates, but if you don't use them or will handle
templating in your app (e.g. with a different library), it won't be
imported.

For database access, there are following options (``picoweb`` does
not depend on any of them, up to your application to choose):

* `btree <https://pycopy.readthedocs.io/en/latest/library/btree.html>`_
  builtin Pycopy module. This is a recommended way to do a database
  storage for `picoweb`, as it allows portability across all Pycopy
  targets, starting with very memory- and storage-limited baremetal systems.
* ``btreedb`` wrapper on top of ``btree`` builtin module. This may add some
  overhead, but may allow to make an application portable between different
  database backends (`filedb` and `uorm` below).
  https://github.com/pfalcon/pycopy-btreedb
* ``filedb``, for a simple database using files in a filesystem
  https://github.com/pfalcon/filedb
* ``uorm``, for Sqlite3 database access (works only with Pycopy
  Unix port) https://github.com/pfalcon/uorm

Last but not least, ``picoweb`` uses a standard ``logging``-compatible
logger for diagnostic output (like a connection opened, errors and debug
information). However this output is optional, and otherwise you can use
a custom logging class instead of the standard ``logging``/``ulogging``
module. Due to this, and to not put additional dependencies burden on
the small webapps for small systems, ``logging`` module is not included
in ``picoweb``'s installation dependencies. Instead, a particular app
using ``picoweb`` should depend on ``pycopy-ulogging`` or
``pycopy-logging`` package. Note that to disable use of logging,
an application should start up using ``WebApp.run(debug=-1)``. The
default value for ``debug`` parameter is 0 however, in which case
picoweb will use ``ulogging`` module (on which your application needs
to depend, again).


Details
-------

picoweb API is roughly based on APIs of other well-known Python web
frameworks. The strongest affinity is Flask, http://flask.pocoo.org, as
arguably the most popular micro-framework. Some features are also based on
Bottle and Django. Note that this does not mean particular "compatibility"
with Flask, Bottle, or Django: most existing web frameworks are synchronous
(and threaded), while picoweb is async framework, so its architecture is
quite different. However, there is an aim to save porting efforts from
repetitive search & replace trials: for example, when methods do similar
things, they are likely named the same (but they may take slightly different
parameters, return different values, and behave slightly differently).

The biggest difference is async, non-threaded nature of picoweb. That means
that the same code may handle multiple requests at the same time, but unlike
threaded environment, there's no external context (like thread and thread
local storage) to associate with each request. Thus, there're no "global"
(or thread-local "global") request and response objects, like Flask,
Bottle, Django have. Instead, all picoweb functions explicitly pass the
current request and response objects around.

Also, picoweb, being unbloated framework, tries to avoid avoidable
abstractions. For example, HTTP at the lowest level has just read and write
endpoints of a socket. To dispatch request, picoweb needs to pre-parse
some request data from input stream, and it saves that partially (sic!)
parsed data as a "request" object, and that's what passed to application
handlers. However, there's no unavoidable need to have a "response"
abstraction - the most efficient/lightweight application may want to
just write raw HTTP status line, headers, and body to the socket. Thus,
raw write stream is passed to application handlers as the "response" object.
(But high-level convenience functions to construct an HTTP response are
provided).


API reference
-------------

The best API reference currently are examples (see below) and the ``picoweb``
source code itself. It's under 10K, so enjoy:
https://github.com/pfalcon/picoweb/blob/master/picoweb/__init__.py

Note that API is experimental and may undergo changes.


Examples
--------

* `example_webapp.py <https://github.com/pfalcon/picoweb/blob/master/example_webapp.py>`_ -
  A simple webapp showing you how to generate a complete HTTP response
  yourself, use ``picoweb`` convenience functions for HTTP headers generation,
  and use of templates. Mapping from URLs to webapp view functions ("web
  routes" or just "routes") is done Django-style, using a centralized route
  list.
* `example_webapp2.py <https://github.com/pfalcon/picoweb/blob/master/example_webapp2.py>`_ -
  Like above, but uses ``app.route()`` decorator for route specification,
  Flask-style.
* `examples/ <https://github.com/pfalcon/picoweb/tree/master/examples>`_ -
  Additional examples for various features of picoweb. See comments in each
  file for additional info. To run examples in this directory, you normally
  would need to have picoweb installed (i.e. available in your ``MICROPYPATH``,
  which defaults to ``~/.micropython/lib/``).
* `notes-pico <https://github.com/pfalcon/notes-pico>`_ - A more realistic
  example webapp, ported from the Flask original.


Running under CPython (regressed)
---------------------------------

Initial versions of picoweb could run under CPython, but later it was
further optimized for Pycopy, and ability to run under CPython
regressed. It's still on TODO to fix it, instructions below tell how
it used to work.

At least CPython 3.4.2 is required (for asyncio loop.create_task() support).
To run under CPython, uasyncio compatibility module for CPython is required
(pycopy-cpython-uasyncio). This and other dependencies can be installed
using requirements-cpython.txt::

    pip install -r requirements-cpython.txt

Reporting Issues
----------------

Here are a few guidelines to make feedback more productive:

1. Please be considerate of the overall best practices and common pitfalls in
   reporting issues, this document gives a good overview:
   `How to Report Bugs Effectively <https://www.chiark.greenend.org.uk/~sgtatham/bugs.html>`_.
2. The reference platform for ``picoweb`` is the Unix port of Pycopy. All issues
   reported must be validated against this version, to differentiate issues of
   ``picoweb``/``uasyncio`` from the issues of your underlying platform.
3. All reports must include version information of all components involved:
   Pycopy, picoweb, uasyncio, uasyncio.core, any additional modules. Generally,
   only the latest versions of the above are supported (this is what you get when
   you install/reinstall components using the ``upip`` package manager). The
   version information are thus first of all important for yourself, the issue
   reporter, it allows you to double-check if you're using an outdated or
   unsupported component.
4. Feature requests: ``picoweb`` is by definition a pico-framework, and bound
   to stay so. Feature requests are welcome, but please be considerate that
   they may be outside the scope of core project. There's an easy way out
   though: instead of putting more stuff *into* ``picoweb``, build new things
   *on top* of it: via plugins, subclassing, additional modules etc. That's
   how it was intended to be from the beginning!
5. We would like to establish a dedicated QA team to support users of this
   project better. If you would like to sponsor this effort, please let us
   know.
