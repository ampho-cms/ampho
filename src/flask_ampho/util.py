"""Ampho Helpers
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import pkgutil
import logging
from typing import Union, List
from os import path
from click import secho


def package_path(pkg_name: str, subdir: Union[str, List[str]]):
    pkg_info = pkgutil.get_loader(pkg_name)
    if not pkg_info:
        raise ModuleNotFoundError(f"Package {pkg_name} is not found")

    if isinstance(subdir, str):
        subdir = [subdir]

    return path.join(path.dirname(pkg_info.path), *subdir)


def secho_info(msg: str, *args, **kwargs):
    """Shortcut for printing info messages
    """
    kwargs['fg'] = 'blue'
    secho(msg, *args, **kwargs)
    logging.info(msg)


def secho_success(msg: str, *args, **kwargs):
    """Shortcut for printing success messages
    """
    kwargs['fg'] = 'green'
    secho(msg, *args, **kwargs)
    logging.info(msg)


def secho_warning(msg: str, *args, **kwargs):
    """Shortcut for printing warning messages
    """
    kwargs['fg'] = 'yellow'
    secho(msg, *args, **kwargs)
    logging.warning(msg)


def secho_error(msg: str, *args, **kwargs):
    """Shortcut for printing error messages
    """
    kwargs['fg'] = 'red'
    secho(msg, None, True, True, *args, **kwargs)
    logging.error(msg)
