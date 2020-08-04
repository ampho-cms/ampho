.. _ampho-setup:

Setup
=====

Installation
------------

Ampho can be installed using traditional ``pip`` tool:

.. sourcecode:: python

    pip install -U flask_ampho


Application factory
-------------------

Being a regular `Flask extension`_, Ampho provides simple traditional way to setup it in the `application factory`_:

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


Root directory
--------------

Ampho uses application's `root path`_ as a guide for other locations such as configuration and log files.


Configuration directory
-----------------------

In addition to standard Flask configuration Ampho provides simple file based configuration mechanism which reads
configuration files from the ``config`` directory located next to the root path. Please refer to the
:doc:`configuration` section for additional information.


Log directory
-------------

By default Ampho registers its own rotating file logger to store logs under the ``log`` directory located next to the
root path. Please refer to the :doc:`logging` section for additional information.


Command line interface
----------------------

Ampho registers its own Flask CLI group named ``ampho`` which is used for calling Ampho related CLI commands. Someone
could find useful to create a shell alias to avoid typing ``flask`` each time while calling Ampho commands:

.. sourcecode:: shell

    alias ampho='flask ampho'


.. _Flask extension: https://flask.palletsprojects.com/en/1.1.x/extensions/
.. _application factory: https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/
.. _root path: https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.root_path
