"""Ampho Application Tests
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import pytest
from typing import Callable
from ampho import Application
from ampho.error import BundleAlreadyRegisteredError, BundleNotRegisteredError, BundleAlreadyLoadedError, \
    BundleNotLoadedError


class TestApplication:
    def test_bundle_register(self, app: Application, rand_bundle: Callable[[], str]):
        bundle_mod_name = rand_bundle()
        bundle = app.register_bundle(bundle_mod_name)

        assert bundle == app.get_bundle(bundle_mod_name)
        assert bundle.name in app.bundles
        assert isinstance(app.bundles, dict)

        # Try to register the same bundle twice
        with pytest.raises(BundleAlreadyRegisteredError):
            app.register_bundle(bundle_mod_name)

    def test_bundle_load(self, app: Application, rand_bundle: Callable[[], str], rand_str: Callable[[], str]):
        # Create and register a bundle
        bundle_name = rand_bundle()
        bundle = app.register_bundle(bundle_name)

        # Try to load non-registered bundle
        with pytest.raises(BundleNotRegisteredError):
            app.load_bundle(rand_str())

        # Try to call methods that require bundle to be loaded
        with pytest.raises(BundleNotLoadedError):
            bundle.render(rand_str())

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

    def test_bundle_methods(self, app: Application, rand_bundle: Callable[[], str],
                            rand_str: Callable[[], str]):
        r_str = rand_str()

        bundle = app.load_bundle(app.register_bundle(rand_bundle()).name)

        assert bundle.gettext(r_str) == r_str

        # Random bundle has a template which contains a string.
        # Both template name and that string equal to the bundle's name.
        # See `conftest.py` for details
        assert bundle.render(bundle.name) == bundle.name

    def test_request(self, app: Application, rand_str: Callable[[], str]):
        client = app.test_client()
        r_str = rand_str()

        assert client.get(f'/{r_str}').data == r_str.encode()
