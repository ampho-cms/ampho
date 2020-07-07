"""Ampho CLI Commands
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from os import getenv
from flask import Flask, current_app
from flask.cli import AppGroup
from flask_migrate import upgrade as fm_upgrade, revision as fm_revision

app = current_app  # type: Flask
ampho_cli = AppGroup('ampho')
app.cli.add_command(ampho_cli)


@ampho_cli.command()
def db_upgrade():
    fm_upgrade(app.extensions['ampho'].migrations_path)


if getenv('AMPHO_DEV') == '1':
    migrations_path = app.extensions['ampho'].migrations_path


    @ampho_cli.command()
    def db_revision():
        fm_revision(migrations_path)
