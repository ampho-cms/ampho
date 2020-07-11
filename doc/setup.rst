Application Setup
=================

Being a regular Flask extension, Ampho could be set up as any other extension. Assume you already have some Flask
application defined in your application factory:

.. sourcecode:: python

    from flask import Flask

    def create_app(config_filename):
        app = Flask(__name__)
        app.config.from_pyfile(config_filename)
        return app


Then, to setup Ampho, you should add couple lines in your factory code:

.. sourcecode:: python

    from flask import Flask

    def create_app(config_filename):
        app = Flask(__name__)
        app.config.from_pyfile(config_filename)

        ampho = Ampho(app)

        return app
