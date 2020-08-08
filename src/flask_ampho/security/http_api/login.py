"""
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from flask import current_app
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask_ampho import Ampho
from flask_ampho.security import make_jwt

ampho = current_app.extensions['ampho']  # type: Ampho

p = RequestParser()
p.add_argument('login')
p.add_argument('password')


class Login(Resource):
    """Login resource
    """

    def post(self):
        """POST method handler
        """
        args = p.parse_args()
        t, claims = make_jwt({'login': args.get('login')})

        return {
            'token': t.serialize(),
            'ttl': t.validity,
            'leeway': t.leeway,
            'starts': claims['nbf'],
            'expires': claims['exp'],
        }
