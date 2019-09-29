"""Ampho Application Tests
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from ampho import Application


class TestApplication:
    def test_application(self, app):
        app_import_name = app[0]  # type: str
        app = app[1]  # type: Application

        # Application name must equal to its module name
        assert app_import_name == app.name
