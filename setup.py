#!/usr/bin/env python

from setuptools import find_packages, setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

requirements = []
with open(path.join(this_directory, 'requirements.txt'), encoding='utf-8') as r:
    line = r.readline()
    while line:
        requirements.append(line.strip())
        line = r.readline()

setup(
    name='azbacklog',
    author="Joshua Davis",
    author_email="me@jdav.is",
    url='https://github.com/Azure/Azure-Backlog-Generator',
    version='0.1.0',
    description='The Azure Backlog Generator (ABG) is designed to build backlogs for complex processes based on proven practices. The backlogs can be generated in either Azure DevOps or GitHub.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'pygithub'
    ],
    extras_require={
        'dev': requirements
    },
    scripts=['src/scripts/azbacklog'],
    python_requires='>=3.6'
)
