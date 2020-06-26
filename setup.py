#!/usr/bin/env python

from setuptools import setup
import os
import glob

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

requirements = []
with open(os.path.join(this_directory, 'requirements.txt'), encoding='utf-8') as r:
    line = r.readline()
    while line:
        requirements.append(line.strip())
        line = r.readline()


def getFiles(path):
    files = []
    (root, dirNames, fileNames) = next(os.walk(path))

    fileNames.sort()
    dirFiles = []
    for fileName in fileNames:
        dirFiles.append(os.path.join(path, fileName))
    files.append((path, dirFiles))

    dirNames.sort()
    for dirName in dirNames:
        files.extend(getFiles(os.path.join(root, dirName)))

    return files


setup(
    name='azbacklog',
    author="Joshua Davis",
    author_email="me@jdav.is",
    url='https://github.com/Azure/Azure-Backlog-Generator',
    version='0.2.0',
    description='The Azure Backlog Generator (ABG) is designed to build backlogs for complex processes based on proven practices. The backlogs can be generated in either Azure DevOps or GitHub.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_dir={'': 'src'},
    packages=[
        'azbacklog',
        'azbacklog.entities',
        'azbacklog.helpers',
        'azbacklog.services'
    ],
    data_files=getFiles('workitems'),
    install_requires=[
        'pygithub==1.51',
        'azure-devops==6.0.0b2'
    ],
    extras_require={
        'dev': requirements
    },
    entry_points={
        'console_scripts': {
            'azbacklog = azbacklog.azbacklog:main'
        }
    },
    python_requires='>=3.6'
)
