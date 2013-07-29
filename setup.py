#!/usr/bin/env python

#from distutils.core import setup
from setuptools import setup

setup(name='pysensu',
      version='0.5',
      description='Utilities for working with Sensu',
      author='K. Daniels',
      author_email='kd@gc.io',
      url='https://github.com/kdaniels/pysensu',
      packages=['pysensu'],
      install_requires=[
        "requests >= 1.2.3",
        "simplejson >= 3.3.0",
      ],
      )
