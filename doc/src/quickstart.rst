Quick start
===========

Installation
------------

.. sourcecode:: python

    pip install -U flask_ampho


File structure
--------------

Assume you have the source code root at ``/home/user/hello-world`` directory and application's package at
``/home/user/hello-world/app``. Create the ``config`` directory next to application root.

.. sourcecode:: text

    /home/user/hello-world
    ├── /app
    │   └─ __init__.py
    ├── /config


Application setup
-----------------

In your application factory code:

.. sourcecode:: python

    from flask import Flask
    from flask_ampho import Ampho

    def create_app():
        return Ampho(Flask(__name__))


Configuration
-------------

Create file ``config/default.json`` and place following configuration into it:

.. sourcecode:: json

    {
      "SQLALCHEMY_DATABASE_URI": "postgresql+psycopg2://user:pass@localhost:5432/ampho",
      "SQLALCHEMY_TRACK_MODIFICATIONS": false,
      "AMPHO_MIGRATION_PACKAGES": [
        "app"
      ]
    }

Don't forget to replace database connection credentials with proper ones.

