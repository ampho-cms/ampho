"""Ampho Bundle Tests
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from os.path import join as path_join
import pytest
from types import ModuleType
from flask import Blueprint
from ampho import Bundle
from ampho.testing import AmphoApplicationTestCase
from ampho.errors import BundleImportError, BundleAlreadyRegisteredError, BundleCircularDependencyError


class TestBundle(AmphoApplicationTestCase):
    """Ampho Bundle Tests
    """

    def test_bundle(self, tmp_path: str):
        """Bundle test cases
        """
        app = self.rand_app(tmp_path)

        # Create a bundle
        b_name = self.rand_bundle(tmp_path)

        # Create bundle using non-existing module
        with pytest.raises(BundleImportError):
            Bundle(self.rand_str())

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
        assert bundle.static_dir == path_join(bundle.root_dir, 'static')

        # Paths generators
        r_str = self.rand_str()
        assert bundle.res_path(r_str) == path_join(bundle.res_dir, r_str)

    def test_bundle_circular_dependency(self, tmp_path: str):
        """Bundle circular dependency test case
        """
        app = self.rand_app(tmp_path)
        b_name_1 = self.rand_str()
        b_name_2 = self.rand_str()

        # Create two bundles which depends on each other
        self.rand_bundle(tmp_path, [b_name_2], b_name_1)
        self.rand_bundle(tmp_path, [b_name_1], b_name_2)

        # Register first bundle, which will cause send bundle registration
        app.register_bundle(b_name_1, True)

        # Loading first bundle should cause error
        with pytest.raises(BundleCircularDependencyError):
            app.load_bundle(b_name_1)

        # Loading second bundle should cause error as well
        with pytest.raises(BundleCircularDependencyError):
            app.load_bundle(b_name_2)

    def test_render(self, tmp_path: str):
        """Test bundle's render method
        """
        app = self.rand_app(tmp_path, [self.rand_bundle(tmp_path)])
        bundle = list(app.bundles.values())[0]  # type: Bundle

        bundle.render(bundle.name + '.jinja2')
