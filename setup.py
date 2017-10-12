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
    name='rooter',
    version=about['__version__'],
    description='Blehhhhh.',
    long_description=long_description,
    author='Some guy',
    author_email='me@xxx.com',
    url='https://github.com/',
    packages=find_packages(exclude=['tests', 'tests_windows']),
    entry_points={
        'console_scripts': ['rooter=cli:cli'],
    },
    install_requires=required,
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ]
)
