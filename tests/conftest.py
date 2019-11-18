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
from typing import Callable


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
def rand_bundle(tmp_path: str) -> Callable:
    # Add tmp_path to search path to allow import modules from there
    if tmp_path not in sys.path:
        sys.path.append(str(tmp_path))

    def f() -> ampho.Bundle:
        pkg_name = rand_str()
        pkg_path = os.path.join(tmp_path, pkg_name)

        create_package(pkg_path, (
            'def init(bundle):\n'
            '    pass'
        ))

        # Create view module
        view_name = rand_str()
        with open(os.path.join(pkg_path, 'views.py'), 'wt') as f:
            f.write(
                'from ampho import g\n'
                'bundle = g.bundle\n'
                '@bundle.route("/<name>")\n'
                f'def {view_name}(name):\n'
                '    return name\n'
            )

        # Create commands module
        command_name = rand_str()
        with open(os.path.join(pkg_path, 'commands.py'), 'wt') as f:
            f.write(
                'from ampho import g\n'
                'bundle = g.bundle\n'
                '@bundle.command("/<name>")\n'
                f'def {command_name}(name):\n'
                '    return name\n'
            )

        # Create static directory
        static_d_path = os.path.join(pkg_path, 'static')
        os.makedirs(static_d_path, 0o750)

        return ampho.Bundle(pkg_name)

    return f


@pytest.fixture
def app(tmp_path: str, rand_bundle):
    """Application fixture
    """
    # Create app's bundle
    app_bundle = rand_bundle()

    # Create instance dir
    instance_dir = os.path.join(tmp_path, 'instance')
    os.mkdir(instance_dir)

    # Create configuration
    config_path = os.path.join(instance_dir, os.getenv('FLASK_ENV', 'production')) + '.json'
    config = {rand_str().upper(): rand_str().upper()}
    with open(config_path, 'wt') as f:
        json.dump(config, f)

    # Create application instance
    app = ampho.Application([f'{app_bundle.name}'], root_path=tmp_path)

    # Check if the config was loaded
    assert app.config.get(list(config.keys())[0]) == list(config.values())[0]

    return app
