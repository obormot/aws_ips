#!/usr/bin/env python
"""
Setup script for the AWS IPs tool.
It uses setuptools package https://pypi.org/project/setuptools/

distutils didn't use because of https://docs.python.org/3/library/distutils.html

Several setup.py examples:
https://github.com/aws/aws-cli/blob/develop/setup.py
https://github.com/pytorch/vision/blob/master/setup.py
https://github.com/sibblegp/b2blaze/blob/master/setup.py

NOTE: Also there is a setup.cfg file but it isn't in use here for now

The official docs:
https://docs.python.org/3/distutils/setupscript.html
https://docs.python.org/3/distutils/configfile.html
"""
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    print('Please install setuptool package')
    sys.exit(1)

VERSION = '0.0.1'

with open('README.md') as f:
    README = f.read()

with open('requirements.txt') as f:
    REQUIREMENTS = f.readlines()

setup(
    name='aws_ips',
    version=VERSION,
    description='List all public IP addresses tied to an AWS account.',
    long_description=README,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    author='artemdevel',
    python_requires='>=2.7',
    url='https://github.com/artemdevel/aws_ips',
    scripts=[
        'bin/aws_ips',
    ],
    install_requires=REQUIREMENTS,
    keywords='aws cloud ip',
    classifiers=[
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Software Development :: Tools',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ],
    license='Apache License 2.0',
)
