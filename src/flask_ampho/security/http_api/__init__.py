"""
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from flask import current_app
from flask_restful import Api
from flask_ampho import Ampho
from .login import Login
from .renew import Renew

ampho = current_app.extensions['ampho']  # type: Ampho

PREFIX = ampho.get_config('AMPHO_SECURITY_REST_PREFIX', '/api/security')

api_v1 = Api(current_app, f'{PREFIX}/1')
api_v1.add_resource(Login, '/login')
api_v1.add_resource(Renew, '/renew')
