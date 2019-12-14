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
from ampho import Application, Bundle
from typing import Callable


@pytest.fixture
def rand_str() -> Callable[[], str]:
    """Generates random string
    """

    def f(n_chars: int = 8) -> str:
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(n_chars))

    return f


def create_package(pkg_dir_path, content: str = ''):
    """Creates a Python package
    """
    os.mkdir(pkg_dir_path)
    with open(os.path.join(pkg_dir_path, '__init__.py'), 'wt') as f:
        f.write(content)


@pytest.fixture
def rand_bundle(tmp_path: str, rand_str: Callable[[], str]) -> Callable:
    # Add tmp_path to search path to allow import modules from there
    if tmp_path not in sys.path:
        sys.path.append(str(tmp_path))

    def f() -> Bundle:
        pkg_name = rand_str()
        bundle_name = rand_str()
        pkg_path = os.path.join(tmp_path, pkg_name)

        create_package(pkg_path, (
            f'BUNDLE_NAME = "{bundle_name}"\n'
            'def init(bundle):\n'
            '    pass'
        ))

        # Create view module
        view_name = rand_str()
        with open(os.path.join(pkg_path, 'views.py'), 'wt') as f:
            f.write(
                'from ampho.bundle_ctx import route\n'
                '@route("/<name>")\n'
                f'def {view_name}(name):\n'
                '    return name\n'
            )

        # Create commands module
        command_name = rand_str()
        with open(os.path.join(pkg_path, 'commands.py'), 'wt') as f:
            f.write(
                'from ampho.bundle_ctx import command, gettext as _\n'
                f'CLI_HELP="{command_name}"\n'
                '@command("/<name>")\n'
                f'def {command_name}(name):\n'
                '    return _("Hello %s") % name\n'
            )

        # Create locale directory
        locale_d_path = os.path.join(pkg_path, 'locale')
        os.makedirs(locale_d_path, 0o750)

        # Create templates directory
        tpl_d_path = os.path.join(pkg_path, 'tpl')
        os.makedirs(tpl_d_path, 0o750)

        # Create static directory
        static_d_path = os.path.join(pkg_path, 'static')
        os.makedirs(static_d_path, 0o750)

        # Create resources directory
        res_d_path = os.path.join(pkg_path, 'res')
        os.makedirs(res_d_path, 0o750)

        # Create template
        with open(os.path.join(tpl_d_path, bundle_name), 'wt') as f:
            f.write(bundle_name)

        return Bundle(pkg_name)

    return f


@pytest.fixture
def app(tmp_path: str, rand_bundle: Callable[[], Bundle], rand_str: Callable[[], str]):
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
    app = Application([f'{app_bundle.module_name}'], root_path=tmp_path)
    app.testing = True

    # Check if the config was loaded
    assert app.config.get(list(config.keys())[0]) == list(config.values())[0]

    return app
