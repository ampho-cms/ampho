"""
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import sys
import random
import string
from typing import Union
from os import path, PathLike
from flask import Flask
from flask_ampho import Ampho
from jwcrypto.jwk import JWK


class AmphoTestCase:
    @staticmethod
    def make_app(tmp_path: Union[PathLike, str], config: dict = None) -> Ampho:
        """Test __init__()
        """
        if config is None:
            config = {}

        config.setdefault('SQLALCHEMY_DATABASE_URI', 'sqlite://')
        config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
        config.setdefault('AMPHO_LOG_DIR', path.join(tmp_path, 'log'))
        config.setdefault('AMPHO_CONFIG_DIR', path.join(tmp_path, 'config'))
        config.setdefault('AMPHO_SECURITY_KEY', JWK.generate(kty="oct", size=256).export())

        app = Flask(__name__, instance_path=path.join(tmp_path, 'instance'))
        app.config.from_mapping(config)

        return Ampho(app)

    @staticmethod
    def rand_int(a: int = 0, b: int = sys.maxsize):
        """Generate a random integer
        """
        return random.randint(a, b)

    @staticmethod
    def rand_str(n_chars: int = 8) -> str:
        """Generate a random string
        """
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(n_chars))
