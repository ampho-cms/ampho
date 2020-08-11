"""Ampho CMS Application
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import os
import logging
import json
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
    def __init__(self, app: Flask = None, sqlalchemy: SQLAlchemy = None, migrate: Migrate = None):
        """Init
        """
        self.root_path = path.dirname(__file__)
        self.app = app
        self.signals = BlinkerNamespace()
        self.cli = AppGroup('ampho')

        self.db = None
        self.security = None

        default_config_dir = path.abspath(path.join(app.root_path, path.pardir, 'config'))
        self.config_dir: str = self.get_config('AMPHO_CONFIG_DIR', default_config_dir)

        default_log_dir = path.abspath(path.join(self.app.root_path, path.pardir, 'log'))
        self.log_dir = self.get_config('AMPHO_LOG_DIR', default_log_dir)

        app.cli.add_command(self.cli)

        if app:
            self.init_app(app, sqlalchemy, migrate)

    def get_config(self, key: str, default: Any = None) -> Any:
        """Get config value
        """
        return self.app.config.get(key, os.getenv(key, default))

    def get_config_int(self, key: str, default: int = 0):
        """Get integer config value
        """
        return int(self.get_config(key, default))

    def get_config_bool(self, key: str, default: str = '1') -> bool:
        """Get boolean config value
        """
        return str(self.get_config(key, default)).lower() in ('1', 'yes', 'true')

    def get_config_json(self, key: str, default=None) -> Any:
        """Get JSON config value
        """
        v = self.get_config(key, default)
        if isinstance(v, str):
            v = json.loads(v)

        return v

    def load_config_dir(self):
        """Load configuration
        """
        if not path.isdir(self.config_dir):
            logging.warning(f'Configuration directory is not found at {self.config_dir}')
            return

        for config_name in ('default', os.getenv('FLASK_ENV', 'production'), f'{getuser()}@{gethostname()}'):
            for ext in ('.py', '.json'):
                config_path = path.join(self.config_dir, config_name) + ext
                if not path.isfile(config_path):
                    continue
                if ext == '.json':
                    self.app.config.from_json(config_path)
                else:
                    self.app.config.from_pyfile(config_path)

    def init_logging(self):
        """Init logging
        """
        # Set default log leve;
        if self.app.debug:
            logging.getLogger().setLevel(logging.DEBUG)

        # Ensure log directory
        os.makedirs(self.log_dir, 0o755, True)

        # Default format
        fmt = '%(asctime)s %(levelname)s'
        if self.app.debug or self.app.testing:
            fmt += ' %(filename)s:%(lineno)d'
        fmt += ': %(message)s'

        # Other parameters
        log_path = path.join(self.log_dir, self.app.name + '.log')
        rotate_when = self.get_config('AMPHO_LOG_ROTATE_WHEN', 'midnight')
        backup_count = int(self.get_config('AMPHO_LOG_BACKUP_COUNT', 30))

        # Setup handler
        handler = TimedRotatingFileHandler(log_path, rotate_when, backupCount=backup_count)
        handler.setFormatter(logging.Formatter(self.get_config('AMPHO_LOG_FORMAT', fmt)))
        logging.getLogger().addHandler(handler)

    def init_app(self, app: Flask, sqlalchemy: SQLAlchemy = None, migrate: Migrate = None):
        """Initialize Ampho
        """
        self.app = app
        app.extensions['ampho'] = self

        # Configuration
        if self.get_config_bool('AMPHO_CONFIG'):
            self.load_config_dir()

        # Logging
        if self.get_config_bool('AMPHO_LOG'):
            self.init_logging()

        # Database
        from .db import Db
        if not sqlalchemy:
            sqlalchemy = SQLAlchemy(app)
        self.db = Db(self, sqlalchemy, migrate or Migrate(app, sqlalchemy))

        if not self.security:
            from .security import Security
            self.security = Security(self)

        logging.info('Ampho %s initialized', __version__)
