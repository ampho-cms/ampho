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
from .error import BundleNotRegisteredError, BundleAlreadyRegisteredError
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
        bundle_names = bundle_names or []

        # Registered bundles
        self._bundles = {}

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

        # Builtin bundles
        bundle_names.extend(['ampho.locale'])

        # Merge bundles list from configuration
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

    def on_init(self, module_names: List[str]):
        """This method should be used to perform necessary application setup instead of overriding __init__().
        """
        with self.app_context():
            # Register bundles
            for module_name in module_names:
                self.register_bundle(Bundle(module_name))

            # Initialize bundles
            for bundle_name in self._bundles:
                self.load_bundle(bundle_name)

    def get_bundle(self, name: str) -> Bundle:
        """Get a bundle object
        """
        if name in self._bundles:
            return self._bundles[name]

        raise BundleNotRegisteredError(name)

    def register_bundle(self, bundle: Bundle) -> Bundle:
        """Register a bundle
        """
        # Bundle name must ne unique
        if bundle.name in self._bundles:
            raise BundleAlreadyRegisteredError(bundle.name)

        # Register bundle
        self._bundles[bundle.name] = bundle

        return bundle

    def load_bundle(self, bundle_name: str) -> Bundle:
        """Initialize a bundle

        :param bundle_name: bundle's name
        """
        return self.get_bundle(bundle_name).load(self)
