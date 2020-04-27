"""Ampho API Functions
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import inspect as _inspect
from typing import Dict
from os import path
from flask import Request, current_app as _c_app, request as _req, g as _g
from ._application import Application
from ._bundle import Bundle

# Following variables are used just for type hinting purposes
current_app: Application = _c_app  # type: ignore
request: Request = _req

# Cache for get_caller_bundle()
_FILE2BUNDLE: Dict[str, Bundle] = {}


def get_caller_bundle(skip_frames: int = 1) -> Bundle:
    """Helper function for caller bundle detection
    """
    # Try to find current bundle
    if 'current_bundle' in _g:
        return _g.current_bundle

    # Try to detect bundle by inspecting source code
    for of in _inspect.getouterframes(_inspect.currentframe())[skip_frames:]:
        filename = path.abspath(of.filename)

        if filename in _FILE2BUNDLE:  # pragma: no cover
            return _FILE2BUNDLE[filename]

        cur_path = path.split(filename)[0].split(path.sep)
        while len(cur_path) > 1:
            bundle = current_app.bundles_by_path.get(path.sep.join(cur_path))
            if bundle:
                _FILE2BUNDLE[filename] = bundle
                return bundle

            cur_path = cur_path[:-1]

    raise RuntimeError('There is no bundle context set')  # pragma: no cover


def route(rule: str, **options):
    """Decorator for routes definition
    """
    return get_caller_bundle().route(rule, **options)


def render(tpl: str, **args) -> str:
    """Render a template
    """
    return get_caller_bundle().render(tpl, **args)
