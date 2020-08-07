"""Ampho Auth
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import List
from flask import Flask, current_app
from flask_ampho.db import signal

app = current_app  # type: Flask


@signal.gmp.connect_via(app)
def on_db_get_migration_packages(sender: Flask, packages: List[str]):
    packages.append('flask_ampho.auth')
