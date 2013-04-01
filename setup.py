#!/usr/bin/env python
from distutils.core import setup
from setuptools import find_packages
import sys

if sys.version_info <= (2, 5):
    error = "ERROR: stackformation requires Python Version 2.6 or above...exiting."
    print >> sys.stderr, error
    sys.exit(1)

setup(name="stackformation",
      version=stackformation.__version__,
      author="Steffen Opel",
      packages=find_packages(),
      license="Apache 2",
      platforms="Posix; MacOS X; Windows",
      install_requires=[
        "boto >= 2.6.0",
        "botocross >= 1.1.0",
      ],
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Intended Audience :: Developers",
          "Intended Audience :: System Administrators",
          "License :: OSI Approved :: Apache Software License",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Topic :: Internet",
          ],
      )
