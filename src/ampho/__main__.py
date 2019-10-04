"""
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from os import environ

if __name__ == '__main__':
    from flask.cli import cli

    environ['FLASK_APP'] = 'ampho.app:app'

    cli.help = ''
    cli.main(prog_name='ampho')
