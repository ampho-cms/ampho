"""Ampho conftest.py
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import pytest
import sys
import os
import string
import random
import json
import ampho
from typing import Tuple, Callable


def rand_str() -> str:
    """Generates random string
    """
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(8))


def create_package(pkg_dir_path, content: str = ''):
    """Creates a Python package
    """
    os.mkdir(pkg_dir_path)
    with open(os.path.join(pkg_dir_path, '__init__.py'), 'wt') as f:
        f.write(content)


@pytest.fixture
def random_bundle(tmp_path: str) -> Callable:
    def f() -> Tuple[str, str]:
        pkg_name = rand_str()
        view_name = rand_str()

        pkg_path = os.path.join(tmp_path, pkg_name)
        create_package(pkg_path, (
            'def init_bundle(bundle):\n'
            '    pass'
        ))

        # Create bundle view module and function
        with open(os.path.join(pkg_path, 'view.py'), 'wt') as f:
            f.write(
                'from flask import g\n\n'
                '@g.bundle.route("/<name>")\n'
                f'def {view_name}(name):\n'
                '    return name\n'
            )

        return pkg_name, view_name

    return f


@pytest.fixture()
def app(tmp_path: str, random_bundle: Callable):
    """Application fixture
    """
    # Add tmp_path to search path
    sys.path.append(str(tmp_path))

    # Create app's bundle
    app_pkg_name, app_view_name = random_bundle()

    # Create instance dir
    instance_dir = os.path.join(tmp_path, 'instance')
    os.mkdir(instance_dir)

    # Create configuration
    config_path = os.path.join(instance_dir, os.getenv('FLASK_ENV', 'production')) + '.json'
    config = {rand_str().upper(): rand_str().upper()}
    with open(config_path, 'wt') as f:
        json.dump(config, f)

    # Create application instance
    app = ampho.Application([f'{app_pkg_name}'], root_path=tmp_path)


    # Check if the config was loaded
    assert app.config.get(list(config.keys())[0]) == list(config.values())[0]

    return app
