#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

about = {}
with open(os.path.join(here, 'cli', "__version__.py")) as f:
    exec(f.read(), about)

required = []

setup(
    name='andy',
    version=about['__version__'],
    description='.',
    long_description=long_description,
    author='',
    author_email='x@x.com',
    url='https://github.com/',
    packages=find_packages(exclude=['tests', 'tests_windows']),
    entry_points={
        'console_scripts': ['andy=cli:cli'],
    },
    install_requires=required,
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License ::  MIT License',
    ]
)
