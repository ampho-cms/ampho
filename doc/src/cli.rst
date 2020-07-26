CLI
===

Ampho registers its own Flask `CLI group`_ named ``ampho`` which is used for storing Ampho related CLI commands.
To see all available commands use following command:

.. sourcecode:: bash

    flask ampho --help

If you plan to use Ampho commands often, it may be convenient to setup `shell alias`_:

.. sourcecode:: bash

    alias ampho='flask ampho'

and then avoid typing ``flask`` while calling commands from ``ampho`` group, i. e.:

.. sourcecode:: bash

    ampho db-up


.. _CLI group: https://flask.palletsprojects.com/en/1.1.x/cli/
.. _shell alias: https://www.gnu.org/software/bash/manual/html_node/Aliases.html
