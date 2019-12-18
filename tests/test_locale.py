"""Ampho Locale Bundle Tests
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from ampho import Application
from ampho.locale.error import BundleDoesntSupportLocalizationError


class TestLocale:
    def test_locale(self, app: Application):
        runner = app.test_cli_runner()

        result = runner.invoke(args=['locale', 'extract'])
        assert result.exit_code == 0

        for b_name in app.bundles:
            result = runner.invoke(args=['locale', 'init', 'en', b_name])
            if not isinstance(result.exception, BundleDoesntSupportLocalizationError):
                assert result.exit_code == 0

        result = runner.invoke(args=['locale', 'update', 'en'])
        assert result.exit_code == 0

        result = runner.invoke(args=['locale', 'compile'])
        assert result.exit_code == 0
