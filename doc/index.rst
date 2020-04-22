Ampho User Manual
=================

**Ampho** is a Python library that provides simple and convenient way to develop applications by splitting them into
small, easily maintainable parts called *"bundles"*.

**Bundle** is a regular Python package designed according to some rules and contains request handlers, templates, CLI
commands, static files, configuration files, application logic, etc.

Using Ampho you don't have to create an application class and instantiate it separately. All you have to do is to
create one or more bundles and then start ready to use application provided by Ampho, using traditional ``python -m``
command or your favorite application server like `uWSGI`_ or `Gunicorn`_.


Installation
------------

To install latest version of the Ampho, use one simple command:

.. sourcecode:: text

    (env) $ pip install -U ampho


Ampho and Flask
---------------

It is important to notice again, that Ampho is **not** a standalone framework. It should be considered as a helper
library, that may help make development process of Flask applications a little bit easier. It means that you don't have
to change your development workflow significantly, as well as you don't have to learn new concepts besides couple ones,
which are described in this document. For all other information please check Flask's official documentation.


What is a bundle
----------------

Technically bundle is a regular Python package. The main purpose of bundles is reducing developers efforts by
splitting application into small and maintainable parts. Bundle is like `Flask blueprint`_ with slightly improved
functionality.

Every Ampho application usually consists of one or more bundles, where one bundle may use another ones, other bundles
may use another ones and so on. Because bundles are just regular Python packages, you can separately develop, test and
distribute them via GitHub, PyPi and other ways you like, being free to develop your application's architecture in any
way you want.

Each bundle has a name which is actually a package name. Obviously you can name your bundles anyhow you like, since any
valid Python package name is suitable.


Bootstrap bundle
----------------

When Ampho starts it needs to know what to do after initialization. Because any Ampho application are splitted into
bundles, it's obviously that a some "special" bootstrap bundle should exist, allowing Ampho to boot it at first. Usually
it's not necessary to specify that bundle name manually, because Ampho searches for a bundle named ``app`` and uses it
as an entry point. If you for some reason want to name your bootstrap bundle differently, you should notice Ampho about
that using environment variable ``AMPHO_ENTRY``.


Root Directory
--------------

Despite almost any modern web application usually consists of many parts, it's a good practice to retain all that parts
under a single location on the filesystem, called **root directory**. Ampho automatically selects parent directory of
the bootstrap bundle as a root one.


Instance directory
------------------

As you may know, Flask has a concept of `instance directory <https://flask.palletsprojects.com/en/master/config/
#instance-folders>`_. Unlike Flask, Ampho automatically creates the application object and configures location of the
instance directory, which is by default located at ``${root_dir}/instance``. You don't have to create this directory
manually, it'll be created by Ampho automatically at start time.


Creating a bundle
-----------------

To create a bundle you just need to create a regular python package which can be properly imported afterwards. Let's
assume you use directory structure mentioned above, so after creating the ``app`` package in the root directory, you'll
have following files layout:

.. sourcecode:: text

    /hello-world
        /app
            __init__.py
        /instance

Notice, that at this point the ``app`` bundle doesn't have anything inside, it's just an empty Python package. But this
is already enough to start the application.


Start the application
---------------------

Now, when you have at least one bundle, you can start Ampho application:

.. sourcecode:: text

    (env) $ ampho run

And voila, you have your application running!

.. sourcecode:: text

    * Serving Flask app "ampho.main:APPLICATION"
    * Environment: production
      WARNING: This is a development server. Do not use it in a production deployment.
      Use a production WSGI server instead.
    * Debug mode: off
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

As you can notice, starting an Ampho application is almost the same as starting a Flask one, except instead of
``flask`` CLI command, ``ampho`` should be used. This is only the difference between Ampho and Flask at this point.


Bundle initialization process
-----------------------------

