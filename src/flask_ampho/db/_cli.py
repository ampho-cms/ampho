"""Ampho CLI Commands
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import click
import flask_migrate
from time import time
from os import path
from shutil import rmtree
from flask import current_app
from flask_ampho import Ampho
from flask_ampho.util import package_path, is_dir_empty, secho_error

ampho = current_app.extensions['ampho']  # type: Ampho


@ampho.cli.command()
@click.argument('package')
def db_init(package: str):
    """Initialize a migration environment
    """
    flask_migrate.init(package_path(package, 'migrations'))


@ampho.cli.command()
@click.argument('package')
@click.argument('message')
@click.option('-h', '--head', default='head')
def db_rev(package: str, message: str, head: str):
    """Create a database schema revision
    """
    m_dir = package_path(package, 'migrations')
    if not path.isdir(m_dir):
        secho_error(f"Directory not found: {m_dir}.\nTry the 'ampho db-init {package}' command")
        return

    v_dir = package_path(package, ['migrations', 'versions'])
    branch = package if is_dir_empty(v_dir) else None
    flask_migrate.revision(m_dir, message, False, None, head, branch_label=branch, rev_id=f'{package}_{int(time())}')


@ampho.cli.command()
@click.option('-s/-S', '--sql/--no-sql', default=False)
@click.argument('rev', default='heads')
def db_up(rev: str, sql: bool):
    """Upgrade database schema
    """
    m_dir = ampho.db.make_migrations_struct()
    flask_migrate.upgrade(m_dir, rev, sql)
    rmtree(m_dir)


@ampho.cli.command()
@click.option('-s/-S', '--sql/--no-sql', default=False)
@click.argument('rev', default='-1')
def db_down(rev: str, sql: bool):
    """Downgrade database schema
    """
    m_dir = ampho.db.make_migrations_struct()
    flask_migrate.downgrade(m_dir, rev, sql)
    rmtree(m_dir)


@ampho.cli.command()
@click.option('-v/-V', '--verbose/--no-verbose', default=False)
def db_current(verbose: bool):
    """Show current revision
    """
    m_dir = ampho.db.make_migrations_struct()
    flask_migrate.current(m_dir, verbose)
    rmtree(m_dir)


@ampho.cli.command()
@click.argument('rev', default="heads")
def db_show(rev: str = None):
    """Show the revision denoted by the given symbol
    """
    m_dir = ampho.db.make_migrations_struct()
    flask_migrate.show(m_dir, rev)
    rmtree(m_dir)
