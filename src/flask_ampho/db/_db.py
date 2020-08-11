"""Ampho Database API
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import logging
from typing import Dict, List
from os import path
from shutil import copytree
from tempfile import mkdtemp
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_ampho import Ampho
from flask_ampho.util import package_path, secho_warning


class Db:
    """Ampho Database API
    """

    def __init__(self, ampho: Ampho, sqlalchemy: SQLAlchemy, migrate: Migrate):
        """Init
        """
        self.ampho = ampho
        self.sqlalchemy = sqlalchemy
        self.migrate = migrate

        self.on_get_migrations_packages = ampho.signals.signal('get-migration-packages')

        # Register CLI commands
        with ampho.app.app_context():
            from . import _cli

    def get_migration_packages(self) -> Dict[str, str]:
        cfg: List[str] = self.ampho.get_config('AMPHO_MIGRATION_PACKAGES', [])
        if isinstance(cfg, str):
            cfg = list(filter(bool, map(lambda x: x.strip(), cfg.split(','))))

        self.on_get_migrations_packages.send(self.ampho.app, packages=cfg)

        r = {}
        for pkg_name in cfg:
            subdir = 'migrations'
            if ':' in pkg_name:
                pkg_name, subdir = pkg_name.split()

            r[pkg_name] = package_path(pkg_name, subdir)

        return r

    def _make_migrations_struct(self) -> str:
        ignore = ['__pycache__']
        tmp_path = mkdtemp(prefix='ampho-migrate-')

        # Prepare Alembic's structure skeleton
        copytree(package_path(__package__.split('.')[0], ['db', 'alembic_skel']), tmp_path, dirs_exist_ok=True)

        # Copy versions from each registered package
        cnt = 0
        dst = path.join(tmp_path, 'versions')
        for pkg_name, dir_path in self.get_migration_packages().items():
            src = path.join(dir_path, 'versions')
            if not path.isdir(src):
                secho_warning(f'Not found: {src}')
                continue

            copytree(src, dst, ignore=lambda a, b: ignore, dirs_exist_ok=True)
            cnt += 1
            logging.debug(f'Copied: {src}')

        return tmp_path
