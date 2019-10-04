"""Ampho Application Tests
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Callable, Tuple
from ampho import Application


class TestApplication:
    def test_application(self, app: Application):
        assert isinstance(app, Application)

    def test_load_bundle(self, app: Application, random_bundle: Callable[[], Tuple[str, str]]):
        bundle = random_bundle()

        assert app.load_bundle(bundle[0]) == app.bundles[bundle[0]]
