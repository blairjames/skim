#!/usr/bin/python3.6

from distutils.core import setup
from Cython.Build import cythonize


setup(
    ext_modules = cythonize('*.pyx', annotate=True)
)

