"""Ampho Security Exceptions
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from flask_ampho.error import AmphoError


class SecurityError(AmphoError):
    pass


class InvalidTokenError(SecurityError):
    pass
