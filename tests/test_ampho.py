"""Ampho Tests
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import os
import pytest
import json
from socket import gethostname
from getpass import getuser
from .base import AmphoTestCase


class TestAmpho(AmphoTestCase):
    """Ampho Test Case
    """

    def test_get_config(self, tmp_path: str):
        """Test get_config()
        """
        # Set configuration directly
        k = self.rand_str().upper()
        v = self.rand_str()
        ampho = self.make_app(tmp_path, {k: v})
        assert ampho.get_config(k) == v

        # Set configuration at runtime
        k = self.rand_str().upper()
        v = self.rand_str()
        assert ampho.get_config(k) is None
        ampho.app.config.from_mapping({k: v})
        assert ampho.get_config(k) == v

        # Set configuration via environment variables
        k = self.rand_str().upper()
        v = self.rand_str()
        assert ampho.get_config(k) is None
        os.environ[k] = v
        assert ampho.get_config(k) == v

    def test_get_config_int(self, tmp_path: str):
        """Test get_config_int()
        """
        k = self.rand_str().upper()
        v = self.rand_int()
        ampho = self.make_app(tmp_path, {k: v})

        assert ampho.get_config_int(k) == v

        ampho.app.config.from_mapping({k: self.rand_str()})
        with pytest.raises(ValueError):
            assert ampho.get_config_int(k)

    def test_get_config_bool(self, tmp_path: str):
        """Test get_config_bool()
        """
        k = self.rand_str().upper()
        ampho = self.make_app(tmp_path)

        for v in 1, True, '1', 'yes', 'true', 'Yes', 'True':
            ampho.app.config[k] = v
            assert ampho.get_config_bool(k) == True

        for v in 0, False, '0', 'no', 'false', 'No', 'False':
            ampho.app.config[k] = v
            assert ampho.get_config_bool(k) == False

    def test_get_config_json(self, tmp_path: str):
        """Test get_config_json()
        """
        k = self.rand_str().upper()
        c = {self.rand_str(): self.rand_str()}
        ampho = self.make_app(tmp_path, {k: json.dumps(c)})

        assert ampho.get_config_json(k) == c

    def test_load_config_dir(self, tmp_path):
        """Test load_config_dir()
        """
        ampho = self.make_app(tmp_path)
        os.makedirs(ampho.get_config('AMPHO_CONFIG_DIR'), 0o755, True)

        values = {}
        for config_name in ('default', os.getenv('FLASK_ENV', 'production'), f'{getuser()}@{gethostname()}'):
            for ext in ('.py', '.json'):
                k = (config_name + ext).upper().replace('.', '_').replace('@', '_').replace('-', '_')
                v = self.rand_str()
                values[k] = v
                with open(os.path.join(ampho.config_dir, config_name + ext), "w") as f:
                    if ext == '.json':
                        json.dump({k: v}, f)
                    else:
                        f.write(f'{k}="{v}"')

        ampho.load_config_dir()
        for k, v in values.items():
            assert ampho.get_config(k) == v
