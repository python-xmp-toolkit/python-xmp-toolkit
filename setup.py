# -*- coding: utf-8 -*-
#
# Copyright (c) 2008-2009, European Space Agency & European Southern
# Observatory (ESA/ESO)
# Copyright (c) 2008-2009, CRS4 - Centre for Advanced Studies, Research and
# Development in Sardinia
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
#     * Neither the name of the European Space Agency, European Southern
#       Observatory, CRS4 nor the names of its contributors may be used to
#       endorse or promote products derived from this software without specific
#       prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY ESA/ESO AND CRS4 ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL ESA/ESO BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER # IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE

"""
Install script for libxmp.
"""
import os
import re
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

# Install requirements.
test_requires = []
if sys.hexversion < 0x03030000:
    test_requires.append('mock>=1.0.1')
if sys.hexversion < 0x02070000:
    test_requires.append('unittest2>=0.5.1')

KWARGS = {
    'name': 'python-xmp-toolkit',
    'description': 'Python XMP Toolkit for working with metadata.',
    'author': 'Lars Holm Nielsen, John Evans, Federico Caboni & Amit Kapadia',
    'author_email': 'lars@hankat.dk',
    'url': 'https://github.com/python-xmp-toolkit/python-xmp-toolkit',
    'long_description': open('README.rst').read(),
    'download_url': 'https://pypi.python.org/pypi/python-xmp-toolkit',
    'license': 'New BSD License',
    'install_requires': ['pytz'],
    'packages': find_packages(exclude=["*test*"]),
    'test_suite': 'test',
    'tests_require': test_requires,
    'classifiers': [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ],
}

# Get the version string.  Cannot do this by importing libxmp!
version_file = os.path.join('libxmp', 'version.py')
with open(version_file, 'rt') as fptr:
    contents = fptr.read()
    match = re.search('VERSION\s*=\s*"(?P<version>\d*.\d*.\d*.*)"\n', contents)
    KWARGS['version'] = match.group('version')

setup(**KWARGS)
