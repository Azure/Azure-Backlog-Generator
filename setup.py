#!/usr/bin/env python

from setuptools import find_packages, setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='azbacklog',
    version='1.0.0',
    description='The Azure Backlog Generator (ABG) is designed to build backlogs for complex processes based on proven practices. The backlogs can be generated in either Azure DevOps or GitHub.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'pygithub'
    ],
    extras_require={
        'dev': [
            'pyfakefs',
            'pytest',
            'coverage'
        ]
    },
    scripts=['src/scripts/main.py']
)