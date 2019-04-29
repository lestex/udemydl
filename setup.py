#!/usr/bin/env python
from setuptools import setup
from udemy_dl import __version__, __author__, __email__
import os

requirements = [pkg.split('=')[0] for pkg in open('requirements.txt').readlines()]

description = 'Download videos from Udemy for personal offline use'

this_directory = os.path.abspath(os.path.dirname(__file__))

try:
    with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except OSError:
    print("Couldn't find README.md")

classifiers = ['Environment :: Console',
               'Programming Language :: Python :: 2',
               'Programming Language :: Python :: 3',
               'Topic :: Multimedia :: Video',]

setup(name='udemydl',
    version=__version__,
    description=description,
    author=__author__,
    author_email=__email__,
    url='https://github.com/lestex/udemydl',      
    install_requires=requirements,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['udemy_dl'],
    classifiers=classifiers,
    entry_points={
        'console_scripts': [
            '{}=udemy_dl.__main__:main'.format('udemydl')
        ]
    }
)
