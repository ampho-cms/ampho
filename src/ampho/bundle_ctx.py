"""Current bundle context helpers
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from flask import g

if 'current_bundle' not in g:
    raise RuntimeError("It seems you've imported the 'bundle_ctx' module in a wrong way")  # pragma: no cover

bundle = g.current_bundle
route = g.current_bundle.route
command = g.current_bundle.command
render = g.current_bundle.render
gettext = g.current_bundle.gettext
_ = gettext
