"""Ampho CMS Application
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import os
import logging
from typing import Any
from os import path
from socket import gethostname
from getpass import getuser
from logging.handlers import TimedRotatingFileHandler
from blinker import Namespace as BlinkerNamespace
from flask import Flask
from flask.cli import AppGroup
from flask_ampho import __version__
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


class Ampho:
    def __init__(self, app: Flask = None, db: SQLAlchemy = None, migrate: Migrate = None):
        """Init
        """
        self.app = app
        self.db = db
        self.migrate = migrate
        self.signals = BlinkerNamespace()

        self.cli = AppGroup('ampho')
        app.cli.add_command(self.cli)

        self.root_path = path.dirname(__file__)

        if app:
            self.init_app(app, db, migrate)

    def _get_config(self, key: str, default: Any = None) -> Any:
        """Get config value
        """
        return self.app.config.get(key, os.getenv(key, default))

    def _get_config_bool(self, key: str, default: str = '1') -> bool:
        """Get config boolean value
        """
        return str(self._get_config(key, default)).lower() in ('1', 'yes', 'true')

    def _init_config(self):
        """Load configuration
        """
        # Ensure config directory
        default_config_dir = path.abspath(path.join(self.app.root_path, path.pardir, 'config'))
        config_dir = self._get_config('AMPHO_CONFIG_DIR', default_config_dir)

        if not path.isdir(config_dir):
            logging.warning(f'Configuration directory is not found at {config_dir}')
            return

        for config_name in ('default', os.getenv('FLASK_ENV', ''), f'{getuser()}@{gethostname()}'):
            for ext in ('.py', '.json'):
                config_path = path.join(config_dir, config_name) + ext
                if not path.isfile(config_path):
                    continue
                if ext == '.json':
                    self.app.config.from_json(config_path)
                else:
                    self.app.config.from_pyfile(config_path)

    def _init_logging(self):
        """Init logging
        """
        # Set default log leve;
        if self.app.debug:
            logging.getLogger().setLevel(logging.DEBUG)

        # Ensure log directory
        default_log_dir = path.abspath(path.join(self.app.root_path, path.pardir, 'log'))
        log_dir = self._get_config('AMPHO_LOG_DIR', default_log_dir)
        os.makedirs(log_dir, 0o755, True)

        # Default format
        fmt = '%(asctime)s %(levelname)s'
        if self.app.debug or self.app.testing:
            fmt += ' %(filename)s:%(lineno)d'
        fmt += ': %(message)s'

        # Other parameters
        log_path = path.join(log_dir, self.app.name + '.log')
        rotate_when = self._get_config('AMPHO_LOG_ROTATE_WHEN', 'midnight')
        backup_count = int(self._get_config('AMPHO_LOG_BACKUP_COUNT', 30))

        # Setup handler
        handler = TimedRotatingFileHandler(log_path, rotate_when, backupCount=backup_count)
        handler.setFormatter(logging.Formatter(self._get_config('AMPHO_LOG_FORMAT', fmt)))
        logging.getLogger().addHandler(handler)

    def teardown(self, exception: Exception):
        pass

    def init_app(self, app: Flask, db: SQLAlchemy = None, migrate: Migrate = None):
        """Initialize Ampho
        """
        self.app = app
        app.extensions['ampho'] = self

        # Configuration
        if self._get_config_bool('AMPHO_CONFIG'):
            self._init_config()

        # Logging
        if self._get_config_bool('AMPHO_LOG'):
            self._init_logging()

        # Database
        if not db:
            self.db = SQLAlchemy(app)

        # Migrate
        if not migrate:
            self.migrate = Migrate(app, self.db)

        # Initialize submodules
        with app.app_context():
            from flask_ampho import db, auth

        logging.info('Ampho %s started', __version__)

        app.teardown_appcontext(self.teardown)
