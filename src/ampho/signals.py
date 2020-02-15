"""Ampho Signals
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from blinker import Namespace

_signals = Namespace()

# Fires after a new bundle registered
bundle_registered = _signals.signal('bundle-registered')
