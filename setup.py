#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

packages = [
    's3fileup',
]

setup(
    name='django-s3fileup',
    version='0.4',
    author='Rohit Sankaran',
    author_email='rohit@riot.io',
    url='http://github.com/roadhead/s3fileup',
    description = 'Django app that exposes a file upload API to S3, direct from the client',
    packages=packages,
    package_data={'': ['README.md', 'LICENSE', 'AUTHORS'],},
    package_dir={'s3fileup': 's3fileup'},
    zip_safe=False,
    install_requires=[
        'boto>=2.7.0',
        'djangorestframework>=2.3.6',
    ],
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
