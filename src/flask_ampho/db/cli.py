"""Ampho CLI Commands
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import logging
import click
import flask_migrate
from typing import List, Dict, Union
from time import time
from os import path, listdir
from shutil import rmtree, copytree
from tempfile import mkdtemp
from werkzeug.local import LocalProxy
from flask import Flask, current_app
from flask_ampho import Ampho
from flask_ampho.util import package_path, is_dir_empty, secho_warning, secho_error
from . import signal

app = current_app  # type: Union[Flask, LocalProxy]
ampho = current_app.extensions['ampho']  # type: Ampho
root_path = ampho.root_path


def _get_migration_packages() -> Dict[str, str]:
    cfg: List[str] = app.config.get('AMPHO_MIGRATION_PACKAGES', [])
    if isinstance(cfg, str):
        cfg = list(filter(bool, map(lambda x: x.strip(), cfg.split(','))))

    signal.gmp.send(app._get_current_object(), packages=cfg)

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

    print('---', v_dir, listdir(v_dir), branch)

    flask_migrate.revision(m_dir, message, False, None, head, branch_label=branch, rev_id=f'{package}_{int(time())}')


@ampho.cli.command()
@click.option('-s/-S', '--sql/--no-sql', default=False)
@click.argument('rev', default='heads')
def db_up(rev: str, sql: bool):
    """Upgrade database schema
    """
    m_dir = _make_migrations_struct()
    flask_migrate.upgrade(m_dir, rev, sql)
    rmtree(m_dir)


@ampho.cli.command()
@click.option('-s/-S', '--sql/--no-sql', default=False)
@click.argument('rev', default='-1')
def db_down(rev: str, sql: bool):
    """Downgrade database schema
    """
    m_dir = _make_migrations_struct()
    flask_migrate.downgrade(m_dir, rev, sql)
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
@click.argument('rev', default="heads")
def db_show(rev: str = None):
    """Show the revision denoted by the given symbol
    """
    m_dir = _make_migrations_struct()
    flask_migrate.show(m_dir, rev)
    rmtree(m_dir)
