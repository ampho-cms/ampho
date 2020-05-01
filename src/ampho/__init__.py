"""Ampho Init
"""
__description__ = 'Ampho is a Python library that provides simple and convenient way to develop Flask applications'
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'
__version__ = '0.4.1'

# Public API
from ._api import current_app, get_caller_bundle, request, route, render
from ._application import Application
from ._bundle import Bundle
