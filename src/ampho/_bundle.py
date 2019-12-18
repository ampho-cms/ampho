"""Ampho Bundle
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import sys
from gettext import bindtextdomain, dgettext
from typing import Optional, Tuple
from types import ModuleType
from importlib import import_module
from os.path import isdir, join as path_join, dirname, basename
from flask import Blueprint, render_template
from flask.cli import AppGroup
from .error import BundleImportError, BundleNotLoadedError, BundleAlreadyLoadedError


class Bundle:
    """TODO: write description

    Usually you don't need to use this class directly. Bundle instances are created by :class:`Application` during its
    startup.

    :param name: a Python module name.
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

    def __init__(self, name: str, **kwargs):
        """Init
        """
        # Because bundle may be re-imported multiple times (for example during testing),
        # it is important not to use Python's module cache and perform actual imports each time
        if name in sys.modules:
            del sys.modules[name]

        # Import bundle's module
        try:
            self._module = module = import_module(name)
        except ImportError:
            raise BundleImportError(name)

        # Bundle's name
        self._name = name

        # Bundle dependencies
        self._requires = tuple(kwargs.get('requires', getattr(module, 'BUNDLE_REQUIRES', ())))

        # Bundle's bound application
        self._app = None

        # Bundle's blueprint
        self._bp = None  # type: Optional[Blueprint]

        # Bundle's root dir path
        self._root_dir = root_dir = dirname(module.__file__)

        # Bundle resource directories paths
        self._locale_dir = self._res_dir = self._static_dir = self._tpl_dir = None  # type: Optional[str]
        for d_name in ('locale', 'res', 'static', 'tpl'):
            kw_d_name = kwargs.get(d_name)
            d_path = path_join(root_dir, kw_d_name or getattr(module, f'BUNDLE_{d_name.upper()}_DIR', d_name))
            setattr(self, f'_{d_name}_dir', d_path if isdir(d_path) else None)

        # Routes URLs defaults
        self._url_defaults = kwargs.get('url_defaults', getattr(module, 'BUNDLE_URL_DEFAULTS', {}))  # type: dict

        # Routes URL prefix
        self._url_prefix = kwargs.get('url_prefix', getattr(module, 'BUNDLE_URL_PREFIX', None))  # type: str

        # Routes subdomain
        self._subdomain = kwargs.get('subdomain', getattr(module, 'BUNDLE_SUBDOMAIN', None))  # type: str

        # Static URL prefix
        self._static_url_prefix = None  # type: Optional[str]
        if self._static_dir:
            pref = f'/{basename(self._static_dir)}/{self._name}'
            self._static_url_prefix = kwargs.get('static_url_prefix', getattr(module, 'BUNDLE_STATIC_URL_PREFIX', pref))

        # Bind gettext's domain
        if self._locale_dir:
            bindtextdomain(self._name, self._locale_dir)

    @property
    def name(self) -> str:
        """Bundle's name
        """
        return self._name

    @property
    def module(self) -> ModuleType:
        """Bundle's module
        """
        return self._module

    @property
    def requires(self) -> Tuple[str, ...]:
        """Bundle's requirements
        """
        return self._requires

    @property
    def app(self):
        """Get application object

        :rtype: ampho.Application
        """
        return self._app

    @property
    def is_loaded(self) -> bool:
        """Whether bundle is loaded
        """
        return self._app is not None

    @property
    def blueprint(self) -> Blueprint:
        """Bundle's `blueprint <https://flask.palletsprojects.com/en/master/api/#flask.Blueprint>`_.
        """
        return self._bp

    @property
    def root_dir(self) -> str:
        """Bundle's root path
        """
        return self._root_dir

    @property
    def locale_dir(self) -> Optional[str]:
        """Bundle's locale dir location
        """
        return self._locale_dir

    @property
    def res_dir(self) -> Optional[str]:
        """Bundle's resource dir location
        """
        return self._res_dir

    @property
    def static_dir(self) -> Optional[str]:
        """Bundle's static dir location
        """
        return self._static_dir

    @property
    def tpl_dir(self) -> Optional[str]:
        """Bundle's templates dir location
        """
        return self._tpl_dir

    @property
    def subdomain(self) -> Optional[str]:
        """Bundle's subdomain
        """
        return self._subdomain

    @property
    def url_prefix(self) -> Optional[str]:
        """Bundle's URL prefix
        """
        return self._url_prefix

    @property
    def url_defaults(self) -> dict:
        """Bundle's URL defaults
        """
        return self._url_defaults

    @property
    def route(self):
        """Bundle's `@router() decorator <https://flask.palletsprojects.com/en/master/quickstart/#routing>`_.
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

    def res_path(self, filename: str) -> str:
        """Get a resource file path
        """
        return path_join(self.res_dir, filename)

    def gettext(self, s: str) -> str:
        """Get translation of a string
        """
        return dgettext(self._name, s)

    def render(self, tpl: str, **args) -> str:
        """Render a template
        """
        if not self._app:
            raise BundleNotLoadedError(self._name)

        with self._app.app_context():
            args.update({
                '_': self.gettext,
                '_bundle': self,
            })
            return render_template(tpl, **args)

    def register(self):
        """Register the bundle
        """
        return self

    def load(self, app):
        """Init bundle
        """
        reg_options = {}

        # Check if the bundle is not already loaded
        if self._app:
            raise BundleAlreadyLoadedError(self._name)

        # Link to the application
        self._app = app

        # Create the Flask blueprint
        # It is important to NOT pass `static_folder` and `static_url_path` args, because we do not want to register
        # separate static routes for bundles.
        self._bp = Blueprint(self._name, self._name, None, None, self._tpl_dir, self._url_prefix, self._subdomain,
                             self._url_defaults, self._root_dir)

        # Initialize bundle's parts
        for sub_name in ('views', 'commands'):
            try:
                # Because bundle may be re-imported multiple times (for example during testing),
                # it is important not to use Python's module cache and perform actual imports each time
                sub_abs_name = f'{self._name}.{sub_name}'
                if sub_abs_name in sys.modules:
                    del sys.modules[sub_abs_name]

                # It is important not to cache 'ampho.bundle_ctx' module,
                # because it must update references to `g.current_bundle` each time it being imported
                if 'ampho.bundle_ctx' in sys.modules:
                    del sys.modules['ampho.bundle_ctx']

                # Import submodule within bundle context
                with self._app.app_context() as ctx:
                    ctx.g.current_bundle = self  # Make current bundle accessible in the currently imported module
                    module = import_module(sub_abs_name)

                    if sub_name == 'commands':
                        if hasattr(module, 'CLI_GROUP'):
                            reg_options['cli_group'] = module.CLI_GROUP
                        if hasattr(module, 'CLI_HELP'):
                            self._bp.cli.help = module.CLI_HELP

            except ModuleNotFoundError:
                pass

        # Register bundle's blueprint
        self._app.register_blueprint(self._bp, **reg_options)

        # Call bundle's initialization function
        hasattr(self._module, 'on_load') and callable(self._module.on_load) and self._module.on_load()

        return self
