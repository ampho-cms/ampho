"""Ampho Bundle Tests
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import pytest
from flask import Blueprint
from ampho import Application, error


class TestBundle:
    def test_application(self, app):
        app = app[1]  # type: Application

        for b_name, bundle in app.bundles.items():
            assert bundle.app == app
            assert bundle.name == b_name
            assert isinstance(bundle.blueprint, Blueprint) == True
            assert bundle.route == bundle.blueprint.route
            assert bundle.cli == bundle.blueprint.cli
            assert bundle.command == bundle.blueprint.cli.command

            with pytest.raises(error.BundleAlreadyRegisteredError):
                app.register_bundle(b_name)
