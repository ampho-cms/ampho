"""Ampho CLI
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from os import environ
from flask.cli import cli


def main():
    environ['FLASK_APP'] = 'ampho._flask_app:app'
    cli.help = ''
    cli.main(prog_name='ampho')
