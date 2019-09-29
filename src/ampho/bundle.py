"""Ampho Bundle
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from importlib import import_module
from os.path import isdir, join as path_join, dirname
from flask import Blueprint
from flask.cli import AppGroup
from .error import BundleAlreadyRegisteredError


class Bundle:
    """Bundle is a simple abstraction over the `Flask's blueprint concept <https://flask.palletsprojects.com/en/master/
    blueprints/>`_. Primary aim of using bundles is to automate blueprints setup routines by providing useful defaults
    and extra helpers that make it easier to accomplish common tasks. You don't need to instantiate blueprint objects
    manually, just create regular Python module/package contains couple of predefined names and/or folders and bundle
    will do all the work for you.

    Usually you don't need to use this class directly. Bundle instances are created by :class:`Application` during its
    startup.

    :param app: an :class:`Application` instance.
    :param module_name: a Python module name.
    :param name: the name of the bundle. Will be prepended to each endpoint name. If it's not specified the
        ``BUNDLE_NAME`` module's property will be used. If it's not specified, value of the :attr:`module_name` argument
        will be used.
    :param static_dir: path to a folder with static files relative to the bundle's root. If it's not specified the
        ``BUNDLE_STATIC_DIR`` module's property will be used. If it's not specified ``static`` will be used.
    :param tpl_dir: path to a folder with templates relative to the bundle's root. If it's not specified the
        ``BUNDLE_TPL_DIR`` module's property will be used. If it's not specified ``tpl`` will be used.
    :param url_prefix: a path to prepend to all of the bundle's URLs. If it's not specified the ``BUNDLE_URL_PREFIX``
        module's property will be used.
    :param subdomain: a subdomain that bundle routes will match on by default. If it's not specified the
        ``BUNDLE_SUBDOMAIN`` module's property will be used.
    :param url_defaults: a default values that bundle views will receive by default. If it's not specified the
        ``BUNDLE_URL_DEFAULTS`` module's property will be used.
    """

    def __init__(self, app, module_name: str, name: str = None, static_dir: str = None, static_url_prefix: str = None,
                 tpl_dir: str = None, url_prefix: str = None, subdomain: str = None, url_defaults: dict = None):
        """Init

        :type app: ampho.Application
        """
        self._app = app

        with app.app_context():
            module = import_module(module_name)

        # Bundle's properties
        name = name or getattr(module, 'BUNDLE_NAME', name) or module_name
        static_dir = static_dir or getattr(module, 'BUNDLE_STATIC_DIR', 'static')
        static_url_prefix = static_url_prefix or getattr(module, 'BUNDLE_STATIC_URL_PREFIX', f'/{static_dir}/{name}')
        tpl_dir = tpl_dir or getattr(module, 'BUNDLE_TPL_DIR', 'tpl')
        url_prefix = url_prefix or getattr(module, 'BUNDLE_URL_PREFIX', None)
        subdomain = subdomain or getattr(module, 'BUNDLE_SUBDOMAIN', None)
        url_defaults = url_defaults or getattr(module, 'BUNDLE_URL_DFAULTS', None)

        # Because bundle name is actually blueprint's name,
        # is is necessary to check for collisions before registering blueprint in the application
        if name in app.bundles:
            raise BundleAlreadyRegisteredError(f"Bundle '{name}' is already registered")

        # Check paths
        root_path = dirname(module.__file__)
        static_dir = static_dir if static_dir and isdir(path_join(root_path, static_dir)) else None
        tpl_dir = tpl_dir if tpl_dir and isdir(path_join(root_path, tpl_dir)) else None

        # Create blueprint
        self._bp = Blueprint(name, module_name, static_dir, static_url_prefix, tpl_dir, url_prefix, subdomain,
                             url_defaults, root_path)

        # Call bundle's initialization hook
        if hasattr(module, 'init_bundle') and callable(module.init_bundle):
            module.init_bundle(self)

        # Initialize views and commands
        for sub_module_name in ('view', 'command'):
            try:
                with app.app_context() as ctx:
                    ctx.g.bundle = self
                    import_module(f'{module_name}.{sub_module_name}')
            except ModuleNotFoundError:
                pass

        app.register_blueprint(self._bp)

    @property
    def app(self):
        """Application instance

        :type: ampho.Application
        """
        return self._app

    @property
    def blueprint(self) -> Blueprint:
        """Bundle's `blueprint <https://flask.palletsprojects.com/en/master/api/#flask.Blueprint>`_.
        """
        return self._bp

    @property
    def name(self) -> str:
        """Bundle's name
        """
        return self._bp.name

    @property
    def route(self):
        """Bundle's `@router() decorator <https://flask.palletsprojects.com/en/
        master/quickstart/#routing>`_.
        """
        return self._bp.route

    @property
    def cli(self) -> AppGroup:
        """Bundle's `AppGroup <https://flask.palletsprojects.com/en/master/api/#command-line-interface>`_.
        """
        return self._bp.cli

    @property
    def command(self):
        """Bundle's `@command decorator <https://flask.palletsprojects.com/en/master/cli/#custom-commands>`_
        """
        return self._bp.cli.command
