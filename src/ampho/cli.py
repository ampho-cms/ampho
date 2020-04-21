"""Ampho CLI Helpers
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import click
from typing import Any
from ._api import get_caller_bundle


def command(*args, **kwargs):
    """Decorator for CLI commands definition
    """
    return get_caller_bundle().command(*args, **kwargs)


def echo(message: Any, fg: str = None, bg: str = None, err: bool = False):
    """Echo a message
    """
    if not isinstance(message, str):
        message = str(message)

    click.secho(message, fg=fg, bg=bg, err=err)


def echo_info(message: Any):
    """Echo an info message
    """
    echo(message, 'blue')


def echo_success(message: Any):
    """Echo a success message
    """
    echo(message, 'green')


def echo_warning(message: Any):
    """Echo a warning message
    """
    echo(message, 'yellow')


def echo_error(message: Any, do_exit: bool = False, exit_code: int = 1):
    """Echo an error message to stderr and optionally raise SystemExit
    """
    echo(message, 'red', err=True)

    if do_exit:
        raise SystemExit(exit_code)
