"""Ampho Application
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import List, Dict
from copy import copy
from os import getenv, getcwd
from os.path import join as path_join, isfile
from flask import Flask
from .error import BundleNotFoundError
from ._bundle import Bundle


class Application(Flask):
    """The application object implements a WSGI application and acts as the central object. Once it is created it will
    act as a central registry for the view functions, the URL rules and much more. For more information please read
    `Flask documentation <https://flask.palletsprojects.com/en/master/api/#application-object>`_

    :param bundles: names of bundle modules which should be registered at application start.
    """

    def __init__(self, bundles: List[str] = None, **kwargs):
        """Init
        """
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
        bundles.extend(['ampho.locale'])

        # Merge bundles list from configuration
        bundles.extend(self.config.get('BUNDLES', []))

        # Register bundles
        if bundles:
            for bundle_name in bundles:
                self.register_bundle(bundle_name)

        # Initialize bundles
        for bundle in self.bundles.values():
            bundle.init()

        # Let derived class to perform setup
        self.on_init()

    @property
    def bundles(self) -> Dict[str, Bundle]:
        """Registered bundles
        """
        return copy(self._bundles)

    def on_init(self):
        """This method should be used to perform necessary application setup instead of overriding __init__().
        """
        pass

    def register_bundle(self, module_name: str) -> Bundle:
        """Register a bundle

        :param module_name: bundle's module name.
        """
        bundle = Bundle(self, module_name)
        self._bundles[bundle.name] = bundle

        return bundle

    def load_bundle(self, module_name: str) -> Bundle:
        """Register and initialize a bundle

        :param module_name: bundle's module name.
        """
        bundle = self.register_bundle(module_name)
        bundle.init()

        return bundle

    def get_bundle(self, name: str) -> Bundle:
        """Get a bundle object
        """
        if name not in self._bundles:
            raise BundleNotFoundError(name)

        return self._bundles[name]
