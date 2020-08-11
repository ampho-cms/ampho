"""Ampho Security API
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Tuple, List
from time import time
from jwcrypto.jwk import JWK
from jwcrypto.jwt import JWT
from flask import Flask
from flask_ampho import Ampho
from flask_ampho.util import secho_warning


class Security:
    """Ampho Security API
    """

    def __init__(self, ampho: Ampho):
        """Init
        """
        self.token_ttl = ampho.get_config_int('AMPHO_SECURITY_TOKEN_TTL', 900)
        self.token_alg = ampho.get_config('AMPHO_SECURITY_TOKEN_ALG', 'HS256')

        k = ampho.get_config_json('AMPHO_SECURITY_KEY')
        if isinstance(k, dict):
            self.jwk = JWK(**k)

        if not self.jwk:
            self.jwk = JWK.generate(kty="oct", size=256)
            secho_warning("AMPHO_SECURITY_KEY is not set, Use 'ampho sec-gen-key' CLI command to generate a key.")

        @ampho.db.on_get_migrations_packages.connect_via(ampho.app)
        def on_db_get_migration_packages(sender: Flask, packages: List[str]):
            packages.append('flask_ampho.auth')

        # Register CLI commands
        with ampho.app.app_context():
            from . import _cli

    def make_jwt(self, claims: dict) -> Tuple[JWT, dict]:
        """Make a signed token
        """
        now = int(time())
        claims.update({
            'nbf': now,
            'exp': now + self.token_ttl
        })

        t = JWT(header={'alg': self.token_alg}, claims=claims)
        t.validity = self.token_ttl
        t.make_signed_token(key=self.jwk)

        return t, claims
