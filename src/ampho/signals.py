"""Ampho signals
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from blinker import Namespace

_signals = Namespace()

bundle_registered = _signals.signal('bundle-registered')
