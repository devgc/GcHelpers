#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

try:
    from setuptools import find_packages, setup, Command
except ImportError:
    from distutils.core import find_packages, setup, Command

setup(
    name='GcHelpers',
    version='0.0.1',
    description='Collection of GC Helpers',
    author='devgc',
    url='https://github.com/devgc/GcHelpers',
    license="Apache Software License v2",
    package_dir={
        'helpers': 'helpers'
    },
    scripts=[
        u'scripts/SQLiteQuery.py'
    ],
    classifiers=[
        'Programming Language :: Python',
    ],
)