"""Ampho Auth
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from flask import Flask, current_app
from . import rest

app = current_app  # type: Flask
