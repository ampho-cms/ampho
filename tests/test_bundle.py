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
from ampho import Bundle
from ampho.error import BundleImportError


class TestBundle:
    def test_bundle_object(self, rand_bundle: Callable[[], Bundle], rand_str: Callable[[], str]):
        r_str = rand_str()
        bundle = rand_bundle()

        # Create bundle using non-existing module
        with pytest.raises(BundleImportError):
            Bundle(rand_str())

        # Typing
        assert isinstance(bundle.module, ModuleType)
        assert isinstance(bundle.blueprint, Blueprint) == True

        # Base properties
        assert bundle.name == bundle.module_name
        assert bundle.cli == bundle.blueprint.cli
        assert bundle.command == bundle.blueprint.cli.command

        # Routing relates properties
        assert bundle.route == bundle.blueprint.route
        assert bundle.subdomain == bundle.blueprint.subdomain
        assert bundle.url_prefix == bundle.blueprint.url_prefix
        assert bundle.url_defaults == bundle.blueprint.url_values_defaults

        # Directories paths
        assert bundle.root_dir == bundle.blueprint.root_path
        assert bundle.static_dir == bundle.blueprint.static_folder
        assert bundle.tpl_dir == bundle.blueprint.template_folder
        assert bundle.res_dir == path_join(bundle.root_dir, 'res')
        assert bundle.locale_dir == path_join(bundle.root_dir, 'locale')

        # Paths generators
        assert bundle.res_path(r_str) == path_join(bundle.res_dir, r_str)
