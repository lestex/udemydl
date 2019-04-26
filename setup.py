#!/usr/bin/env python
import os
import subprocess
from setuptools import setup
from udemy_dl import __version__

requirements = [pkg.split('=')[0] for pkg in open('requirements.txt').readlines()]

description = 'Download videos from Udemy for personal offline use'
# try:
#     subprocess.call(["pandoc", "README.md", "-f", "markdown", "-t", "rst", "-o", "README.rst"])
#     long_description = open("README.rst").read()
# except OSError:
#     print("Pandoc not installed")
long_description = description

classifiers = ['Environment :: Console',
               'Programming Language :: Python :: 2',
               'Programming Language :: Python :: 3',
               'Topic :: Multimedia :: Video',]

setup(name='udemy-dl',
      version=__version__,
      description=description,
      author='Andrey Larin',
      author_email='lestex@gmail.com',
      url='https://github.com/lestex/udemy-dl',      
      install_requires=requirements,
      long_description=long_description,
      packages=['udemy_dl'],
      classifiers=classifiers,
      entry_points={
        'console_scripts': [
            '{}=udemy_dl.__main__:main'.format('udemy-dl')
        ]
      }
    )
