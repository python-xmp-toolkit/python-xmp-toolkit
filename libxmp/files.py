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

"""
The Files module provides support for locating the XMP in a file, adding XMP to a file, 
or updating the XMP in a file. It returns the entire XMP packet, the core pacakage can 
then be used to manipulate the individual XMP properties. :class:`XMPFiles` contains a number of 
"smart" file handlers that know how to efficiently access the XMP in specific file formats. It also 
includes a fallback packet scanner that can be used for unknown file formats. 
"""

from libxmp import XMPError, XMPMeta
from libxmp import _exempi, _XMP_ERROR_CODES, _check_for_error
from libxmp.core import _encode_as_utf8
from libxmp.consts import *

import os

__all__ = ['XMPFiles']

class XMPFiles:
	"""
	API for access to the "main" metadata in a file.
	XMPFiles provides the API for the Exempi's File Handler component.
	This provides convenient access to the main, or document level, XMP for a
	file. The general model is to open a file, read and write the metadata, then
	close the file. While open, portions of the file might be maintained in RAM
	data structures. Memory usage can vary considerably depending on file format
	and access options. The file may be opened for read-only or read-write access,
	with typical exclusion for both modes.

	Errors result in raising of an :exc:`libxmp.XMPError` exception.
		
	:keyword file_path: 	Path to file to open.
	
	.. todo:: 
		Documentation
    """
	def __init__(self, **kwargs ):
		self._file_path = None
		self.xmpfileptr = _exempi.xmp_files_new()
			
		if kwargs.has_key( 'file_path' ):
			file_path = kwargs['file_path']
			del kwargs['file_path']
			
			self.open_file( file_path, **kwargs )
			
			
	def __del__(self):
		"""
		Free up the memory associated with the XMP file instance.
		"""
		if not _exempi.xmp_files_free( self.xmpfileptr ):
			raise XMPError( 'Could not free memory for XMPFiles.' )

		
	def open_file(self, file_path, **kwargs ):
		"""
		Open a given file and read XMP from file. File must be closed again with
		:func:`close_file`
		
		:param file_path: Path to file to open.
		:raises XMPError: in case of errors.
		
		.. todo:: 
			Change signature into using kwargs to set option flag
		"""
		open_flags = options_mask( XMP_OPEN_OPTIONS, **kwargs ) if kwargs else XMP_OPEN_NOOPTION
		
		if self._file_path != None:
			raise XMPError('A file is already open - close it first.')
		
		# Ensure file path is UTF-8 encoded (expected by Exempi)
		file_path = _encode_as_utf8(file_path)
		
		if not os.path.exists(file_path):
			raise XMPError('File does not exists.')
				
		if _exempi.xmp_files_open( self.xmpfileptr, file_path, open_flags ):
			self._file_path = file_path
		else:
			_check_for_error()
	
	def close_file( self, close_flags = XMP_CLOSE_NOOPTION ):
		"""
		Close file after use. XMP will not be written to file until
		this method has been called.
		
		:param close_flags: One of the close flags
		:raises XMPError: in case of errors.
		
		.. todo:: 
			Change signature into using kwargs to set option flag
		"""
		if not _exempi.xmp_files_close( self.xmpfileptr, close_flags ):
			_check_for_error()
		else:
			self._file_path = None
		
	def get_xmp( self ):
		""" 
		Get XMP from file.
		
		:return: A new :class:`libxmp.core.XMPMeta` instance.
		:raises XMPError: in case of errors.
		"""
		xmpptr = _exempi.xmp_files_get_new_xmp( self.xmpfileptr )
		_check_for_error()
		
		if xmpptr:
			return XMPMeta( _xmp_internal_ref = xmpptr )
		else:
			return None
		
	def put_xmp( self, xmp_obj ):
		"""
		Write XMPMeta object to file. See also :func:`can_put_xmp`.
		
		:param xmp_obj: An :class:`libxmp.core.XMPMeta` object
		"""
		xmpptr = xmp_obj.xmpptr
		
		if xmpptr != None:
			if not _exempi.xmp_files_put_xmp( self.xmpfileptr, xmpptr ):
				_check_for_error()
		
	def can_put_xmp( self, xmp_obj ):
		"""
		Determines if a given :class:`libxmp.core.XMPMeta` objet can be written in the file.
		
		:param xmp_obj: An :class:`libxmp.core.XMPMeta` object
		:return:  true if :class:`libxmp.core.XMPMeta` object can be written in file.
		:rtype: bool
		"""
		if not isinstance( xmp_obj, XMPMeta ):
			raise XMPError('Not a XMPMeta object')
			
		xmpptr = xmp_obj.xmpptr
		
		if xmpptr != None:
			return _exempi.xmp_files_can_put_xmp(self.xmpfileptr, xmpptr )
		else:
			return False