Database
========

Ampho uses `SQLAlchemy`_ and `Alembic`_ to deal with database management tasks, so there is nothing new for developers
familiar with these libraries and related tools. To reduce amount of code Ampho uses two popular Flask extensions:
`Flask SQLAlchemy`_ and `Flask Migrate`_ under the hood.


Setup
-----

In order to work properly Ampho expects `SQLAlchemy` and `Alembic` configured objects to be passed at initialization
time. If one of them or both isn't provided, Ampho will create them by itself, so in the simplest case you may
:doc:`initialize Ampho <setup>` as usual.

If you want to pass pre-configured `SQLAlchemy` and/or `Alembic` instances, you can do this using second and third Ampho
constructor's arguments:

.. sourcecode:: python

    from flask import Flask
    from flask_ampho import Ampho
    from flask_sqlalchemy import SQLAlchemy
    from flask_migrate import Migrate

    def create_app() -> Flask:
        app = Flask(__name__)

        db = SQLAlchemy(app)
        migrate = Migrate(app, db)

        Ampho(app, db, migrate)

        return app


Access database and migration objects
-------------------------------------

You can access `SQLAlchemy` and `Migration` instances in your code using ``db`` and ``migrate`` properties:

.. sourcecode:: python

    from flask import current_app

    ampho = current_app.extensions['ampho']
    db = ampho.db
    migrate = ampho.migrate


Migrations management
---------------------

Ampho allows to manage migrations separately for different parts of a project. In order to do this, Ampho uses `Alembic
branches`_ feature using Python package names for branches naming. For example, if you have application's code located
in the ``app`` package, then Ampho the ``app`` migrations name should be used in migration related CLI commands. In the
following examples it's assumed you're working with ``app`` package.


Environment initialization
^^^^^^^^^^^^^^^^^^^^^^^^^^

Before you can work with migrations, a migration environment must be created within a package using ``ampho db-init``
CLI command supplied with a package name:

.. sourcecode:: shell

    ampho db-init app

In case of success you'll find the ``migrations`` directory inside your package, fulfilled with standard Alembic's
file structure:

.. sourcecode:: text

    /app
    ├── /migrations
    │   ├── /versions
    │   ├── alembic.ini
    │   ├── env.py
    │   ├── README
    │   └── script.py.mako

Usually you don't have to change anything at that structure after initialization.


Revisions creation
^^^^^^^^^^^^^^^^^^

To create migration revisions the ``ampho db-rev`` CLI command should be used supplied with package name and short
description, i. e.:

.. sourcecode:: shell

    ampho db-rev app "Initial"

After this command successfully complete, you'll find a migration script under the ``versions`` directory:

.. sourcecode:: text

    /app
    ├── /migrations
    │   ├── /versions
    │   │   └── app_1595770095_initial.py


Writing migrations
^^^^^^^^^^^^^^^^^^

Please refer to the official `Alembic documentation`_ to find out corresponding information.


Revision specifiers
^^^^^^^^^^^^^^^^^^^

While working with schema modification commands like ``db-up`` and ``db-down`` you have deal with revision names. As
was said earlier, Ampho uses Python package names for Alembic branches labeling, therefore you may freely use syntax
provided by `Alembic branches`_ to specify revisions.


Schema upgrade
^^^^^^^^^^^^^^

Command syntax:

.. sourcecode:: shell

    ampho db-up [-s] [REVISION]

where ``-s`` options forces Ampho only to show SQL code which will be executed.

Apply all non-applied migrations:

.. sourcecode:: shell

    ampho db-up heads

or simply

.. sourcecode:: shell

    ampho db-up

Apply all non-applied migrations for a particular package:

.. sourcecode:: shell

    ampho db-up app@head

Upgrade to specific revision:

.. sourcecode:: shell

    ampho db-up app_1595770095

Upgrade 1 revision forward:

.. sourcecode:: shell

    ampho db-up app@+1


Schema downgrade
^^^^^^^^^^^^^^^^

Command syntax:

.. sourcecode:: shell

    ampho db-down [-s] [REVISION]

where ``-s`` options forces Ampho only to show SQL code which will be executed.

Move down by 1 revision:

.. sourcecode:: shell

    ampho db-down -1

or simply

.. sourcecode:: shell

    ampho db-down

Downgrade to the base:

.. sourcecode:: shell

    ampho db-down base

Move down by 1 revision for a particular package:

.. sourcecode:: shell

    ampho db-down app@-1

Fully downgrade for a particular package:

.. sourcecode:: shell

    ampho db-down app@base

Downgrade down to a particular revision:

.. sourcecode:: shell

    ampho db-down app_1595770095


Information about current revisions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Command syntax:

.. sourcecode:: shell

    ampho [-v] db-current

where ``-v`` enables verbose output.


Information about revisions
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Command syntax:

.. sourcecode:: shell

    ampho db-show [REVISION]

All revisions:

.. sourcecode:: shell

    ampho db-show

Revisions from a package:

.. sourcecode:: shell

    ampho db-show app

Particular revision:

.. sourcecode:: shell

    ampho db-show app_1595770095


Configuration
-------------

Please refer to the `Flask SQLAlchemy`_ and `Flask Migrate`_ documentation for configuration parameters list and
explanation.


AMPHO_MIGRATION_PACKAGES
^^^^^^^^^^^^^^^^^^^^^^^^

List of strings or comma-separated string. Specifies package names which provide migrations.


.. _SQLAlchemy: https://www.sqlalchemy.org/
.. _Alembic: https://alembic.sqlalchemy.org/
.. _Flask SQLAlchemy: https://flask-sqlalchemy.palletsprojects.com/
.. _Flask Migrate: https://flask-migrate.readthedocs.io/
.. _Alembic documentation: https://alembic.sqlalchemy.org/en/latest/
.. _Alembic branches: https://alembic.sqlalchemy.org/en/latest/branches.html
