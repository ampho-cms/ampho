"""Ampho CLI Test Cases
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import pytest  # type: ignore
from ampho.testing import AmphoApplicationTestCase
from ampho import cli


class TestCli(AmphoApplicationTestCase):
    """Ampho CLI Test Cases
    """

    def test_cli_echo(self):
        """Echo test cases
        """
        assert cli.echo(self.rand_str()) is None
        assert cli.echo(self.rand_int()) is None
        assert cli.echo_info(None) is None
        assert cli.echo_success(None) is None
        assert cli.echo_warning(None) is None

        with pytest.raises(SystemExit):
            assert cli.echo_error(self.rand_str(), True)
