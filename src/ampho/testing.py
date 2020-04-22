"""Ampho Base Test Case
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import importlib
import string
import random
import sys
import os
import json
from typing import List
from pathlib import Path
from ._application import Application


class AmphoApplicationTestCase:
    """Base Ampho application test case
    """

    @staticmethod
    def _create_package(pkg_dir_path, content: str = ''):
        """Create a Python package
        """
        os.mkdir(pkg_dir_path)
        with open(os.path.join(pkg_dir_path, '__init__.py'), 'wt') as f:
            f.write(content)

    @staticmethod
    def rand_int(a: int = 0, b: int = sys.maxsize):
        """Generate a random integer
        """
        return random.randint(a, b)

    @staticmethod
    def rand_str(n_chars: int = 8) -> str:
        """Generate a random string
        """
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(n_chars))

    def rand_bundle(self, tmp_path: Path, requires: List[str] = None, name: str = None,
                    on_register: str = '    pass', on_load: str = '    pass',
                    append_init: str = '', append_views: str = '', append_commands: str = '') -> str:
        """Create a random bundle
        """
        # Add tmp_path to search path to allow import modules from there
        if str(tmp_path) not in sys.path:
            sys.path.append(str(tmp_path))

        name = name or self.rand_str()
        pkg_path = os.path.join(tmp_path, name)
        requires_str = ', '.join([f'"{b_name}"' for b_name in requires or []])

        self._create_package(pkg_path, (
            f'REQUIRES = [{requires_str}]\n\n'
            'def on_register():\n'
            f'{on_register}\n\n'
            'def on_load():\n'
            f'{on_load}\n\n'
            f'{append_init}\n'
        ))

        # Create views module
        view_name = self.rand_str()
        with open(os.path.join(pkg_path, 'views.py'), 'wt') as f:
            f.write(
                'from ampho import route, render\n\n'
                '@route("/<route_arg>")\n'
                f'def {view_name}(route_arg):\n'
                f'    return render("{name}.jinja2", some_variable=route_arg)\n\n'
                f'{append_views}\n'
            )

        # Create commands module
        command_name = self.rand_str()
        with open(os.path.join(pkg_path, 'commands.py'), 'wt') as f:
            f.write(
                'from ampho import cli\n\n'
                f'CLI_GROUP = "{name}"\n'
                f'CLI_HELP = "{command_name}"\n\n'
                '@cli.command("/<name>")\n'
                f'def {command_name}(name):\n'
                '    print(name)\n\n'
                f'{append_commands}\n'
            )

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
        with open(os.path.join(tpl_d_path, name + '.jinja2'), 'wt') as f:
            f.write('{{some_variable}}')

        # Invalidate import caches to guarantee on-the-fly created bundle be loaded
        importlib.invalidate_caches()

        return name

    def rand_app(self, tmp_path: Path, requires: List[str] = None, config: dict = None, entry_bundle_name: str = None):
        """Create a random Ampho application
        """
        # Create application bundle
        if entry_bundle_name is None:
            entry_bundle_name = self.rand_str()
            self.rand_bundle(tmp_path, requires, entry_bundle_name)

        # Set entry bundle name
        os.environ['AMPHO_ENTRY'] = entry_bundle_name

        # Create instance dir
        instance_dir = os.path.join(tmp_path, 'instance')
        os.mkdir(instance_dir)

        # Create configuration
        config_path = os.path.join(instance_dir, os.getenv('FLASK_ENV', 'production')) + '.json'
        config_content = config or {}  # type: dict
        config_content.update({
            'TESTING': True,
            self.rand_str().upper(): self.rand_str(),
        })
        with open(config_path, 'wt') as f:
            json.dump(config_content, f)

        # Create application instance
        return Application()
