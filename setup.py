import sys
try:
    from setuptools import setup, Extension, Command
except ImportError:
    from distutils.core import setup, Extension, Command

VERSION = "0.0.1"


setup(
    name="calcalc",
    version=VERSION,
    author="Nick Kern",
    py_modules=['CalCalc']
)