When Ampho loads a bundle, it does this operation in two steps. At first, bundle is registered, and then it is loaded.
If you need to perform actions during bundle registration, you should define ``on_register()`` hook function in the
bundle module's ``__init__.py`` code and it'll be called automatically by Ampho. Similarly, you may define ``on_load()``
function, if you need actions to be performed at bundle loading time.

.. sourcecode:: python

    def on_register():
        print('Bundle is registered')

    def on_load():
        print('Bundle is loaded')


Bundle requirements
-------------------

A bundle can depend on other bundles. In that case it is important, that required bundles be properly loaded and
initialized before dependant bundle. To define requirements for your bundle, use ``REQUIRES`` list or tuple of
strings property in bundle's ``__init__.py``, i. e.:

.. sourcecode:: python

    REQUIRES = ('ampho_locale', 'ampho_db')


Application configuration
-------------------------

Ampho applications are configured the same way as `Flask ones <https://flask.palletsprojects.com/en/master/config/>`_.
In addition to Flask' configuration mechanism, Ampho provides another convenient way to handle and distribute
application's configuration using JSON files with pre-defined names, located in the `instance directory`_.

When Ampho starts, it searches for configuration files in the following order:

#. ``default.json``
#. ``{environment}.json``
#. ``{username}@{hostname}.json``


where parameters from each next file are merged with a previous one. The ``default.json`` file is being loaded always.
The ``{environment}.json`` is loaded only if ``{environment}`` corresponds to current ``${FLASK_ENV}`` environment
variable. And the ``{username}@{hostname}.json`` will be loaded only if ``{username}`` and ``{hostname}`` are correspond
to the ``${USER}`` and ``${HOSTNAME}`` environment variables.

For example, some application can have following configuration files set:

.. sourcecode:: text

    /hello-world
        /instance
            default.json
            development.json
            production.json
            home_user@home_host.json
            prod_user@prod_host.json

Using this approach, you can store all the application configuration in one place, while Ampho will choose appropriate
configuration set automatically depending on environment where application runs.


Routing
-------

In general it doesn't matter where exactly views code is located, but Ampho proposes a convenient way to organize
views and map them to URLs.

When Ampho loads a bundle, it checks for the ``views`` module presence in the bundle's package, and, if it's
present, Ampho automatically imports it within bundle's context, so you can easily use ``views`` module to define
views and map them as routes.

Let's look how this works. At first, of course, we need to create ``views`` module inside a bundle:

.. sourcecode:: text

    /hello-world
        /app
            __init__.py
            views.py

And place some code there:

.. sourcecode:: python

    from ampho import route

    @route('/')
    def home() -> str:
        """Home page
        """
        return 'Hello, world!'

As you can see, there is the ``ampho.route`` decorator used to make the ``home()`` function responsible for
processing requests to the ``/`` URL path.

Since Ampho uses Flask under the hood, you are free to use any features of the `Flask routing`_, including variable
rules, different HTTP methods and so on.

.. note::

    Don't forget to use ``route()`` decorator from the ``ampho`` package instead of the ``flask``'s one, because it
    does some kind of magic while dealing with bundles.

For all other aspects of working with routing, please refer to the `Flask routing guide`_.


Template rendering
------------------

Template rendering in Ampho works almost the same way as in Flask, except two moments:

#. Template files should be located inside the ``tpl`` directory of the bundle.
#. To render templates the ``ampho.render()`` function should be user instead if ``flask.render_template()``. The first
   one has exactly same signature as the `flask.render_template()`_, but injects ``_bundle`` variable into each
   template, which is current bundle object.


CLI commands
------------

In general it doesn't matter where exactly CLI commands code is located, but Ampho proposes a convenient to organize
commands code by placing them into separate module named ``commands``.

.. sourcecode:: text

    /hello-world
        /app
            __init__.py
            commands.py  <-- Here is the module with commands
            views.py

