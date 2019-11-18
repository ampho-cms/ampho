"""Ampho Application Tests
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import pytest
from typing import Callable
from ampho import Application, Bundle
from ampho.error import BundleAlreadyRegisteredError, BundleNotRegisteredError
from .conftest import rand_str


class TestApplication:
    def test_application(self, app: Application):
        assert isinstance(app, Application)

    def test_register_bundle(self, app: Application, rand_bundle: Callable[[], Bundle]):
        bundle = rand_bundle()

        assert bundle == app.register_bundle(bundle)
        assert bundle == app.get_bundle(bundle.name)

        # Try to register the same bundle twice
        with pytest.raises(BundleAlreadyRegisteredError):
            app.register_bundle(bundle)

    def test_load_bundle(self, app: Application, rand_bundle: Callable[[], Bundle]):
        bundle = rand_bundle()

        app.register_bundle(bundle)

        assert bundle == app.load_bundle(bundle.name)

        # Try to load non-registered bundle
        with pytest.raises(BundleNotRegisteredError):
            app.load_bundle(rand_str())
