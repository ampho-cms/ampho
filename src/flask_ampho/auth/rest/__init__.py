"""Ampho Auth REST API
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import List
from flask import Flask, current_app
from flask_restful import Api as RestfulApi
from flask_ampho.db import signal
from .login import Login

app = current_app  # type: Flask

r_api_v1 = RestfulApi(app, '/api/ampho/auth/1')
r_api_v1.add_resource(Login, '/login')
