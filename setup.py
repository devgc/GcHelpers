#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

try:
    from setuptools import find_packages, setup
except ImportError:
    from distutils.core import find_packages, setup

setup(
    name='gchelpers',
    version='0.0.1',
    description='Collection of GC Helpers',
    author = 'G-C Partners, LLC',
    author_email = 'dev@g-cpartners.com',
    url='https://github.com/devgc/GcHelpers',
    download_url = 'https://github.com/devgc/GcHelpers/tarball/0.0.1',
    license="Apache Software License v2",
    zip_safe=False,
    install_requires=[
        'geoip2',
        'pyyaml',
        'python-dateutil'
    ],
    packages=find_packages(
        '.',
    ),
    package_dir={
        'gchelpers': 'gchelpers',
        'geodb': 'geodb'
    },
    scripts=[
        u'scripts/SQLiteQuery.py',
        u'scripts/SQLiteToXlsx.py',
        u'scripts/UpdateGeoIpDb.py'
    ],
    classifiers=[
        'Programming Language :: Python',
    ]
)