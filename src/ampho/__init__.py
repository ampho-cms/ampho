"""Ampho Init
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'
__description__ = 'Content management system based on Flask'
__version__ = '0.5'

import os
import logging
from os import path
from socket import gethostname
from getpass import getuser
from logging.handlers import TimedRotatingFileHandler
from flask import Flask
from ampho import error


def _get_config_bool(app: Flask, key: str, default: str = '1') -> bool:
    """Get config boolean value
    """
    return str(app.config.get(key, default)).lower() in ('1', 'yes', 'true')


def _init_config(app: Flask):
    """Load configuration
    """
    # Ensure config directory
    default_config_dir = path.abspath(path.join(app.instance_path, path.pardir, 'config'))
    config_dir = app.config.get('AMPHO_CONFIG_DIR')
    if not config_dir:
        config_dir = app.config['AMPHO_CONFIG_DIR'] = default_config_dir
    os.makedirs(config_dir, 0o755, True)

    for config_name in ('default', os.getenv('FLASK_ENV', ''), f'{getuser()}@{gethostname()}'):
        for ext in ('.py', '.json'):
            config_path = path.join(app.instance_path, config_name) + ext
            if not path.isfile(config_path):
                continue
            if ext == '.json':
                app.config.from_json(config_path)
            else:
                app.config.from_pyfile(config_path)


def _init_logging(app: Flask):
    """Init logging
    """
    # Ensure log directory
    default_log_dir = path.abspath(path.join(app.instance_path, path.pardir, 'log'))
    log_dir = app.config.get('AMPHO_LOG_DIR')
    if not log_dir:
        log_dir = app.config['AMPHO_LOG_DIR'] = default_log_dir
    os.makedirs(log_dir, 0o755, True)

    # Default format
    fmt = '%(asctime)s %(levelname)s'
    if app.debug or app.testing:
        fmt += ' %(filename)s:%(lineno)d'
    fmt += ': %(message)s'

    # Other parameters
    log_path = path.join(log_dir, app.name + '.log')
    backup_count = int(app.config.get('AMPHO_LOG_BACKUP_COUNT', 30))

    # Setup handler
    handler = TimedRotatingFileHandler(log_path, 'midnight', backupCount=backup_count)
    handler.setFormatter(logging.Formatter(app.config.get('AMPHO_LOG_FORMAT', fmt)))
    logging.getLogger().addHandler(handler)


def _init_db(app: Flask):
    """Initialize database
    """
    uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')  # type: str
    if not uri:
        raise error.ConfigurationError('SQLALCHEMY_DATABASE_URI configuration parameter is empty')

    app.config['SQLALCHEMY_DATABASE_URI'] = uri.replace('$INSTANCE', app.instance_path)


def ampho_init(app: Flask) -> Flask:
    """Initialize Ampho
    """
    # Ensure the instance folder exists
    os.makedirs(app.instance_path, 0o755, True)

    # Load configuration
    if _get_config_bool(app, 'AMPHO_CONFIG'):
        _init_config(app)

    # Update app name
    app.name = app.config.get('APP_NAME', app.name)

    # Initialize logging
    if _get_config_bool(app, 'AMPHO_LOG'):
        _init_logging(app)

    # Initialize database
    _init_db(app)

    logging.info('Ampho %s started', __version__)

    return app
