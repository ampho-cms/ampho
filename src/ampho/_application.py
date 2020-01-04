"""Ampho Application
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import List, Dict
from copy import copy
from os import environ, getenv, getcwd
from os.path import join as path_join, isfile
from socket import gethostname
from getpass import getuser
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
        self._bundles = {}
        self._bundles_by_path = {}

        # Bundles are being loaded
        self._loading_bundles = []

        # Application's root dir
        kwargs.setdefault('root_path', getcwd())
        root_path = kwargs['root_path']

        # Construct instance path, because Flask constructs it in a wrong way in some cases
        if 'instance_path' not in kwargs:
            kwargs['instance_path'] = path_join(root_path, 'instance')

        # Construct absolute path to static dir
        if 'static_folder' not in kwargs:
            kwargs['static_folder'] = path_join(root_path, 'static')

        # Set Flask environment name
        environ.setdefault('FLASK_ENV', 'development' if getenv('FLASK_DEBUG') == '1' else 'production')

        # Call Flask's constructor
        kwargs.setdefault('instance_relative_config', True)
        super().__init__(__name__, **kwargs)

        # Load configuration
        config_names = ['default', getenv('FLASK_ENV'), f'{getuser()}@{gethostname()}']
        for config_name in config_names:
            config_path = path_join(self.instance_path, config_name) + '.json'
            if isfile(config_path):
                self.config.from_json(config_path)

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
    def bundles(self) -> Dict[str, Bundle]:
        """Get registered bundles by module name

        :rtype: Dict[str, Bundle]
        """
        return copy(self._bundles)

    @property
    def bundles_by_path(self) -> Dict[str, Bundle]:
        """Get registered bundles by path

        :rtype: Dict[str, Bundle]
        """
        return copy(self._bundles_by_path)

    def on_init(self, bundles: List[str]):
        """This method should be used to perform necessary application setup instead of overriding __init__().

        :param List[str] bundles: names of bundle modules which should be registered and loaded at application start.
        """
        with self.app_context():
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

        finally:
            self._loading_bundles.pop()

        return bundle
