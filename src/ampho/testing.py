"""Ampho Base Test Cases
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import string
import random
import sys
import os
import json
from typing import List
from ._application import Application


class AmphoApplicationTestCase:
    @staticmethod
    def _create_package(pkg_dir_path, content: str = ''):
        """Create a Python package
        """
        os.mkdir(pkg_dir_path)
        with open(os.path.join(pkg_dir_path, '__init__.py'), 'wt') as f:
            f.write(content)

    @staticmethod
    def rand_str(n_chars: int = 8) -> str:
        """Generate a random string
        """
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(n_chars))

    def rand_bundle(self, tmp_path: str, requires: List[str] = None, name: str = None, append_content: str = '',
                    append_views_content: str = '', append_commands_content: str = '') -> str:
        """Create a random bundle
        """
        # Add tmp_path to search path to allow import modules from there
        if tmp_path not in sys.path:
            sys.path.append(str(tmp_path))

        name = name or self.rand_str()
        pkg_path = os.path.join(tmp_path, name)
        requires_str = ', '.join([f'"{b_name}"' for b_name in requires or []])

        self._create_package(pkg_path, (
            f'BUNDLE_REQUIRES = [{requires_str}]\n'
            'def on_register():\n'
            '    pass\n'
            'def on_load():\n'
            '    pass\n'
            f'{append_content}\n'
        ))

        # Create views module
        view_name = self.rand_str()
        with open(os.path.join(pkg_path, 'views.py'), 'wt') as f:
            f.write(
                'from ampho import route, render\n'
                '@route("/<route_arg>")\n'
                f'def {view_name}(route_arg):\n'
                f'    return render("{name}", some_variable=route_arg)\n'
                f'{append_views_content}\n'
            )

        # Create commands module
        command_name = self.rand_str()
        with open(os.path.join(pkg_path, 'commands.py'), 'wt') as f:
            f.write(
                'from ampho import cli\n'
                f'CLI_GROUP = "{name}"\n'
                f'CLI_HELP="{command_name}"\n'
                '@cli.command("/<name>")\n'
                f'def {command_name}(name):\n'
                '    print(name)\n'
                f'{append_commands_content}\n'
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
        with open(os.path.join(tpl_d_path, name), 'wt') as f:
            f.write('{{some_variable}}')

        return name

    def rand_app(self, tmp_path: str, requirements: List[str] = None):
        """Create an Ampho application
        """
        # Create instance dir
        instance_dir = os.path.join(tmp_path, 'instance')
        os.mkdir(instance_dir)

        # Create configuration
        config_path = os.path.join(instance_dir, os.getenv('FLASK_ENV', 'production')) + '.json'
        config = {self.rand_str().upper(): self.rand_str().upper()}
        with open(config_path, 'wt') as f:
            json.dump(config, f)

        # Create application instance
        app = Application(requirements, root_path=tmp_path)
        app.testing = True

        return app
