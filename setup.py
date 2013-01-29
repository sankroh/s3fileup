#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
    from setuptools.command.test import test
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages
    from setuptools.command.test import test


class mytest(test):
    def run(self, *args, **kwargs):
        from runtests import runtests
        runtests()

setup(
    name='s3fileup',
    version='0.1.0',
    author='Rohit Sankaran',
    author_email='rohit@riot.io',
    url='http://github.com/heartherumble/s3fileup',
    description = 'Django app that exposes a file upload API to S3, direct from the client',
    packages=find_packages(),
    zip_safe=False,
    install_requires=['boto'],
    tests_require = [
        'Django',
        'boto',
    ],
    test_suite = 'nexus.tests',
    include_package_data=True,
    cmdclass={"test": mytest},
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
