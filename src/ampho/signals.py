"""Ampho Signals
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from blinker import Namespace  # type: ignore

_signals = Namespace()

# After a new bundle registered
bundle_registered = _signals.signal('bundle-registered')
