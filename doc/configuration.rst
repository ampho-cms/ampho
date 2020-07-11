Configuration
=============

In addition to standard `Flask configuration`_ Ampho proposes its own file based configuration mechanism.

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

.. _Flask configuration: https://flask.palletsprojects.com/en/1.1.x/config/
