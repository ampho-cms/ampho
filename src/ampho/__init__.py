"""Ampho Init
"""
__description__ = 'Ampho is the core part of the Ampho CMS'
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'
__version__ = '0.2'

# Public API
from ._api import current_app, get_caller_bundle, request, route, render
from ._application import Application
from ._bundle import Bundle
