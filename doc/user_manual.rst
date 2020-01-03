Ampho User Manual
=================

*Ampho* is a Python library that provides simple and convenient way to develop web applications by splitting them into
small, easily maintainable parts called *"bundles"*.

**Bundle** is a regular Python package designed according to some rules and contains request handlers, templates, CLI
commands, static files, configuration files and application logic.

Unlike many popular web frameworks, when using *Ampho* you don't even have to create an application class and
instantiate it separately. All you have to do is to create one or more bundles and then start application provided by
*Ampho*, using traditional ``python -m`` command or your favourite application server like `uWSGI`_ or `Gunicorn`_.


Application's Root Directory
----------------------------

Despite almost any modern web application usually consists of many parts, it's a good practice to retain all that parts
under a single location on the filesystem, called **root directory**. Everywhere in this manual it's assumed you have
your application located in ``/home/user/src/hello-world``:

.. sourcecode:: text

    $ mkdir -p /home/user/src/hello-world && cd $_


Virtual Environment
-------------------

During all of this manual it is assumed, that you use Python's `virtual environment`_ to develop and run your
application. Following traditions, virtual environment usually is located in the root directory^

.. sourcecode:: text

    $ cd /home/user/src/hello-world
    $ python -m venv env
    $ source ./env/bin/activate
    (env) $

So after virtual environment installation you'll have following directory structure:

.. sourcecode:: text

    /hello-world
        /env


Installation
------------

To install latest version of the *Ampho* use one simple command:

.. sourcecode:: text

    (env) $ pip install -U ampho


What is the Bundle
------------------

Technically bundle is a regular Python package. The main purpose of bundles is reducing developers efforts by
splitting application into small and maintainable parts. Bundles are like `Flask's blueprints`_ with slightly improved
functionality.

Every *Ampho* application usually consists of one or more bundles, where one bundle may use another ones, other bundles
may use another ones and so on. Because bundles are just regular Python packages, you can separately develop, test and
distribute them via GitHub, PyPi and other ways you like, being free to develop your application's architecture in any
way you want.

Each bundle has a name which actually its Python package name. Obviously you can name your bundles anyhow you like,
since any valid Python package name is suitable.


The "app" bundle
----------------

Bundle's name ``app`` is a little bit special. The thing is, when the *Ampho* application starts, it should know what
should be loaded. You can specify list of that bundles using environment variable or configuration parameter (more about
that you can find below in this manual), but if you don't do this, *Ampho* will try to load at least one bundle named
``app``. So for simple setups you even don't have to specify application's "main" bundle, simply give the ``app`` name
to it.


Creating a bundle
-----------------

To create a bundle you just need to create a regular python package which can be properly imported afterwards. Let's
assume you use directory structure mentioned above, so after creating the ``app`` package in the root directory, you'll
have following files layout:

.. sourcecode:: text

    /hello-world
        /app
            /__init__.py
        /env

Notice, that at this point the ``app`` bundle doesn't have anything inside, it's just an empty Python package. But this
is already enough to start the application.


Start the application
---------------------

Now, when you have at least one bundle, you can start *Ampho* application:

.. sourcecode:: text

    (env) $ ampho run

And voila, you have your application running!

.. sourcecode:: text

    * Serving Flask app "ampho._cli:app"
    * Environment: production
      WARNING: This is a development server. Do not use it in a production deployment.
      Use a production WSGI server instead.
    * Debug mode: off
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)


Debug and auto reloading
------------------------

While doing development it's pretty annoying to manually restart the application whenever code is changed. To force the
application reload by itself in such cases, set ``AMPHO_DEBUG`` environment variable to `1`. For convenience this option
also enables debugging capabilities, so **you shouldn't enable this feature on production environment**.


Routing
-------

Almost any web application can be considered as a code which takes requests from outer world, processes them and
gives a response back. To do this properly, application should know what code to execute to process particular
request. In the web we have concept of `URLs`_ which give the ability to distinct requests for different parts of the
application.

In order to assign URLs to particular parts of program code it is common to use **routes**. Route is a record about
what URL should trigger what code. The code itself is being wrapped into callable object like a function or a class
method. In terms of Ampho, as like as in many other web frameworks, such object is called a **view**.

