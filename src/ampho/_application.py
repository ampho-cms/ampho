"""Ampho Application
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import List, Dict
from copy import copy
from os import getenv, getcwd
from os.path import join as path_join, isfile
from flask import Flask, Response
from htmlmin import minify
from .error import BundleNotRegisteredError, BundleAlreadyRegisteredError, BundleCircularDependencyError
from ._bundle import Bundle


class Application(Flask):
    """The application object implements a WSGI application and acts as the central object. Once it is created it will
    act as a central registry for the view functions, the URL rules and much more. For more information please read
    `Flask documentation <https://flask.palletsprojects.com/en/master/api/#application-object>`_

    :param bundle_names: names of bundle modules which should be registered at application start.
    """

    def __init__(self, bundle_names: List[str] = None, **kwargs):
        """Init
        """
        # Registered bundles
        self._bundles = {}

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

        # Call Flask's constructor
        kwargs.setdefault('instance_relative_config', True)
        super().__init__(__name__, **kwargs)

        # Load configuration
        config_names = ['default', getenv('FLASK_ENV', 'production')]
        for config_name in config_names:
            config_path = path_join(self.instance_path, config_name) + '.json'
            if isfile(config_path):
                self.config.from_json(config_path)

        # Build list bundles to load
        bundle_names = bundle_names or []
        bundle_names.extend(['ampho.locale'])
        bundle_names.extend(self.config.get('BUNDLES', []))

        # Let derived class to perform setup
        self.on_init(bundle_names)

        # Minify output in production mode
        if not self.debug:
            self.after_request_funcs.setdefault(None, []).append(self._minify_output)

    @staticmethod
    def _minify_output(response: Response):
        """Minify output
        """
        if response.content_type.startswith('text/html'):
            response.set_data(minify(response.get_data(as_text=True)))

        return response

    @property
    def bundles(self) -> Dict[str, Bundle]:
        """Get registered bundles by module name
        """
        return copy(self._bundles)

    def on_init(self, bundle_names: List[str]):
        """This method should be used to perform necessary application setup instead of overriding __init__().
        """
        with self.app_context():
            # Register bundles
            for name in bundle_names:
                self.register_bundle(name, True)

            # Initialize bundles
            for name in bundle_names:
                self.load_bundle(name, True)

    def get_bundle(self, name: str) -> Bundle:
        """Get a bundle object
        """
        if name in self._bundles:
            return self._bundles[name]

        raise BundleNotRegisteredError(name)

    def register_bundle(self, name: str, skip_registered: bool = False) -> Bundle:
        """Register a bundle
        """
        # Bundle must not be registered more than once
        if name in self._bundles:
            if skip_registered:
                return self._bundles[name]

            raise BundleAlreadyRegisteredError(name)

        # Instantiate bundle object
        bundle = self._bundles[name] = Bundle(name)

        # Register dependencies
        for req in bundle.requires:
            self.register_bundle(req, skip_registered)

        # Register bundle
        return bundle.register()

    def load_bundle(self, name: str, skip_loaded: bool = False) -> Bundle:
        """Load a bundle
        """
        if name in self._loading_bundles:
            raise BundleCircularDependencyError(name, self._loading_bundles)

        bundle = self.get_bundle(name)

        # Bundles must not be loaded more than once
        if bundle.is_loaded and skip_loaded:
            return bundle

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
