"""Ampho Security API Tests
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from werkzeug import Response
from flask_restful import Api, Resource
from flask_ampho import Ampho
from flask_ampho.security import authorize
from .conftest import rand_str


class AuthorizableResource(Resource):
    @authorize
    def get(self):
        pass


def test_authorize(ampho: Ampho):
    """authorize() test
    """
    api_path = '/' + rand_str()
    res_path = '/' + rand_str()
    res_url = api_path + res_path

    api = Api(ampho.app, api_path)
    api.add_resource(AuthorizableResource, res_path)

    cli = ampho.app.test_client()

    # Unauthorized response
    resp = cli.get(res_url)  # type: Response
    assert resp.status_code == 401
