"""Ampho Application
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import List, Dict
from copy import copy
from importlib.util import find_spec
from os import getenv
from os.path import join as path_join, split as path_split, pardir, abspath, isfile
from flask import Flask
from .bundle import Bundle


class Application(Flask):
    """The application object implements a WSGI application and acts as the central object. Once it is created it will
    act as a central registry for the view functions, the URL rules and much more. For more information please read
    `Flask documentation <https://flask.palletsprojects.com/en/master/api/#application-object>`_

    :param import_name: the name of the application package.
    :param bundles: names of bundle modules which should be registered at application start.
    """

    def __init__(self, import_name: str, bundles: List[str] = None, **kwargs):
        """Init
        """
        # Registered bundles
        self._bundles = {}

        # Application's root dir
        root_path = kwargs.get('root_path')
        if not root_path:
            root_path = abspath(path_join(*path_split(find_spec(import_name).origin)[:-1], pardir))
            kwargs['root_path'] = root_path

        # Construct instance path, because Flask constructs it in a wrong way in some cases
        if 'instance_path' not in kwargs:
            kwargs['instance_path'] = path_join(root_path, 'instance')

        # Construct absoulte path to static dir
        if 'static_folder' not in kwargs:
            kwargs['static_folder'] = path_join(root_path, 'static')

        # Call Flask's constructor
        kwargs.setdefault('instance_relative_config', True)
        super().__init__(import_name, **kwargs)

        # Load configuration
        config_path = path_join(self.instance_path, getenv('FLASK_ENV', 'production')) + '.json'
        if isfile(config_path):
            self.config.from_json(config_path)

        # Load bundles
        if bundles:
            for bundle_name in bundles:
                self.register_bundle(bundle_name)

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
