#!/usr/bin/env python


"""
Setup script for gpsdio-filtersplit
"""


import os
from setuptools import setup


with open('README.rst') as f:
    readme = f.read().strip()


with open('LICENSE.txt') as f:
    license = f.read().strip()


version = None
author = None
email = None
source = None
with open(os.path.join('gpsdio_filtersplit', '__init__.py')) as f:
    for line in f:
        if line.strip().startswith('__version__'):
            version = line.split('=')[1].strip().replace('"', '').replace("'", '')
        elif line.strip().startswith('__author__'):
            author = line.split('=')[1].strip().replace('"', '').replace("'", '')
        elif line.strip().startswith('__email__'):
            email = line.split('=')[1].strip().replace('"', '').replace("'", '')
        elif line.strip().startswith('__source__'):
            source = line.split('=')[1].strip().replace('"', '').replace("'", '')
        elif None not in (version, author, email, source):
            break


setup_args = dict(
    author=author,
    author_email=email,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Communications',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Utilities',
    ],
    description="A CLI plugin for `gpsdio` that splits, filters and transforms messages using python expressions.",
    entry_points='''
        [gpsdio.gpsdio_plugins]
        sort=gpsdio_filtersplit.core:gpsdio_filtersplit
    ''',
    extras_require={
        'test': ['pytest', 'pytest-cov']
    },
    include_package_data=True,
    install_requires=[
        'click>=3.0',
        'gpsdio>=0.0.2',
    ],
    keywords='AIS GIS remote sensing sort',
    license=license,
    long_description=readme,
    name='gpsdio-filtersplit',
    packages=['gpsdio_filtersplit'],
    url=source,
    version=version,
    zip_safe=True
)


setup(**setup_args)
