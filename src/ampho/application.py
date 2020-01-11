"""Ampho CLI Main Module
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from os import environ
from flask.cli import FlaskGroup
from ampho import Application

application = Application([b for b in environ.get('AMPHO_BUNDLES', 'app').split(',') if b])  # pragma: no cover


def main():
    environ['FLASK_APP'] = 'ampho.application'
    FlaskGroup().main(prog_name='ampho')
