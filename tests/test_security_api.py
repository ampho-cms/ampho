"""Ampho Security Api Tests
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from time import time
from .base import AmphoTestCase


class TestSecurityApi(AmphoTestCase):
    """Ampho Security Api Tests
    """

    def test_make_jwt(self, tmp_path):
        """make_jwt() test
        """
        ttl = self.rand_int(1, 1000)
        ampho = self.make_app(tmp_path, {
            'AMPHO_SECURITY_TOKEN_TTL': ttl,
        })

        k = self.rand_str()
        v = self.rand_str()
        now = int(time())
        jwt, claims = ampho.security.make_jwt({k: v})

        assert jwt.validity == ttl
        assert claims['nbf'] == now
        assert claims['exp'] == now + ttl
        assert claims[k] == v
