"""Ampho Application Tests
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import pytest  # type: ignore
from os import environ
from ampho import Bundle
from ampho.testing import AmphoApplicationTestCase
from ampho.errors import BundleNotRegisteredError, BundleImportError, BundleAlreadyLoadedError


class TestApplication(AmphoApplicationTestCase):
    """Ampho Application Tests
    """

    def test_invalid_entry_bundle(self):
        """Invalid entry bundle test case
        """
        tmp_dir = self.make_tmp_dir()
        environ['AMPHO_ENTRY'] = self.rand_str()

        with pytest.raises(BundleImportError):
            self.rand_app(tmp_dir=tmp_dir)

    def test_load(self):
        """Bundle load test case
        """
        b_name = self.rand_bundle_struct()

        bundle = Bundle(b_name)
        assert not bundle.is_loaded

        bundle.load(self.app)
        assert bundle.is_loaded

        # Try to load loaded bundle again
        with pytest.raises(BundleAlreadyLoadedError):
            bundle.load(self.app)

    def test_get_bundle(self):
        """Get bundle test case
        """
        # Get registered and loaded bundle
        assert self.app.get_bundle(self.entry_bundle.name) == self.entry_bundle

        # Get non-registered bundle
        with pytest.raises(BundleNotRegisteredError):
            self.app.get_bundle(self.rand_str())

    def test_properties(self):
        """'bundles' property test case
        """
        assert self.app.tmp_path
        assert len(self.app.bundles) == 1

    def test_request(self):
        """Bundle HTTP request test case
        """
        client = self.app.test_client()
        r_str = self.rand_str()

        assert client.get(f'/{r_str}').data == r_str.encode()
