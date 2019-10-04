"""Ampho Bundle Tests
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import pytest
from types import ModuleType
from flask import Blueprint
from ampho import Application, error
from ampho.error import BundleNotFoundError
from .conftest import rand_str


class TestBundle:
    def test_app_bundle(self, app: Application):
        for b_name, bundle in app.bundles.items():
            assert isinstance(bundle.module, ModuleType)
            assert isinstance(bundle.blueprint, Blueprint) == True
            assert bundle.app == app
            assert bundle.name == b_name
            assert bundle.root_dir == bundle.blueprint.root_path
            assert bundle.static_dir == bundle.blueprint.static_folder
            assert bundle.tpl_dir == bundle.blueprint.template_folder
            assert bundle.subdomain == bundle.blueprint.subdomain
            assert bundle.url_prefix == bundle.blueprint.url_prefix
            assert bundle.url_defaults == bundle.blueprint.url_values_defaults
            assert bundle.route == bundle.blueprint.route
            assert bundle.cli == bundle.blueprint.cli
            assert bundle.command == bundle.blueprint.cli.command

            # Try to register the same bundle twice
            with pytest.raises(error.BundleAlreadyRegisteredError):
                app.register_bundle(b_name)

    def test_load_invalid_bundle(self, app: Application):
        with pytest.raises(BundleNotFoundError):
            app.load_bundle(rand_str())
