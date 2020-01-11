"""Ampho Application Tests
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import pytest
from ampho.testing import AmphoApplicationTestCase
from ampho.errors import BundleAlreadyRegisteredError, BundleNotRegisteredError, BundleAlreadyLoadedError, \
    BundleNotLoadedError


class TestApplication(AmphoApplicationTestCase):
    def test_bundle_register(self, tmp_path: str):
        app = self.rand_app(tmp_path)

        b_name = self.rand_bundle(tmp_path)
        bundle = app.register_bundle(b_name)

        assert bundle == app.get_bundle(b_name)
        assert bundle.name in app.bundles
        assert isinstance(app.bundles, dict)

        # Try to register the same bundle twice
        with pytest.raises(BundleAlreadyRegisteredError):
            app.register_bundle(b_name)

    def test_bundle_load(self, tmp_path: str):
        app = self.rand_app(tmp_path)

        # Create and register a bundle
        bundle_name = self.rand_bundle(tmp_path)
        bundle = app.register_bundle(bundle_name)

        # Try to load non-registered bundle
        with pytest.raises(BundleNotRegisteredError):
            app.load_bundle(self.rand_str())

        # Try to call methods that require bundle to be loaded
        with pytest.raises(BundleNotLoadedError):
            bundle.render(self.rand_str())

        # Load bundle
        assert bundle.is_loaded is False
        assert app.load_bundle(bundle_name) is bundle
        assert bundle.app is app
        assert bundle.is_loaded is True

        # Try to load the same bundle twice
        with pytest.raises(BundleAlreadyLoadedError):
            app.load_bundle(bundle_name)

        # Load the same bundle, but without exception
        assert app.load_bundle(bundle_name, True) is bundle

    def test_bundle_methods(self, tmp_path: str):
        app = self.rand_app(tmp_path)
        bundle = app.load_bundle(app.register_bundle(self.rand_bundle(tmp_path)).name)

        # Random bundle has a template which contains a string.
        # Both template name and that string equal to the bundle's name.
        # See `conftest.py` for details
        assert bundle.render(bundle.name, some_variable=bundle.name) == bundle.name

    def test_request(self, tmp_path: str):
        client = self.rand_app(tmp_path, [self.rand_bundle(tmp_path)]).test_client()
        r_str = self.rand_str()

        assert client.get(f'/{r_str}').data == r_str.encode()
