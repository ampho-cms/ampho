"""Ampho CLI Helpers
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import click
from typing import Any
from sys import exit
from ._api import get_caller_bundle


def command(*args, **kwargs):
    """Decorator for CLI commands definition
    """
    return get_caller_bundle().command(*args, **kwargs)


def echo(s: Any, fg: str = None, bg: str = None, err: bool = False):
    """Echo a message
    """
    if not isinstance(s, str):
        s = str(s)

    click.secho(s, fg=fg, bg=bg, err=err)


def echo_info(s: Any):
    """Echo an info message
    """
    echo(s, 'blue')


def echo_success(s: Any):
    """Echo a success message
    """
    echo(s, 'green')


def echo_warning(s: Any):
    """Echo a warning message
    """
    echo(s, 'yellow')


def echo_error(s: Any, do_exit: bool = False, exit_code: int = 1):
    """Echo an error message to stderr and optionally call sys.exit()
    """
    echo(s, 'red', err=True)

    if do_exit:
        exit(exit_code)
