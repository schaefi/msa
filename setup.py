#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from os import path
from setuptools import setup

from msa.version import __version__

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as readme:
    long_description = readme.read()

config = {
    'name': 'msa',
    'long_description': long_description,
    'long_description_content_type': 'text/x-rst',
    'description': 'MSA - Web Check',
    'author': 'Marcus Schaefer',
    'url': 'https://github.com/schaefi/msa',
    'author_email': 'marcus.schaefer@gmail.com',
    'version': __version__,
    'license' : 'GPLv3+',
    'install_requires': [
        'docopt',
        'psycopg2-binary',
        'kafka-python',
        'requests',
        'cerberus'
    ],
    'packages': ['msa'],
    'entry_points': {
        'console_scripts': [
            'msa-lookup=msa.msa_lookup:main',
            'msa-store=msa.msa_store:main',
            'msa-init=msa.msa_init:main'
        ]
    },
    'include_package_data': True,
    'zip_safe': False,
    'classifiers': [
       # classifier: http://pypi.python.org/pypi?%3Aaction=list_classifiers
       'Development Status :: 3 - Alpha',
       'Intended Audience :: Developers',
       'License :: OSI Approved :: '
       'GNU General Public License v3 or later (GPLv3+)',
       'Operating System :: POSIX :: Linux',
       'Programming Language :: Python :: 3.6',
       'Topic :: System :: Operating System',
    ]
}

setup(**config)
