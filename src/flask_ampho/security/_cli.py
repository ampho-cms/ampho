"""Ampho Security CLI Commands
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import click
from flask import current_app
from jwcrypto.jwk import JWK
from flask_ampho import Ampho

ampho = current_app.extensions['ampho']  # type: Ampho


@ampho.cli.command()
def sec_gen_key():
    """Generate a JSON web key
    """
    click.echo(JWK.generate(kty="oct", size=256).export())
