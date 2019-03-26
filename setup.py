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

required = [
    "crayons",
    "requests",
    "pexpect",
    "blindspin",
]

_TEST_REQUIRE = [
    "pytest==4.1.1",
    "pytest-cov==2.6.1",
    "pytest-asyncio==0.10.0",
    "pylint==2.3.0",
    "black==18.9b0",
    "isort==4.3.4",
]

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
    tests_require=_TEST_REQUIRE,
    extras_require={"test": _TEST_REQUIRE},
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License ::  MIT License',
    ]
)
