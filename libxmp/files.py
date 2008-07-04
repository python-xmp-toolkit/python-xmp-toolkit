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

from libxmp import XMPError
from libxmp import XMPMeta
from libxmp import _exempi, _XMP_ERROR_CODES
import os

#
# Open options
#
XMP_OPEN_NOOPTION = 0x00000000 #< No open option
XMP_OPEN_READ = 0x00000001 #< Open for read-only access.
XMP_OPEN_FORUPDATE = 0x00000002 #< Open for reading and writing.
XMP_OPEN_ONLYXMP = 0x00000004 #< Only the XMP is wanted, allows space/time optimizations.
XMP_OPEN_CACHETNAIL = 0x00000008 #< Cache thumbnail if possible,  GetThumbnail will be called.
XMP_OPEN_STRICTLY = 0x00000010 #< Be strict about locating XMP and reconciling with other forms. 
XMP_OPEN_USESMARTHANDLER = 0x00000020 #< Require the use of a smart handler.
XMP_OPEN_USEPACKETSCANNING = 0x00000040 #< Force packet scanning, don't use a smart handler.
XMP_OPEN_LIMITSCANNING = 0x00000080 #< Only packet scan files "known" to need scanning.
XMP_OPEN_INBACKGROUND = 0x10000000  #< Set if calling from background thread.

#
# Close options
#
XMP_CLOSE_NOOPTION      = 0x0000 #< No close option */
XMP_CLOSE_SAFEUPDATE    = 0x0001 #< Write into a temporary file and swap for crash safety.

