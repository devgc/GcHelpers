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
    author='devgc',
    url='https://github.com/devgc/GcHelpers',
    license="Apache Software License v2",
    zip_safe=False,
    install_requires=[
        'geoip2',
    ],
    packages=find_packages(
        '.',
    ),
    package_dir={
        'gchelpers': 'gchelpers',
        'geodb': 'geodb'
    },
    data_files = [
        ('geodb',[u'geodb/GeoLite2-City.mmdb'])
    ],
    scripts=[
        u'scripts/SQLiteQuery.py'
    ],
    classifiers=[
        'Programming Language :: Python',
    ]
)