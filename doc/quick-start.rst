Quick start
===========


Introduction
------------

First thing you should know is that *Ampho* is not a something conceptually new. *Ampho* even is not a web framework or
something like that. Actually it is just a wrapper over the `Flask framework`_. The goal of the *Ampho* is to reduce
developers' efforts on their way of creating modular and easy to maintain web applications. That's it.


Core concepts
-------------

Every *Ampho* application consists of one or more `bundles`_. Bundle is a regular Python package which contains all
necessary data such as `views`_, `templates`_, static files, CLI commands and so on. In short, when *Ampho* application
starts, it automatically executes code from bundles, so you don't have to create application class, instantiate and pass
it to other parts of an application. Just create necessary bundles containing all business logic of your application
and then *Ampho* will do all dirty work for you.


Virtual environment
-------------------

If you still don't use virtual environments you definitely should start to use it. If you don't understand what I am
talking about, please read `short explanation <https://flask.palletsprojects.com/en/master/installation/
#virtual-environments>`_ from the *Flask* creators:

.. note::

    What problem does a virtual environment solve? The more Python projects you have, the more likely it is that you
    need to work with different versions of Python libraries, or even Python itself. Newer versions of libraries for one
    project can break compatibility in another project.

Presume you have your application code located in ``~/src/hello-world`` directory. To create a virtual environment for
that application ``cd`` to that directory and use following command to initialize a virtual environment under the
``env`` directory:

.. sourcecode:: text

    $ python -m env

Then you can activate created environment by following command:

.. sourcecode:: text

    $ source ./env/bin/activate


So for now you have installed and activated Python virtual environment in ``env`` directory:

.. sourcecode:: text

    /hello-world
        /env

Let's move on!


Requirements
------------

After you have installed and activated a virtual environment you can install required dependencies. To continue our
journey you'll need only the ``ampho`` package which contains all necessary things and other dependencies:

.. sourcecode:: text

    (env) $ pip install -U ampho

That's all! Now we have all necessary to start building our first bundle.


Bundles
-------

Technically bundle is a regular Python package. The main purpose of bundles is to reduce developers efforts while
splitting application into small and maintainable parts. Bundles are like *Flask's* blueprints with slightly improved
functionality. Indeed Ampho bundles use *Flask's* blueprints under the hood, so it is nothing new for developers
familiar with *Flask's* concepts.

Every Ampho application usually consists of one or more bundles. Bundles may use other bundles and so on. Because
bundles are just regular Python packages, you can separately distribute them as extensions via GitHub, PyPi and other
ways you like, being free to develop your application's architecture in any way you want.

Let's create our first bundle called ``app``. To create a bundle you just need to create a regular python package:

.. sourcecode:: text

    /hello-world
        /app
            /__init__.py
        /env


Indeed bundle's name ``app`` is a little bit special. When an *Ampho* application starts it should know what bundles to
load. You can specify list of loadable bundles in different ways, but when you don't do this, *Ampho* will try to load
at least one bundle called ``app``. So for simple applications you even don't have to specify application's "main"
bundle, simply give the ``app`` name to it.


Start the application
---------------------

Now, when we have at least one bundle, we can start our first application. ``cd`` to the ``hello-world`` directory and
issue following command:

.. sourcecode:: text

    (env) $ ampho run

And voila, you have your first *Ampho* application running!

.. sourcecode:: text

    * Serving Flask app "ampho._flask_app:app"
    * Environment: production
      WARNING: This is a development server. Do not use it in a production deployment.
      Use a production WSGI server instead.
    * Debug mode: off
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

As you can see, you have a regular *Flask* application running. And yes, at this moment it cannot do anything useful.
So let's move on!


Views
-----

Almost any web application can be considered as computer code which takes requests from outer world, processes them and
gives back a response. To do this properly, application should know what code to execute to process particular
request. In the web we have concept of `URLs`_ which give the ability to distinct requests for different parts of the
application.

In order to assign URLs to particular parts of program code it is common to use **routes**. Route is a record about
what URL corresponds to what code. The code itself is being wrapped into callable object like a function or a class
method. In terms of *Ampho*, as like as in many other web frameworks, such object is called a **view**.

In general it doesn't matter where exactly view is located in the application code, but *Ampho* proposes a convenient
way to organize views' code and map it to URLs.

When *Ampho* loads a bundle, it checks for the ``views`` module presence in the bundle's package, and, if it's
present, *Ampho* automatically imports it within bundle's context, so you can easily use ``views`` module to define
views and map them as routes.

Let's look how this works. First, of course, we need to create ``views`` module in the ``app`` bundle:

.. sourcecode:: text

    /hello-world
        /app
            /__init__.py
            /views.py
        /env

Now open newly created ``views.py`` file and put there some code:

.. sourcecode:: python

    from flask import g


    @g.route('/')
    def home() -> str:
        """Home page
        """
        return 'Hello world!'

It is pretty simple to understand what happens here. Obviously, it is a function which will be called each time when
application will need to process an HTTP-request to the URL's root path and then the response from that function wil be
returned as the response.

"But what the heck that ``g`` object?" -- someone unfamiliar with *Flask* may wonder. It is thing known as a **context
manager** and it allows to dramatically decrease amount of code in some cases. It is a global object that keeps track
of the application-level data during a request. This means that it's not necessary to pass application object
exactly to each function which needs it and/or doing unnecessary imports. Instead an application and other necessary
data are initialized in the `application context`_ at application start and later can be accessed from any other module
via special object named ``g`` imported from ``flask`` package.

At application loading time each bundle has access to the ``g.route()`` decorator. It is regular *Flask*
`route() decorator`_ which is used for URL routes registrations.

Let's add another one view to see how it's simple:

.. sourcecode:: python

    @g.route('/<name>')
    def home(name: str) -> str:
        """Home page
        """
        return f'Hello {name}!'

So now you may restart the application and open its URL `<http://127.0.0.1:5000/>`_ in the browser to test the first
route and `<http://127.0.0.1:5000/John%20Doe>`_ to test the second one.


Templates
---------

Of course in real web application it is not convenient to render responses exactly in views` code. Usually it is
necessary to render more or less big amounts of HTML files and it is good practice to keep them separately. It is where
**templates** are coming.

Template is a separate file which can be loaded somewhere in the application and rendered using variable values where
it's needed. *Ampho* uses powerful `Jinja`_ template engine by default.

Let's modify our last view to make use the power of templating. First thing we should do is to create template file.
By default *Ampho* bundles expects templates to be stored in the separate directory named ``tpl`` within bundle's file
structure. Let's create that directory and place our first template named ``home.html`` here.

.. sourcecode:: text

    /hello-world
        /app
            /tpl
                /home.html
            /__init__.py
            /views.py
        /env

.. sourcecode:: html

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Hello {{ name }}!</title>
    </head>
    <body>
        <p>Hello {{ name }}!</p>
    </body>
    </html>

Now it's time to modify view's code to use rendered template instead of directly returned string:

.. sourcecode:: python

    from flask import g, render_template

    @g.route('/<name>')
    def home(name: str) -> str:
        """Home page
        """
        return render_template('home.html', name=name)


Dont forget to restart the application before looking how it works now.


.. _Flask framework: https://flask.palletsprojects.com
.. _URLs: https://en.wikipedia.org/wiki/URL
.. _application context: https://flask.palletsprojects.com/en/master/appcontext/
.. _route() decorator: https://flask.palletsprojects.com/en/master/api/#flask.Flask.route
.. _URL route registrations: https://flask.palletsprojects.com/en/master/api/#url-route-registrations
.. _Jinja: https://jinja.palletsprojects.com