#
# File formats
#
XMP_FT_PDF      = 0x50444620L  #  'PDF ' 
XMP_FT_PS       = 0x50532020L  #  'PS  ' general PostScript following DSC conventions. 
XMP_FT_EPS      = 0x45505320L  #  'EPS ' encapsulated PostScript. 
XMP_FT_JPEG     = 0x4A504547L  #  'JPEG' 
XMP_FT_JPEG2K   = 0x4A505820L  #  'JPX ' ISO 15444-1 
XMP_FT_TIFF     = 0x54494646L  #  'TIFF' 
XMP_FT_GIF      = 0x47494620L  #  'GIF ' 
XMP_FT_PNG      = 0x504E4720L  #  'PNG '   
XMP_FT_SWF      = 0x53574620L  #  'SWF ' 
XMP_FT_FLA      = 0x464C4120L  #  'FLA ' 
XMP_FT_FLV      = 0x464C5620L  #  'FLV ' 
XMP_FT_MOV      = 0x4D4F5620L  #  'MOV ' Quicktime 
XMP_FT_AVI      = 0x41564920L  #  'AVI ' 
XMP_FT_CIN      = 0x43494E20L  #  'CIN ' Cineon 
XMP_FT_WAV      = 0x57415620L  #  'WAV ' 
XMP_FT_MP3      = 0x4D503320L  #  'MP3 ' 
XMP_FT_SES      = 0x53455320L  #  'SES ' Audition session 
XMP_FT_CEL      = 0x43454C20L  #  'CEL ' Audition loop 
XMP_FT_MPEG     = 0x4D504547L  #  'MPEG' 
XMP_FT_MPEG2    = 0x4D503220L  #  'MP2 ' 
XMP_FT_MPEG4    = 0x4D503420L  #  'MP4 ' ISO 14494-12 and -14 
XMP_FT_WMAV     = 0x574D4156L  #  'WMAV' Windows Media Audio and Video 
XMP_FT_AIFF     = 0x41494646L  #  'AIFF' 
XMP_FT_HTML     = 0x48544D4CL  #  'HTML' 
XMP_FT_XML      = 0x584D4C20L  #  'XML ' 
XMP_FT_TEXT     = 0x74657874L  #  'text' 
#  Adobe application file formats. 
XMP_FT_PHOTOSHOP       = 0x50534420L  #  'PSD ' 
XMP_FT_ILLUSTRATOR     = 0x41492020L  #  'AI  ' 
XMP_FT_INDESIGN        = 0x494E4444L  #  'INDD' 
XMP_FT_AEPROJECT       = 0x41455020L  #  'AEP ' 
XMP_FT_AEPROJTEMPLATE  = 0x41455420L  #  'AET ' After Effects Project Template 
XMP_FT_AEFILTERPRESET  = 0x46465820L  #  'FFX ' 
XMP_FT_ENCOREPROJECT   = 0x4E434F52L  #  'NCOR' 
XMP_FT_PREMIEREPROJECT = 0x5052504AL  #  'PRPJ' 
XMP_FT_PREMIERETITLE   = 0x5052544CL  #  'PRTL' 
# Catch all
XMP_FT_UNKNOWN  = 0x20202020L

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

	Errors result in the throw of an XMPError exception.
	
	Note not all methods are implemented and also some options of methods.
    """

	def __init__(self, **kwargs ):
		"""
		@param file_path Path to file to open.
		"""
		self.xmpfileptr = _exempi.xmp_files_new()
			
		if kwargs.has_key( 'file_path' ):
			file_path = kwargs['file_path']
			
			format = XMP_FT_UNKNOWN
			open_flags = XMP_OPEN_NOOPTION
			if kwargs.has_key('format'):
				format = kwargs['format']
			if kwargs.has_key('open_flags'):
				open_flags = kwargs['open_flags']
			
			self.open( file_path, format, open_flags )
			
			
	def __del__(self):
		"""
		Free up the memory associated with the XMP file instance.
		"""
		if not _exempi.xmp_files_free( self.xmpfileptr ):
			raise XMPError('Could not free memory for XMPFiles.')
		
	def open_file(self, file_path, open_flags = XMP_OPEN_NOOPTION, format = XMP_FT_UNKNOWN ):
		"""
		@param open_flags One of the open flags.
		@param format Not implemented. Put for forward compatiblilty with TXMPFiles C++ class
		"""
		if not os.path.exists(file_path):
			raise XMPError('File does not exists.')
			
		if _exempi.xmp_files_open( self.xmpfileptr, file_path, open_flags ):
			self.file_path = file_path
		else:
			self._check_for_error()
	
	def close_file( self, close_flags = XMP_CLOSE_NOOPTION ):
		"""
		@param close_flags One of the close flags
		"""
		if not _exempi.xmp_files_close( self.xmpfileptr, close_flags ):
			self._check_for_error()
		
		
	def get_xmp( self ):
		""" 
		Get metadata from file.
		
		@return A new XMPMeta instance.
		"""
		xmpptr = _exempi.xmp_files_get_new_xmp( self.xmpfileptr )
		self._check_for_error()
		return XMPMeta( xmp_internal_ref = xmpptr )
		
	def put_xmp( self, xmp_obj ):
		"""
		@param xmp_obj An XMPMeta object
		"""
		xmpptr = xmp_obj._get_internal_ref()
		
		if xmpptr != None:
			if not _exempi.xmp_files_put_xmp( self.xmpfileptr, xmpptr ):
				self._check_for_error()
		
	def can_put_xmp( self, xmp_obj ):
		"""
		@param xmp_obj An XMPMeta object
		"""
		xmpptr = xmp_obj._get_internal_ref()
		
		if xmpptr != None:
			return _exempi.xmp_files_can_put_xmp(self.xmpfileptr, xmpptr )
		else:
			return False
		
	def _check_for_error(self):
		"""
		Check if an error occured when executing last operation. Raise an
		exception in case of an error.
		"""
		err = _exempi.xmp_get_error()
		if err != 0:
			raise XMPError( _XMP_ERROR_CODES[err] )
			
	def get_thumbnail( self ):
		""" 
		Not Implemented - Exempi does not implement this function yet
		"""
		raise NotImplementedError

	def get_file_info( self ):
		""" 
		Not Implemented - Exempi does not implement this function yet
		"""
		raise NotImplementedError
		
	@staticmethod
	def initialize( options = None ):
		"""
		Initialize library. Must be called before anything else.
		
		@param options Not implemented - provided for future implementations.
		"""
		if not _exempi.xmp_init():
			self._check_for_error()
	
	@staticmethod
	def terminate():
		_exempi.xmp_terminate()
	
	@staticmethod
	def get_version_info():
		""" 
		Not Implemented - Exempi does not implement this function yet
		"""
		raise NotImplementedError
	
	@staticmethod
	def get_format_info( format ):
		""" 
		Not Implemented - Exempi does not implement this function yet
		"""
		raise NotImplementedError