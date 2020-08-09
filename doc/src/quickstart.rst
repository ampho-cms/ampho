Quick start
===========

Installation
------------

.. sourcecode:: python

    pip install -U flask_ampho


File structure
--------------

Assume you have the source code root at ``/home/user/hello-world`` directory and application's package at
``/home/user/hello-world/app``.

.. sourcecode:: text

    /home/user/hello-world
    ├── /app
    │   └─ __init__.py


Application setup
-----------------

In your application factory code:

.. sourcecode:: python

    from flask import Flask
    from flask_ampho import Ampho

    def create_app():
        app = Flask(__name__)
        Ampho(app)

        return app


Security key
------------

In order to perform security related operations Ampho needs a security key. Ampho uses the JWK (JSON Web Key) standard
to store a key and have a CLI command to easily generate it:

.. sourcecode:: shell

    flask ampho sec-gen-key

.. sourcecode:: json

    {"k":"PkJ4gc1vCESz212pozSfjxpU66osYOIpi3X14OoHv7s","kty":"oct"}

Generated key must be placed into ``AMPHO_SECURITY_KEY`` configuration parameter. I hope that it's not necessary to
say one more time that **keeping the key in secret is vital**.


Configuration
-------------

Ampho provides it's own file based configuration mechanism

Create the ``config`` directory next to application root:

    /home/user/hello-world
    ├── /app
    ├── /config

Create file ``config/default.json`` and place following configuration into it:

.. sourcecode:: json

    {
      "SQLALCHEMY_DATABASE_URI": "postgresql+psycopg2://user:pass@localhost:5432/ampho",
      "SQLALCHEMY_TRACK_MODIFICATIONS": false,
      "AMPHO_SECURITY_KEY": {
        "k": "PkJ4gc1vCESz212pozSfjxpU66osYOIpi3X14OoHv7s",
        "kty": "oct"
      },
      "AMPHO_MIGRATION_PACKAGES": [
        "app"
      ]
    }

Don't forget to replace database connection credentials with proper ones.

