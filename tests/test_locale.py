"""Ampho Locale Bundle Tests
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Callable
from ampho import Application


class TestLocale:
    def test_locale(self, app: Application):
        runner = app.test_cli_runner()
        result = runner.invoke(args=['locale', 'extract'])
        assert result.exit_code == 0

        result = runner.invoke(args=['locale', 'init', 'en', list(app.bundles.keys())[0]])
        assert result.exit_code == 0

        result = runner.invoke(args=['locale', 'update', 'en'])
        assert result.exit_code == 0

        result = runner.invoke(args=['locale', 'compile'])
        assert result.exit_code == 0
