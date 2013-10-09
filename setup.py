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

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

try:
    VERSION = open('VERSION', 'r').readline().strip()
except IOError as err:
    MSG = "Error: you must run setup from the root directory ({0})"
    MSG = MSG.format(err)
    raise SystemExit(MSG)

LONG_DESC = "Python XMP Toolkit is a library for working with XMP metadata, "
LONG_DESC += "as well as reading/writing XMP metadata stored in many "
LONG_DESC += "different file formats."

DOWNLOAD_URL = 'http://code.google.com/p/python-xmp-toolkit/downloads/list'

KWARGS = {
    'name': 'python-xmp-toolkit',
    'description': 'Python XMP Toolkit for working with metadata.',
    'author': 'Lars Holm Nielsen, Federico Caboni & Amit Kapadia',
    'author_email': 'lnielsen@eso.org,federico.caboni@me.com,akapad@gmail.com',
    'url': 'http://code.google.com/p/python-xmp-toolkit/',
    'long_description': LONG_DESC,
    'download_url': DOWNLOAD_URL,
    'license': 'New BSD License',
    'install_requires': ['flufl.enum>=4.0']
    'packages': find_packages(exclude=["*test*"]),
    'version': VERSION
}

setup(**KWARGS)
