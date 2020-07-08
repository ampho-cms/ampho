"""Ampho Auth REST API
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from flask import Flask, current_app
from flask_restful import Api
from .login import Login

app = current_app  # type: Flask
api = app.extensions['ampho'].restful  # type: Api

api.add_resource(Login, '/login')
