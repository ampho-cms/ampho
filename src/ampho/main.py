"""Ampho CLI Main Module
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from os import environ
from flask.cli import FlaskGroup
from ampho import Application

APPLICATION = Application()  # pragma: no cover


def main():
    """Main
    """
    environ['FLASK_APP'] = 'ampho.main:APPLICATION'
    FlaskGroup().main(prog_name='ampho')
