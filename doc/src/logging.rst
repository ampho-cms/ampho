Logging
=======

By default at initialization time Ampho sets up separate root `TimedRotatingFileHandler`_ log handler amd formatter. The
``when`` argument. Set ``AMPHO_LOG`` to ``0`` if you want to disable this feature.


Configuration
-------------

* **int** ``AMPHO_LOG``. Whether to enable Ampho logger. Default is ``1``. Set to ``0`` to disable.
* **str** ``AMPHO_LOG_DIR``. Log directory location. Default is the ``log`` directory located next to application's
  instance directory.
* **str** ``AMPHO_LOG_FORMAT``. Log format. Default is ``"%(asctime)s %(levelname)s  %(filename)s:%(lineno)d"`` if the
  ``DEBUG`` configuration parameter is set to ``1``, and ``"%(asctime)s %(levelname)s"`` otherwise.
* **str** ``AMPHO_LOG_BACKUP_WHEN``. When to roll over backup files. Default is ``"midnight"``. See
  `TimedRotatingFileHandler`_ documentation for possible values.
* **int** ``AMPHO_LOG_BACKUP_COUNT``. Number of files kept int the log directory. Default is ``30``.


.. _TimedRotatingFileHandler: https://docs.python.org/3/library/logging.handlers.html#logging.handlers.TimedRotatingFileHandler
