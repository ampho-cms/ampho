"""Ampho Security API Tests
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from time import time
from flask_ampho import Ampho
from .conftest import rand_int, rand_str


def test_make_jwt(ampho: Ampho):
    """make_jwt() test
    """
    ttl = rand_int(1, 1000)
    ampho.app.config['AMPHO_SECURITY_TOKEN_TTL'] = ttl

    k = rand_str()
    v = rand_str()
    now = int(time())
    jwt, claims = ampho.security.make_jwt({k: v})

    assert jwt.validity == ttl
    assert claims['nbf'] == now
    assert claims['exp'] == now + ttl
    assert claims[k] == v
