"""Ampho Locale Bundle Commands
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import click
from os import path, makedirs
from flask import g, current_app
from babel.messages.frontend import CommandLineInterface as BabelCLI
from ampho import Bundle

_bundle = g.bundle  # type: Bundle

def _get_babel_cli() -> BabelCLI:
    return BabelCLI()


def _get_bundle(bundle_name: str) -> Bundle:
    """Get a bundle by name
    """
    return current_app.get_bundle(bundle_name)


def _get_bundle_lang_dir(bundle_name: str, ensure: bool = False):
    """Get bundle's translations catalogs dir
    """
    dir_path = path.join(_get_bundle(bundle_name).root_dir, 'locale')

    if ensure and not path.isdir(dir_path):
        makedirs(dir_path, 0o755)

    return dir_path


@g.bundle.command('extract')
@click.argument('bundle')
def extract(bundle: str):
    """Extract messages to a POT file
    """
    mappings_f_path = path.join(_bundle.root_dir, 'res', 'babel.ini')
    inp_d_path = _get_bundle(bundle).root_dir
    out_f_path = path.join(_get_bundle_lang_dir(bundle), f'{bundle}.pot')
    _get_babel_cli().run(['babel', 'extract', '--no-location', '--omit-header', '--sort-output',
                          '-F', mappings_f_path, '-o', out_f_path, inp_d_path])


@g.bundle.command('init')
@click.argument('bundle')
@click.argument('locale')
def init(bundle: str, locale: str):
    """Init a new PO file
    """
    out_d_path = _get_bundle_lang_dir(bundle)
    inp_f_path = path.join(out_d_path, f'{bundle}.pot')
    _get_babel_cli().run(['babel', 'init', '-D', bundle, '-l', locale, '-i', inp_f_path, '-d', out_d_path])


@g.bundle.command('update')
@click.argument('bundle')
@click.argument('locale')
def update(bundle: str, locale: str):
    """Update an existing PO file
    """
    out_d_path = _get_bundle_lang_dir(bundle)
    inp_f_path = path.join(out_d_path, f'{bundle}.pot')
    _get_babel_cli().run(['babel', 'update', '-D', bundle, '-l', locale, '-i', inp_f_path, '-d', out_d_path])


@g.bundle.command('compile')
@click.argument('bundle')
def compile(bundle):
    """Compile translations
    """
    _get_babel_cli().run(['babel', 'compile', '-D', bundle, '-d', _get_bundle_lang_dir(bundle)])