In general it doesn't matter where exactly view is located in the application code, but *Ampho* proposes a convenient
way to organize views' code and map it to URLs.

When Ampho loads a bundle, it checks for the ``views`` module presence in the bundle's package, and, if it's
present, Ampho automatically imports it within bundle's context, so you can easily use ``views`` module to define
views and map them as routes.

Let's look how this works. At first, of course, we need to create ``views`` module inside a bundle:

.. sourcecode:: text

    /hello-world
        /app
            /__init__.py
            /views.py
        /env

Now open newly created ``views.py`` file and place some code there:

.. sourcecode:: python

    from ampho import route

    @route('/')
    def home() -> str:
        """Home page
        """
        return 'Hello, world!'

As you can see, there is the ``ampho.route`` decorator used to make the ``home()`` function responsible for
processing requests to the ``/`` URL path. As you can suggest, the first argument of the ``route()`` decorator is the
path of the URL connected to decorated function.

Since *Ampho* uses Flask under the hood, you are free to use any features of the `Flask routing`_, including variable
rules, different HTTP methods and so on.

For example, let's add another one view to demonstrate usage of Flask's variable rules feature:

.. sourcecode:: python

    @route('/<name>')
    def hello(name: str) -> str:
        """Greetings page
        """
        return f'Hello, {name}!'


URL Building
------------

To build an URL to a specific view function, use the ``url_for()`` function. It accepts the name of the view
function prefixed with bundle name as its first argument and any number of keyword arguments, each corresponding to a
variable part of the URL rule. Unknown variable parts are appended to the URL as query parameters:

.. sourcecode:: python

    from ampho import url_for

    print(url_for('app.hello', name='Alice'))  # Will print '/hello/Alice'

The same function can be used in `templates`_ as well:

.. sourcecode:: html

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Ampho Application</title>
    </head>
    <body>
        <p>
            <a href="{{ url_for('app.hello', name='Alice') }}">Say hello to Alice</a>
        </p>
    </body>
    </html>

To view all existing rule names, use the following CLI command:

.. sourcecode:: text

    (env) $ ampho routes

.. sourcecode:: text

    Endpoint   Methods  Rule
    ---------  -------  -----------------------
    app.hello  GET      /<name>
    app.home   GET      /


Redirects and Errors
--------------------

To do.


Templates
---------

Of course in real web application it is not convenient to render responses exactly in views` code. Usually it is
necessary to render more or less big amounts of HTML code, and it is good practice to keep it separately. It is where
**templates** are coming.

Template is a separate file which can be loaded somewhere in the application and rendered using variable values where
it's needed. *Ampho* uses powerful `Jinja`_ template engine by default.

Let's modify our last view to make use the power of templating. First thing we should do is to create template file.
By default any *Ampho* bundle expects templates to be stored in the separate directory named ``tpl`` within bundle's
file structure. Let's create that directory and place our first template named ``home.html`` here.

.. sourcecode:: text

    /hello-world
        /app
            /__init__.py
            /tpl
                /home.html
            /views.py
        /env

.. sourcecode:: html

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Ampho Application</title>
    </head>
    <body>
        <p>Hello, {{ name }}!</p>
    </body>
    </html>

After that modify view's code to use rendered template instead of directly returned string:

.. sourcecode:: python

    from ampho import route, render

    @route('/<name>')
    def hello(name: str) -> str:
        """Greetings page
        """
        return render('home.html', name=name)


Accessing Request Data
----------------------

To do.


Cookies
-------
To do.


Context Locals
--------------

To do.


Logging
-------

To do.


Deploying to a Web Server
-------------------------

To do.


.. _virtual environment: https://docs.python.org/3/tutorial/venv.html
.. _Gunicorn: https://gunicorn.org/
.. _uWSGI: https://uwsgi-docs.readthedocs.io/
.. _Flask: https://flask.palletsprojects.com
.. _Flask's blueprints: https://flask.palletsprojects.com/en/master/blueprints/
.. _Flask routing: https://flask.palletsprojects.com/en/1.1.x/quickstart/#routing
.. _URLs: https://en.wikipedia.org/wiki/URL
.. _Jinja: https://jinja.palletsprojects.com
