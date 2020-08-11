"""Ampho Security Related Utils
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import logging
from typing import Callable, Optional

from json import loads
from flask import current_app, request, abort
from flask_ampho import Ampho
from jwcrypto.jwt import JWT


def authorize(f: Callable):
    """Authorization decorator to use in request handlers
    """

    def deco(*args, **kwargs):
        ampho = current_app.extensions['ampho']  # type: Ampho
        auth = request.headers.get('Authorization')  # type: Optional[str]
        if not (auth and auth.lower().startswith('bearer')):
            abort(401)

        bearer = auth.split()
        if len(bearer) != 2:
            abort(401)

        try:
            t = JWT(jwt=bearer[1], key=ampho.security.jwk)
            kwargs['auth'] = loads(t.claims)
            return f(*args, **kwargs)

        except Exception as e:
            logging.error(e)
            abort(401)

    return deco
