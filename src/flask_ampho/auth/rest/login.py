"""Ampho Auth REST API Login
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from flask_restful import Resource


class Login(Resource):
    def post(self):
        return {'Hello': 'World'}

    def get(self):
        return {'Hello': 'World'}
