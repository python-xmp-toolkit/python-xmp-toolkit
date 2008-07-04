# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, European Space Agency & European Southern Observatory
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
#       Observatory nor the names of its contributors may be used to endorse or 
#       promote products derived from this software without specific prior 
#       written permission.
# 
# THIS SOFTWARE IS PROVIDED BY <copyright holder> ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <copyright holder> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE

import ctypes
import os

_XMP_ERROR_CODES = {
	# More or less generic error codes. 
	0 : 'XMPErr_Unknown',
	-1 : 'XMPErr_TBD',
	-2 : 'XMPErr_Unavailable',
	-3 : 'XMPErr_BadObject',
	-4 : 'XMPErr_BadParam',
	-5 : 'XMPErr_BadValue',
	-6 : 'XMPErr_AssertFailure',
	-7 : 'XMPErr_EnforceFailure',
	-8 : 'XMPErr_Unimplemented',
	-9 : 'XMPErr_InternalFailure',
	-10 : 'XMPErr_Deprecated',
	-11 : 'XMPErr_ExternalFailure',
	-12 : 'XMPErr_UserAbort',
	-13 : 'XMPErr_StdException',
	-14 : 'XMPErr_UnknownException',
	-15 : 'XMPErr_NoMemory',

	# More specific parameter error codes.
	-101 : 'XMPErr_BadSchema',
	-102 : 'XMPErr_BadXPath',
	-103 : 'XMPErr_BadOptions',
	-104 : 'XMPErr_BadIndex',
	-105 : 'XMPErr_BadIterPosition',
	-106 : 'XMPErr_BadParse',
	-107 : 'XMPErr_BadSerialize',
	-108 : 'XMPErr_BadFileFormat',
	-109 : 'XMPErr_NoFileHandler',
	-110 : 'XMPErr_TooLargeForJPEG',

	# File format and internal structure error codes.
	-201 : 'XMPErr_BadXML',
	-202 : 'XMPErr_BadRDF',
	-203 : 'XMPErr_BadXMP',
	-204 : 'XMPErr_EmptyIterator',
	-205 : 'XMPErr_BadUnicode',
	-206 : 'XMPErr_BadTIFF',
	-207 : 'XMPErr_BadJPEG',
	-208 : 'XMPErr_BadPSD',
	-209 : 'XMPErr_BadPSIR',
	-210 : 'XMPErr_BadIPTC',
	-211 : 'XMPErr_BadMPEG'
}

#
# This Python package require that libexempi shared library has been installed.
#
try:
	if os.name == 'posix':
		try: 
			_exempi = ctypes.CDLL( "libexempi.so" )
		except OSError, e:
			_exempi = ctypes.CDLL( "libexempi.dylib" )
	elif os.name == 'nt':
		raise NotImplementedError(u'Windows is currently not supported.')
	else:
		raise NotImplementedError(u'The platform (' + os.name + ') is currently not supported.')
except OSError, e:
	raise LibraryLoadingError('Could not load shared library exempi.')
	

class LibraryLoadingError(StandardError):
	""" Error signaling that the Exempi library cannot be loaded. """
	pass
	
class XMPError(Exception):
	""" General XMP Error. """
	pass
	
# Import classes into global namespace
from core import XMPMeta
from files import XMPFiles

