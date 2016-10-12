#!/usr/bin/env python
import os
from setuptools import setup

cwd = os.path.dirname(os.path.abspath(__name__))

long_description = open(os.path.join(cwd, 'README.rst'), 'r').read()

setup(
    name='inflow',
    version='0.1.0a2',
    author='Jaap Broekhuizen',
    author_email='broekhuizen@baopt.nl',
    description='A simple InfluxDB client library.',
    url='https://github.com/AdvancedClimateSystems/inflow/',
    long_description=long_description,
    license='MPL',
    packages=['inflow'],
    install_requires=[
        'requests~=2.11.1',
        'six~=1.10.0'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ]
)
