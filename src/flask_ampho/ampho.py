"""Ampho CMS Application
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import os
import logging
from os import path
from socket import gethostname
from getpass import getuser
from logging.handlers import TimedRotatingFileHandler
from flask import Flask
from flask.cli import AppGroup
from flask_ampho import __version__
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api as RestfulApi


class Ampho:
    def __init__(self, app: Flask = None, db: SQLAlchemy = None, migrate: Migrate = None, restful: RestfulApi = None):
        """Init
        """
        self.app = app
        self.db = db
        self.migrate = migrate
        self.restful = restful

        self.cli = AppGroup('ampho')
        app.cli.add_command(self.cli)

        self.root_path = path.dirname(__file__)

        if app:
            self.init_app(app, db, migrate, restful)

    def _get_config_bool(self, key: str, default: str = '1') -> bool:
        """Get config boolean value
        """
        return str(self.app.config.get(key, default)).lower() in ('1', 'yes', 'true')

    def _init_config(self):
        """Load configuration
        """
        # Ensure config directory
        default_config_dir = path.abspath(path.join(self.app.instance_path, path.pardir, 'config'))
        config_dir = self.app.config.get('AMPHO_CONFIG_DIR', default_config_dir)
        os.makedirs(config_dir, 0o755, True)

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
        default_log_dir = path.abspath(path.join(self.app.instance_path, path.pardir, 'log'))
        log_dir = self.app.config.get('AMPHO_LOG_DIR', default_log_dir)
        os.makedirs(log_dir, 0o755, True)

        # Default format
        fmt = '%(asctime)s %(levelname)s'
        if self.app.debug or self.app.testing:
            fmt += ' %(filename)s:%(lineno)d'
        fmt += ': %(message)s'

        # Other parameters
        log_path = path.join(log_dir, self.app.name + '.log')
        rotate_when = self.app.config.get('AMPHO_LOG_ROTATE_WHEN', 'midnight')
        backup_count = int(self.app.config.get('AMPHO_LOG_BACKUP_COUNT', 30))

        # Setup handler
        handler = TimedRotatingFileHandler(log_path, rotate_when, backupCount=backup_count)
        handler.setFormatter(logging.Formatter(self.app.config.get('AMPHO_LOG_FORMAT', fmt)))
        logging.getLogger().addHandler(handler)

    def teardown(self, exception: Exception):
        pass

    def init_app(self, app: Flask, db: SQLAlchemy = None, migrate: Migrate = None, restful: RestfulApi = None):
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
            db = SQLAlchemy(app)
        self.db = db

        # Migrate
        if not migrate:
            migrate = Migrate(app, db)
        self.migrate = migrate

        # RESTful
        if not restful:
            version = app.config.get('AMPHO_RESTFUL_VERSION', '1')
            prefix = app.config.get('AMPHO_RESTFUL_PREFIX', f'/api/{version}')
            restful = RestfulApi(app, prefix)
        self.restful = restful

        # Submodules
        with app.app_context():
            from flask_ampho import db, auth

        logging.info('Ampho %s started', __version__)

        app.teardown_appcontext(self.teardown)
