"""Ampho Application Tests
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import pytest
from typing import Callable
from ampho import Application, Bundle
from ampho.error import BundleAlreadyRegisteredError, BundleNotRegisteredError, BundleAlreadyLoadedError, \
    BundleNotLoadedError


class TestApplication:
    def test_bundle_register(self, app: Application, rand_bundle: Callable[[], Bundle]):
        bundle = rand_bundle()

        assert bundle == app.register_bundle(bundle)
        assert bundle == app.get_bundle(bundle.name)
        assert isinstance(app.bundles, dict)

        # Try to register the same bundle twice
        with pytest.raises(BundleAlreadyRegisteredError):
            app.register_bundle(bundle)

    def test_bundle_load(self, app: Application, rand_bundle: Callable[[], Bundle],
                         rand_str: Callable[[], str]):
        bundle = rand_bundle()

        assert bundle == app.register_bundle(bundle)

        # Try to load non-registered bundle
        with pytest.raises(BundleNotRegisteredError):
            app.load_bundle(rand_str())

        # Try to call methods that requires bundle to be loaded
        with pytest.raises(BundleNotLoadedError):
            bundle.render_tpl(rand_str())

        # Load bundle
        assert bundle == app.load_bundle(bundle.name)

        # Try to load the same bundle twice
        with pytest.raises(BundleAlreadyLoadedError):
            app.load_bundle(bundle.name)

    def test_bundle_methods(self, app: Application, rand_bundle: Callable[[], Bundle],
                            rand_str: Callable[[], str]):
        r_str = rand_str()
        bundle = app.load_bundle(app.register_bundle(rand_bundle()).name)

        assert bundle.gettext(r_str) == r_str

        # Random bundle has a template which contains a string.
        # Both template name and that string equal to the bundle's name
        assert bundle.render_tpl(bundle.name) == bundle.name
