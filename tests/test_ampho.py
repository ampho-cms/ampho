"""Ampho Tests
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import pytest
from os import PathLike, path
from flask import Flask
from flask_ampho import Ampho


@pytest.fixture
def instance_path(tmp_path: PathLike) -> str:
    return path.join(tmp_path, 'instance')


def test_ampho_init(instance_path: PathLike):
    app = Flask(__name__, instance_path=instance_path)
    app.config.from_mapping({
        'SQLALCHEMY_DATABASE_URI': 'sqlite://',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })
    Ampho(app)
