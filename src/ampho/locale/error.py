"""Ampho Locale Bundle Errors
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class LocaleError(Exception):
    pass


class BundleDoesntSupportLocalizationError(LocaleError):
    def __init__(self, bundle: str):
        """Init
        """
        self._bundle = bundle

    def __str__(self):
        """__str__()
        """
        return f"Bundle '{self._bundle}' doesn't support localization"
