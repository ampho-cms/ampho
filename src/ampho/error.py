"""Ampho Errors
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class AmphoError(Exception):
    """Base Ampho error"""
    pass


class BundleNotFoundError(AmphoError):
    """Bundle's module is not found
    """


class BundleAlreadyRegisteredError(AmphoError):
    """Bundle with the same name is already registered
    """
    pass
