"""Ampho Bundle Tests
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from os.path import join as path_join
import pytest
from typing import Callable, List
from types import ModuleType
from flask import Blueprint
from ampho import Application, Bundle
from ampho.error import BundleImportError, BundleAlreadyRegisteredError, BundleCircularDependencyError


class TestBundle:
    def test_bundle(self, app: Application, rand_bundle: Callable[[], str], rand_str: Callable[[], str]):
        # Create a bundle
        b_name = rand_bundle()

        # Create bundle using non-existing module
        with pytest.raises(BundleImportError):
            Bundle(rand_str())

        # Register bundle
        bundle = app.register_bundle(b_name)

        # Try to register the same bundle twice
        with pytest.raises(BundleAlreadyRegisteredError):
            app.register_bundle(b_name)

        # Register the same bundle twice, but without error
        assert app.register_bundle(b_name, True) == bundle

        # Register and load the bundle to perform further tests
        bundle = app.load_bundle(b_name)

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
        r_str = rand_str()
        assert bundle.res_path(r_str) == path_join(bundle.res_dir, r_str)

    def test_bundle_circular_dependency(self, app: Application, rand_str: Callable[[], str],
                                        rand_bundle: Callable[[List[str], str], str]):
        b_name_1 = rand_str()
        b_name_2 = rand_str()

        # Create two bundles which depends on each other
        rand_bundle([b_name_2], b_name_1)
        rand_bundle([b_name_1], b_name_2)

        # Register first bundle, which will cause send bundle registration
        app.register_bundle(b_name_1, True)

        # Loading first bundle should cause error
        with pytest.raises(BundleCircularDependencyError):
            app.load_bundle(b_name_1)

        # Loading second bundle should cause error as well
        with pytest.raises(BundleCircularDependencyError):
            app.load_bundle(b_name_2)
