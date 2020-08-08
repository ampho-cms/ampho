"""Ampho Security Related Utils
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import logging
from typing import Callable, Optional, Tuple
from time import time
from json import loads
from flask import current_app, request, abort
from flask_ampho import Ampho
from jwcrypto.jwt import JWT

ampho = current_app.extensions['ampho']  # type: Ampho
_TOKEN_TTL = ampho.get_config_int('AMPHO_SECURITY_TOKEN_TTL', 900)


def make_jwt(claims: dict) -> Tuple[JWT, dict]:
    """Make a signed token
    """
    now = int(time())
    alg = ampho.get_config('AMPHO_SECURITY_JWT_ALG', 'HS256')
    claims.update({
        'nbf': now,
        'exp': now + _TOKEN_TTL
    })

    t = JWT(header={'alg': alg}, claims=claims)
    t.validity = _TOKEN_TTL
    t.make_signed_token(key=ampho.jwk)

    return t, claims


def deserialize_token(s: str) -> JWT:
    """Deserialize a token from a string
    """
    return JWT(jwt=s, key=ampho.jwk)


def authorize(f: Callable):
    """Authorization decorator to use in request handlers
    """

    def deco(*args, **kwargs):
        auth = request.headers.get('Authorization')  # type: Optional[str]
        if not (auth and auth.lower().startswith('bearer')):
            abort(401)

        bearer = auth.split()
        if len(bearer) != 2:
            abort(401)

        try:
            t = JWT(jwt=bearer[1], key=ampho.jwk)
            kwargs['auth'] = loads(t.claims)
            return f(*args, **kwargs)

        except Exception as e:
            logging.error(e)
            abort(401)

    return deco
