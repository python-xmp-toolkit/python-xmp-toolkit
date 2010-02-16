# -*- coding: utf-8 -*-
#
# Copyright (c) 2008-2009, European Space Agency & European Southern Observatory (ESA/ESO)
# Copyright (c) 2008-2009, CRS4 - Centre for Advanced Studies, Research and Development in Sardinia
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
#       Observatory, CRS4 nor the names of its contributors may be used to endorse or 
#       promote products derived from this software without specific prior 
#       written permission.
# 
# THIS SOFTWARE IS PROVIDED BY ESA/ESO AND CRS4 ``AS IS'' AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL ESA/ESO BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE

import libxmp
import os

"""
The `utils` module includes
"""

__all__ = ['terminate','object_to_dict','file_to_dict']

def object_to_dict(xmp):
	"""
	Extracts all XMP data from a given XMPMeta instance organizing it into a standard
	Python dictionary.
	"""
	d = dict()
	
	if not xmp:
		return {}
	
	for x in xmp:           
		if x[-1]['IS_SCHEMA']:
			d[x[0]] = []
		else:
			d[x[0]].append(x[1:])
	
	return d

def file_to_dict(file_path):
	"""
	Extracts all XMP data from a given file organizing it into a standard Python 
	dictionary.	
	
	:param file_path: Path to file to open.
	:return: An empty dictionary if there's no valid XMP in the file passed as
		an argument.
	"""	
	if not os.path.isfile( os.path.abspath( file_path ) ):
		raise IOError, "No such file or directory: '%s'" % file_path	

	xmpfile = libxmp.files.XMPFiles()
	
	try:
		xmpfile.open_file( file_path, open_read=True )
		xmp = xmpfile.get_xmp()
	except libxmp.XMPError:
		return {}
	
	return object_to_dict(xmp)
	
	
	
def terminate():
	"""
	Terminate usage of library. 
	
	Normally function should not be called. Cases however might exists 
	where memory clean-up is needed, then this method may be called.
	
	.. warning:: 	
		After this function have been called, any call to methods in 
		libxmp will result in a crash of Python.
	
		
	Note, Exempi library is automatically initialized when loading libxmp and normally
	you will not need to call this method. However, there might be cases where 
	"""
	_exempi.xmp_terminate()