Once you have module named ``commands`` in a bundle, Ampho will import it automatically at bundle loading time, so
everything you need to do is to place commands' functions into it, wrapping them with ``ampho.cli.command()`` decorator.

.. sourcecode:: python

    from ampho import cli, echo_info

    @cli.command('hello')
    def hello():
        echo_info('Hello, world')


That's all. Now, you can run your command from CLI:

.. sourcecode:: text

    (env) $ ampho app hello
    Hello, world

Notice, that ``hello`` command was automatically placed to the ``app`` group, which name is the name of the bundle where
command was defined. If you need to change command group's name, it could be done via ``CLI_GROUP`` module-level
property. Additionally, using the ``CLI_HELP`` property, you can set group's description shown when you run ``ampho``
command without arguments.

.. sourcecode:: python

    from ampho import cli, echo_info

    CLI_GROUP = 'my_app'
    CLI_HELP = 'Set of extremely useful commands'

    @cli.command('hello')
    def hello():
        echo_info('Hello, world')

For all other aspects of working with CLI commands, please refer to the `Flask CLI guide`_.


Application Context
-------------------

When you use pure Flask, you create application object by yourself. But when you use Ampho, this object created by Ampho
for you. To access this object use ``ampho.current_app`` attribute, i. e.:

.. sourcecode:: python

    from ampho import current_app
    from flask.logging import default_handler

    current_app.logger.removeHandler(default_handler)


Logging
-------

If ``FLASK_ENV`` configuration parameter is ``development`` or ``FLASK_DEBUG`` is ``1``, logging level automatically
is set to ``DEBUG``.

Besides of `Flask logging`_ capabilities, Ampho additionally adds `TimedRotatingFileHandler`_ by default. This logger
is configured to write one file per day into the ``${root_dir}/log`` by default and retains last 30 files.

If you don't need this logger to be enabled, set ``LOG_FILES_ENABLED`` configuration parameter to ``0``.

If it's necessary to change `log messages format`_ of this logger, you can do this via ``LOG_FILES_MSG_FORMAT``
configuration parameter.

Number of retained files is controlled via ``LOG_FILES_BACKUP_COUNT`` configuration parameter.


Deploying
---------

Generally deploying Ampho application to a web server is the same as `deploying a Flask application`_.

One thing should be noted, that when `deploying to a uWSGI server`_, the ``ampho.main`` module name should be
used as the application container, i. e.:

.. sourcecode:: text

    uwsgi --http :8080 --plugin=python --venv=./env --module=ampho.main


.. _virtual environment: https://docs.python.org/3/tutorial/venv.html
.. _Gunicorn: https://gunicorn.org/
.. _uWSGI: https://uwsgi-docs.readthedocs.io/
.. _Flask: https://flask.palletsprojects.com
.. _Flask blueprint: https://flask.palletsprojects.com/en/master/blueprints/
.. _Flask routing: https://flask.palletsprojects.com/en/master/quickstart/#routing
.. _URLs: https://en.wikipedia.org/wiki/URL
.. _Jinja: https://jinja.palletsprojects.com
.. _flask.render_template() function: https://flask.palletsprojects.com/en/master/api/#flask.render_template
.. _Flask routing guide: https://flask.palletsprojects.com/en/master/quickstart/#routing
.. _Flask CLI guide: https://flask.palletsprojects.com/en/master/cli/
.. _Flask logging: https://flask.palletsprojects.com/en/master/logging/
.. _TimedRotatingFileHandler: https://docs.python.org/3/library/logging.handlers.html#timedrotatingfilehandler
.. _flask.render_template(): https://flask.palletsprojects.com/en/master/api/#flask.render_template
.. _log messages format: https://docs.python.org/3/library/logging.html#logrecord-attributes
.. _deploying a Flask application: https://flask.palletsprojects.com/en/master/deploying/
.. _deploying to a uWSGI server: https://flask.palletsprojects.com/en/master/deploying/uwsgi/
