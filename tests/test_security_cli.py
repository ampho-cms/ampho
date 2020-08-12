"""Ampho Security CLI Tests
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import json
from jwcrypto.jwk import JWKTypesRegistry
from flask_ampho import Ampho


def test_sec_gen_key(ampho: Ampho):
    """make_jwt() test
    """
    runner = ampho.app.test_cli_runner()

    from flask_ampho.security._cli import sec_gen_key
    result = runner.invoke(sec_gen_key)

    res_json = json.loads(result.output)

    assert isinstance(res_json, dict)
    assert 'k' in res_json
    assert res_json.get('kty') in JWKTypesRegistry
