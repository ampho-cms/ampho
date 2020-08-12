"""
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import sys
import random
import string
import pytest
from os import path, PathLike
from flask import Flask
from flask_ampho import Ampho
from jwcrypto.jwk import JWK


def rand_int(a: int = 0, b: int = sys.maxsize):
    """Generate a random integer
    """
    return random.randint(a, b)


def rand_str(n_chars: int = 8) -> str:
    """Generate a random string
    """
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(n_chars))


@pytest.fixture(autouse=True)
def ampho(tmp_path: PathLike) -> Ampho:
    app = Flask(__name__, instance_path=path.join(tmp_path, 'instance'))
    app.config.from_mapping({
        'SQLALCHEMY_DATABASE_URI': 'sqlite://',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'AMPHO_LOG_DIR': path.join(tmp_path, 'log'),
        'AMPHO_CONFIG_DIR': path.join(tmp_path, 'config'),
        'AMPHO_SECURITY_KEY': JWK.generate(kty="oct", size=256).export(),
    })

    yield Ampho(app)
