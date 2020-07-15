Ampho Installation
==================

Ampho can be installed using traditional ``pip`` tool:

.. sourcecode:: python

    pip install -U flask_ampho

Being a regular `Flask extension`_, Ampho provides simple traditional way to setup:

.. sourcecode:: python

    from flask import Flask
    from flask_ampho import Ampho

    def create_app(config_filename):
        app = Flask(__name__)
        app.config.from_pyfile(config_filename)

        ampho = Ampho(app)

        return app

Or, using another popular pattern:

.. sourcecode:: python

    from flask import Flask
    from flask_ampho import Ampho

    ampho = Ampho()

    def create_app(config_filename):
        app = Flask(__name__)
        app.config.from_pyfile(config_filename)

        ampho.init_app(app)

        return app


* Next: `Configuration`_


.. _Flask extension: https://flask.palletsprojects.com/en/1.1.x/extensions/
.. _Configuration: configuration.rst
