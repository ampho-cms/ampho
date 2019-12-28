#!/bin/env python
"""Ampho setup.py
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import io
import re
from setuptools import find_packages
from setuptools import setup

PKG_NAME = 'ampho'
GITHUB_USER = 'ampho-cms'

with io.open('README.rst', 'rt') as f:
    readme = f.read()

with io.open(f'src/{PKG_NAME}/__init__.py', 'rt') as f:
    content = f.read()
    description = re.search(r"__description__ = '(.*?)'", content).group(1)
    author = re.search(r"__author__ = '(.*?)'", content).group(1)
    author_email = re.search(r"__email__ = '(.*?)'", content).group(1)
    lic = re.search(r"__license__ = '(.*?)'", content).group(1)
    version = re.search(r"__version__ = '(.*?)'", content).group(1)

setup(
    name=PKG_NAME,
    version=version,
    url=f'https://github.com/{GITHUB_USER}/{PKG_NAME}',
    project_urls={
        'Code': f'https://github.com/{GITHUB_USER}/{PKG_NAME}',
        'Documentation': f'https://{PKG_NAME}.readthedocs.io',
        'Issue tracker': f'https://github.com/{GITHUB_USER}/{PKG_NAME}/issues',
    },
    license=lic,
    author=author,
    author_email=author_email,
    maintainer=author,
    maintainer_email=author_email,
    description=description,
    long_description=readme,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'flask==1.*',
        'htmlmin==0.*',
        'babel==2.*',
        'blinker==1.*',
    ],
    entry_points={
        'console_scripts': [
            'ampho = ampho._cli:main'
        ]
    },
)
