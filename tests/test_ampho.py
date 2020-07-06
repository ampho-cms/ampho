"""Ampho Tests
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import pytest
from os import PathLike, path
from flask import Flask
from ampho import ampho_init


@pytest.fixture
def instance_path(tmp_path: PathLike) -> str:
    return path.join(tmp_path, 'instance')


def test_ampho_init(instance_path: PathLike):
    ampho_init(Flask(__name__, instance_path=instance_path))
