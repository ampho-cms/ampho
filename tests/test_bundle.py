"""Ampho Bundle Tests
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from os.path import join as path_join
import pytest
from typing import Callable
from types import ModuleType
from flask import Blueprint
from ampho import Application, Bundle
from ampho.error import BundleImportError


class TestBundle:
    def test_bundle_object(self, app: Application, rand_bundle: Callable[[], str], rand_str: Callable[[], str]):
        r_str = rand_str()
        bundle_mod_name = rand_bundle()
        bundle = Bundle(app, bundle_mod_name)

        # Create bundle using non-existing module
        with pytest.raises(BundleImportError):
            Bundle(app, rand_str())

        # Typing
        assert isinstance(bundle.module, ModuleType)
        assert isinstance(bundle.blueprint, Blueprint) is True

        # Base properties
        assert bundle.cli == bundle.blueprint.cli
        assert bundle.command == bundle.blueprint.cli.command

        # Routing relates properties
        assert bundle.route == bundle.blueprint.route
        assert bundle.subdomain == bundle.blueprint.subdomain
        assert bundle.url_prefix == bundle.blueprint.url_prefix
        assert bundle.url_defaults == bundle.blueprint.url_values_defaults

        # Directories paths
        assert bundle.root_dir == bundle.blueprint.root_path
        assert bundle.tpl_dir == bundle.blueprint.template_folder
        assert bundle.res_dir == path_join(bundle.root_dir, 'res')
        assert bundle.locale_dir == path_join(bundle.root_dir, 'locale')
        assert bundle.static_dir == path_join(bundle.root_dir, 'static')

        # Paths generators
        assert bundle.res_path(r_str) == path_join(bundle.res_dir, r_str)
