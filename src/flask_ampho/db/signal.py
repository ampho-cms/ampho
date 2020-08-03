"""Ampho DB Signals
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from flask import current_app
from flask_ampho import Ampho

_ampho = current_app.extensions['ampho']  # type: Ampho

gmp = _ampho.signals.signal('get-migration-packages')
