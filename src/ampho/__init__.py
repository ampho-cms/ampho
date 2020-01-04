"""Ampho
"""
__description__ = 'Ampho is the core part of the Ampho CMS -- simple framework for building complex web applications'
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'
__version__ = '0.0.1'

# Public API
from ._api import app, get_caller_bundle, request, route, command, render
from ._application import Application
from ._bundle import Bundle
