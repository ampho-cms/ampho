"""Renew HTTP API Recource
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from flask_restful import Resource
from flask_ampho.security import authorize, make_jwt


class Renew(Resource):
    """Renew HTTP API Recource
    """

    @authorize
    def post(self, auth: dict):
        """POST method handler
        """
        return make_jwt(auth)
