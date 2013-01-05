#!/usr/bin/env python
import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

__author__ = 'Max Arnold <arnold.maxim@gmail.com>'
__version__ = '0.1'

setup(
    name='python-mpns',
    version=__version__,

    # Packaging options.
    include_package_data=True,

    # Package dependencies.
    install_requires=['simplejson', 'requests==1.0.4'],

    # Metadata for PyPI.
    author='Max Arnold',
    author_email='arnold.maxim@gmail.com',
    license='BSD',
    url='http://github.com/max-arnold/python-mpns',
    keywords='mobile push notification microsoft',
    description='Python client for Microsoft Push Notification Service.',
    long_description=open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'README.md')), 'rb').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Communications :: Telephony',
        'Topic :: Internet'
    ]
    packages=[
        'mpns',
    ],
    platforms='any'
)
