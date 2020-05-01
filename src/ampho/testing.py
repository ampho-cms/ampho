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
from typing import Optional, List
from tempfile import mkdtemp
from shutil import rmtree
from ._application import Application
from ._bundle import Bundle


class AmphoApplicationTestCase:
    """Base Ampho application test case
    """
    # Path to test case temporary directory
    tmp_dir: Optional[str] = None

    # Test case application
    app: Optional[Application] = None

    # Test case entry bundle
    entry_bundle: Optional[Bundle] = None

    # Entry bundle requirements
    ENTRY_BUNDLE_REQUIRES: List[str] = []

    # Should created temporary directories be removed at teardown
    RM_TMP_DIRS: bool = True

    # Created temporary directories during a testing session
    _TMP_DIRS: List[str] = []

    @classmethod
    def setup_class(cls):
        """Class setup fixture
        """
        cls.tmp_dir = cls.make_tmp_dir()

        entry_bundle_name = cls.rand_bundle_struct(cls.tmp_dir, cls.ENTRY_BUNDLE_REQUIRES)
        os.environ['AMPHO_ENTRY'] = entry_bundle_name

        cls.app = cls.rand_app()
        cls.entry_bundle = cls.app.get_bundle(entry_bundle_name)
        cls.cli_runner = cls.app.test_cli_runner()

    @classmethod
    def teardown_class(cls):
        """Class teardown fixture
        """
        if cls.RM_TMP_DIRS:
            for D in cls._TMP_DIRS:
                rmtree(D, True)

    @staticmethod
    def _create_package(dir_path, content: str = ''):
        """Create a Python package
        """
        os.mkdir(dir_path)
        with open(os.path.join(dir_path, '__init__.py'), 'wt') as f:
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

    @classmethod
    def make_tmp_dir(cls) -> str:
        """Yes, I know about tmp_path fixture existence.
        This method is aimed to be used in class setup/teardown methods.
        """
        d_path = mkdtemp(prefix='ampho-test-')
        cls._TMP_DIRS.append(d_path)

        return d_path

    @classmethod
    def rand_bundle_struct(cls, tmp_dir: str = None, requires: List[str] = None, name: str = None,
                           on_register: str = '    pass', on_load: str = '    pass',
                           append_init: str = '', append_views: str = '', append_commands: str = '') -> str:
        """Create a random bundle structure
        """
        if not tmp_dir:
            tmp_dir = cls.tmp_dir

        # Add tmp_dir to search path to allow import modules from there
        if str(tmp_dir) not in sys.path:
            sys.path.append(str(tmp_dir))

        name = name or cls.rand_str()
        pkg_path = os.path.join(tmp_dir, name)  # type: ignore
        requires_str = ', '.join([f'"{b_name}"' for b_name in requires or []])

        cls._create_package(pkg_path, (
            f'REQUIRES = [{requires_str}]\n\n'
            'def on_register():\n'
            f'{on_register}\n\n'
            'def on_load():\n'
            f'{on_load}\n\n'
            f'{append_init}\n'
        ))

        # Create views module
        view_name = cls.rand_str()
        with open(os.path.join(pkg_path, 'views.py'), 'wt') as f:
            f.write(
                'from ampho import route, render\n\n'
                '@route("/<route_arg>")\n'
                f'def {view_name}(route_arg):\n'
                f'    return render("{name}.jinja2", some_variable=route_arg)\n\n'
                f'{append_views}\n'
            )

        # Create commands module
        command_name = cls.rand_str()
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

    @classmethod
    def rand_app(cls, config: dict = None, tmp_dir: str = None, **kwargs):
        """Create a random Ampho application
        """
        # Ensure path to tmp dir
        if not tmp_dir:
            tmp_dir = cls.tmp_dir

        # Create instance dir
        instance_dir = os.path.join(tmp_dir, 'instance')  # type: ignore
        os.mkdir(instance_dir)

        # Create configuration
        config_path = os.path.join(instance_dir, os.getenv('FLASK_ENV', 'production')) + '.json'
        config_content = config or {}
        config_content.update({
            'TESTING': True,
        })
        with open(config_path, 'wt') as f:
            json.dump(config_content, f)

        # Create application instance
        return Application(**kwargs)
