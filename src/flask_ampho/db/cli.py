"""Ampho CLI Commands
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import logging
import click
import flask_migrate
from typing import List, Dict
from time import time
from os import path
from shutil import rmtree, copytree
from tempfile import mkdtemp
from flask import Flask, current_app
from flask_ampho import Ampho
from flask_ampho.util import package_path, secho_warning, secho_error

app = current_app  # type: Flask
ampho = app.extensions['ampho']  # type: Ampho
root_path = ampho.root_path


def _get_migration_packages() -> Dict[str, str]:
    cfg: List[str] = app.config.get('AMPHO_MIGRATION_PACKAGES', [])
    if isinstance(cfg, str):
        cfg = list(filter(bool, map(lambda x: x.strip(), cfg.split(','))))

    cfg.extend(['flask_ampho.auth'])

    r = {}
    for pkg_name in cfg:
        subdir = 'migrations'
        if ':' in pkg_name:
            pkg_name, subdir = pkg_name.split()

        r[pkg_name] = package_path(pkg_name, subdir)

    return r


def _make_migrations_struct() -> str:
    ignore = ['__pycache__']
    tmp_path = mkdtemp(prefix='ampho-migrate-')

    # Prepare Alembic's structure skeleton
    copytree(package_path(__package__.split('.')[0], ['db', 'alembic_skel']), tmp_path, dirs_exist_ok=True)

    # Copy versions from each registered package
    cnt = 0
    dst = path.join(tmp_path, 'versions')
    for pkg_name, dir_path in _get_migration_packages().items():
        src = path.join(dir_path, 'versions')
        if not path.isdir(src):
            secho_warning(f'Not found: {src}')
            continue

        copytree(src, dst, ignore=lambda a, b: ignore, dirs_exist_ok=True)
        cnt += 1
        logging.debug(f'Copied: {src}')

    return tmp_path


@ampho.cli.command()
@click.option('-r', '--rev', default='heads')
@click.option('-s/-S', '--sql/--no-sql', default=False)
def db_up(rev: str, sql: bool):
    """Upgrade database schema
    """
    m_dir = _make_migrations_struct()
    flask_migrate.upgrade(m_dir, rev, sql)
    rmtree(m_dir)


@ampho.cli.command()
@click.option('-r', '--rev', default='-1')
@click.option('-s/-S', '--sql/--no-sql', default=False)
def db_down(rev: str, sql: bool):
    """Downgrade database schema
    """
    m_dir = _make_migrations_struct()
    flask_migrate.downgrade(m_dir, rev, sql)
    rmtree(m_dir)


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
@click.option('-s/-S', '--sql/--no-sql', default=False)
def db_rev(package: str, message: str, head: str, sql: bool):
    """Create a database schema revision
    """
    m_dir = package_path(package, 'migrations')
    if not path.isdir(m_dir):
        secho_error(f"Directory not found: {m_dir}.\nTry the 'ampho db-init {package}' command")
        return

    flask_migrate.revision(m_dir, message, False, sql, head, rev_id=f'{package}_{int(time())}')


@ampho.cli.command()
@click.option('-v/-V', '--verbose/--no-verbose', default=False)
def db_heads(verbose: bool):
    """Show current available heads
    """
    m_dir = _make_migrations_struct()
    flask_migrate.heads(m_dir, verbose)
    rmtree(m_dir)


@ampho.cli.command()
@click.option('-v/-V', '--verbose/--no-verbose', default=False)
def db_current(verbose: bool):
    """Show current revision
    """
    m_dir = _make_migrations_struct()
    flask_migrate.current(m_dir, verbose)
    rmtree(m_dir)


@ampho.cli.command()
@click.option('-r', '--rev', default='heads')
def db_show(rev: bool):
    """Show the revision denoted by the given symbol
    """
    m_dir = _make_migrations_struct()
    flask_migrate.show(m_dir, rev)
    rmtree(m_dir)
