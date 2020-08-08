"""Ampho Security
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from .api import make_jwt, deserialize_token, authorize


def _init():
    from typing import List
    from flask import Flask, current_app
    from flask_ampho.db import signal
    from flask_ampho import Ampho
    from jwcrypto.jwk import JWK
    from ..util import secho_warning
    from . import cli, http_api

    app = current_app  # type: Flask
    ampho = app.extensions['ampho']  # type: Ampho

    k = ampho.get_config_json('AMPHO_SECURITY_KEY')
    if isinstance(k, dict):
        ampho.jwk = JWK(**k)

    if not ampho.jwk:
        ampho.jwk = JWK.generate(kty="oct", size=256)
        secho_warning("AMPHO_SECURITY_KEY is not set, Use 'ampho sec-gen-key' CLI command to generate a key.")

    @signal.gmp.connect_via(app)
    def on_db_get_migration_packages(sender: Flask, packages: List[str]):
        packages.append('flask_ampho.auth')


_init()
