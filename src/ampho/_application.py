"""Ampho Application
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import logging
from typing import List, Mapping
from collections import OrderedDict
from copy import copy
from os import environ, getenv, getcwd, makedirs
from os.path import join as path_join, isfile, split as path_split, sep as path_sep, isdir
from socket import gethostname
from getpass import getuser
from logging.handlers import TimedRotatingFileHandler
from flask import Flask, Response
from htmlmin import minify
from .errors import BundleNotRegisteredError, BundleAlreadyRegisteredError, BundleCircularDependencyError, \
    BundleAlreadyLoadedError
from ._bundle import Bundle
from .signals import bundle_registered


class Application(Flask):
    """The application object implements a WSGI application. Once it is created it will act as a central registry for
    view functions, URL rules and all other application's stuff.

    :param List[str] bundles: names of bundle modules which should be registered and loaded at application start.
    :param str root_path: path to the root directory of the application.
    :param str instance_path: path to the instance directory of the application. Default is ``$root_path/instance``.
    :param str static_folder: path to the directory contains static files. default is ``$root_path/static``.
    :param bool instance_relative_config: is application configuration located relative to instance directory. Default
           is ``True``.
    """

    def __init__(self, bundles: List[str] = None, **kwargs):
        """Init
        """
        # Registered bundles
        self._bundles = OrderedDict()
        self._bundles_by_path = {}

        # Bundles are being loaded
        self._loading_bundles = []

        # Application's root dir path
        if 'root_path' not in kwargs:
            if 'VIRTUAL_ENV' in environ:
                kwargs['root_path'] = path_sep.join(path_split(getenv('VIRTUAL_ENV'))[:-1])
            else:
                kwargs['root_path'] = getcwd()

        # Construct instance path, because Flask constructs it in a wrong way in some cases
        if 'instance_path' not in kwargs:
            kwargs['instance_path'] = path_join(kwargs['root_path'], 'instance')

        # Construct absolute path to static dir
        if 'static_folder' not in kwargs:
            kwargs['static_folder'] = path_join(kwargs['root_path'], 'static')

        # Set Flask environment name
        environ.setdefault('FLASK_ENV', 'production')

        # Call Flask's constructor
        kwargs.setdefault('instance_relative_config', True)
        super().__init__(__name__, **kwargs)

        # Create temporary directory
        self._tmp_path = path_join(self.root_path, 'tmp')
        if not isdir(self._tmp_path):
            makedirs(self._tmp_path, 0o755)

        # Load configuration
        config_names = ['default', getenv('FLASK_ENV'), f'{getuser()}@{gethostname()}']
        for config_name in config_names:
            config_path = path_join(self.instance_path, config_name) + '.json'
            if isfile(config_path):
                self.config.from_json(config_path)

        # Set logging level
        if self.debug or self.testing:
            logging.getLogger().setLevel(logging.DEBUG)

        # Initialize timed rotating file logger handler
        if int(self.config.get('LOG_FILES_ENABLED', '1')):
            makedirs(self.log_path, 0o755, True)
            log_path = path_join(self.log_path, 'ampho.log')
            default_fmt = '%(asctime)s] %(levelname)s: %(message)s'
            log_format = self.config.get('LOG_FILES_MSG_FORMAT', default_fmt)
            backup_count = int(self.config.get('LOG_FILES_BACKUP_COUNT', 30))
            t_handler = TimedRotatingFileHandler(log_path, 'midnight', backupCount=backup_count)
            t_handler.setFormatter(logging.Formatter(log_format))
            logging.getLogger().addHandler(t_handler)

        # Bundles to load
        bundles = (bundles or []) + self.config.get('BUNDLES', [])

        # Let derived class to perform setup
        self.on_init(bundles)

        # Minify output in production mode
        if not self.debug:
            self.after_request_funcs.setdefault(None, []).append(self._minify)

    @staticmethod
    def _minify(response: Response) -> Response:
        """Minify response
        """
        if response.content_type.startswith('text/html'):
            response.set_data(minify(response.get_data(as_text=True)))

        return response

    @property
    def tmp_path(self) -> str:
        """Get application temporary directory path
        """
        return self._tmp_path

    @property
    def log_path(self) -> str:
        """Get log directory path
        """
        return path_join(self.root_path, self.config.get('LOG_FILES_PATH', 'log'))

    @property
    def bundles(self) -> Mapping[str, Bundle]:
        """Get registered bundles by module name

        :rtype: Dict[str, Bundle]
        """
        return copy(self._bundles)

    @property
    def bundles_by_path(self) -> Mapping[str, Bundle]:
        """Get registered bundles by path

        :rtype: Dict[str, Bundle]
        """
        return copy(self._bundles_by_path)

    def on_init(self, bundles: List[str]):
        """This method should be used to perform necessary application setup instead of overriding __init__().

        :param List[str] bundles: names of bundle modules which should be registered and loaded at application start.
        """
        # Register bundles
        for name in bundles:
            self.register_bundle(name, True)

        # Initialize bundles
        for name in bundles:
            self.load_bundle(name, True)

    def get_bundle(self, name: str) -> Bundle:
        """Get a bundle by name

        :param str name: bundle name.
        :rtype: Bundle
        :returns: A bundle instance.
        :raises BundleNotRegisteredError: if the bundle is not registered.
        """
        if name in self._bundles:
            return self._bundles[name]

        raise BundleNotRegisteredError(name)

    def register_bundle(self, name: str, skip_registered: bool = False) -> Bundle:
        """Register a bundle

        :param str name: bundle name
        :param bool skip_registered: should already registered name be silently skipped
        :returns: Bundle's instance.
        :rtype: Bundle
        :raises BundleAlreadyRegisteredError: if a bundle with the same name is already registered.
        """
        # Bundle must not be registered more than once
        if name in self._bundles:
            if skip_registered:
                return self._bundles[name]

            raise BundleAlreadyRegisteredError(name)

        # Instantiate bundle object
        bundle = Bundle(name)
        self._bundles[name] = bundle
        self._bundles_by_path[bundle.root_dir] = bundle

        # Register dependencies
        for req in bundle.requires:
            self.register_bundle(req, skip_registered)

        # Finish bundle registration
        bundle.register()
        bundle_registered.send(bundle)

        # Log
        logging.debug("Bundle registered: {}, {}".format(bundle.name, bundle.root_dir))

        return bundle

    def load_bundle(self, name: str, skip_loaded: bool = False) -> Bundle:
        """Load a bundle

        :param str name: bundle name.
        :param bool skip_loaded: don't raise :py:exc:`errors.BundleAlreadyLoadedError` in case if bundle with the same
            name is already registered.
        :returns: Bundle's instance.
        :rtype: Bundle
        :raises BundleCircularDependencyError: if a circular dependency was detected.
        :raises BundleAlreadyLoadedError: if the bundle is already loaded.
        """
        if name in self._loading_bundles:
            raise BundleCircularDependencyError(name, self._loading_bundles)

        # Get registered bundle instance
        bundle = self.get_bundle(name)

        # Bundles must not be loaded more than once
        if bundle.is_loaded:
            if skip_loaded:
                return bundle
            raise BundleAlreadyLoadedError(name)

        # Mark bundle as being loaded to prevent circular dependencies
        self._loading_bundles.append(name)

        try:
            # Load dependencies
            for req_name in bundle.requires:
                self.load_bundle(req_name, skip_loaded)

            # Load the bundle
            bundle.load(self)

            # Log
            logging.debug("Bundle '{}' loaded".format(bundle.name))

        finally:
            self._loading_bundles.pop()

        return bundle
