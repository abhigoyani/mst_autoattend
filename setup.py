import os
import sys
from distutils.core import setup

from setuptools import setup, find_packages

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 6)

# This check and everything above must remain compatible with Python 2.7.
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================
This version requires Python {}.{}, but you're trying to
install it on Python {}.{}.
""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)


setup(name='mst_autoattend',
    version='0.1',
    package_dir = {'': 'src'},
    packages=find_packages(),
    description='A tool to attend the MS Team meetings for you!',
    author='Shivam Kumar Jha',
    author_email='coffee@thealphadollar.me',
    url='https://github.com/thealphadollar/MS-Teams-Class-Attender',
    install_requires=[
    'webdriver_manager==3.2.1',
    'selenium==3.141.0',
    ],
    entry_points={
        'console_scripts': [
            'mst_autoattend=mst_autoattend:main',
        ],
    },
    include_package_data=True
)
