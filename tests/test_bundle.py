"""Ampho Bundle Tests
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import pytest  # type: ignore
from types import ModuleType
from os.path import join as path_join
from flask import Blueprint
from ampho import Bundle
from ampho.testing import AmphoApplicationTestCase
from ampho.errors import BundleImportError, BundleAlreadyRegisteredError, BundleCircularDependencyError, \
    BundleAlreadyLoadedError, BundleNotLoadedError, BundleAlreadyImportedError


class TestBundle(AmphoApplicationTestCase):
    """Ampho Bundle Tests
    """

    def test_create(self):
        """Bundle create test case
        """
        b_name = self.rand_bundle_struct()

        # Create a bundle
        bundle = Bundle(b_name)
        assert bundle.name == b_name

        # Create bundle from the same module more than once
        with pytest.raises(BundleAlreadyImportedError):
            Bundle(b_name)

        # Create a bundle using non-accessible module
        with pytest.raises(BundleImportError):
            Bundle(self.rand_str())

        # Test some properties which are not tested elsewhere
        assert self.entry_bundle.app == self.app

    def test_register(self):
        """Bundle registration test case
        """
        b_name = self.rand_bundle_struct()

        # Register a bundle
        bundle = self.app.register_bundle(b_name)
        assert bundle.name == b_name

        # Register the same bundle twice
        with pytest.raises(BundleAlreadyRegisteredError):
            self.app.register_bundle(b_name)

        # Register the same bundle twice, but without error
        assert self.app.register_bundle(b_name, True) == bundle

        # Load a bundle
        assert self.app.load_bundle(b_name) == bundle

        # Load the same bundle twice
        with pytest.raises(BundleAlreadyLoadedError):
            self.app.load_bundle(b_name)

        # Load the same bundle twice, but without error
        assert self.app.load_bundle(b_name, True) == bundle

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
        assert bundle.static_dir == path_join(bundle.root_dir, 'static')

        # Paths generators
        r_str = self.rand_str()
        assert bundle.res_path(r_str) == path_join(bundle.res_dir, r_str)

    def test_circular_dependency(self):
        """Bundle circular dependency test case
        """
        b_name_1 = self.rand_str()
        b_name_2 = self.rand_str()

        # Create two bundles which depends on each other
        self.rand_bundle_struct(self.tmp_dir, [b_name_2], b_name_1)
        self.rand_bundle_struct(self.tmp_dir, [b_name_1], b_name_2)

        # Register first bundle, which will cause send bundle registration
        self.app.register_bundle(b_name_1, True)

        # Loading first bundle should cause error
        with pytest.raises(BundleCircularDependencyError):
            self.app.load_bundle(b_name_1)

        # Loading second bundle should cause error as well
        with pytest.raises(BundleCircularDependencyError):
            self.app.load_bundle(b_name_2)

    def test_render(self):
        """Test bundle's render method
        """
        # Test loaded bundle render
        self.entry_bundle.render(self.entry_bundle.name + '.jinja2')

        # Test not loaded bundle
        bundle = Bundle(self.rand_bundle_struct())
        with pytest.raises(BundleNotLoadedError):
            bundle.render(bundle.name + '.jinja2')
