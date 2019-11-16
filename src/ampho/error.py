"""Ampho Errors
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class AmphoError(Exception):
    """Base Ampho error
    """
    pass


class BundleNotFoundError(AmphoError):
    """Bundle's module is not found
    """

    @property
    def name(self) -> str:
        return self._name

    def __init__(self, name: str):
        self._name = name

    def __str__(self) -> str:
        return f"Bundle's module '{self._name}' is not found"


class BundleAlreadyRegisteredError(AmphoError):
    """Bundle with the same name is already registered
    """
    pass
