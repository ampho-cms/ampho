"""Various API helpers
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from . import _application
from flask import Request as _Request
from werkzeug.contrib.sessions import Session as _Session
from flask import current_app as _app, request as _req, session as _sess

# Following variables are used just for type hinting purposes
current_app = _app  # type: _application.Application
request = _req  # type: _Request
session = _sess  # type: _Session
