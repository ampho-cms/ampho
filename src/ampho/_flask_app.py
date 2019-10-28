"""Ampho Application Instance
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from os import environ
from ampho import Application

app = Application([b for b in environ.get('AMPHO_BUNDLES', 'app').split(',') if b])  # pragma: no cover
