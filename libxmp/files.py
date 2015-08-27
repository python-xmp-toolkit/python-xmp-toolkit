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
The Files module provides support for locating the XMP in a file, adding XMP to
a file, or updating the XMP in a file. It returns the entire XMP packet, the
core pacakage can then be used to manipulate the individual XMP properties.
:class:`XMPFiles` contains a number of "smart" file handlers that know how to
efficiently access the XMP in specific file formats. It also includes a
fallback packet scanner that can be used for unknown file formats.
"""
import os
import sys

from . import XMPError, XMPMeta
from .consts import options_mask
from .consts import XMP_CLOSE_NOOPTION
from .consts import XMP_OPEN_OPTIONS
from .consts import XMP_OPEN_NOOPTION
from . import exempi as _cexempi

__all__ = ['XMPFiles']

class XMPFiles(object):
    """API for access to the "main" metadata in a file.

    XMPFiles provides the API for the Exempi's File Handler component.  This
    provides convenient access to the main, or document level, XMP for a file.
    The general model is to open a file, read and write the metadata, then
    close the file. While open, portions of the file might be maintained in RAM
    data structures. Memory usage can vary considerably depending on file
    format and access options. The file may be opened for read-only or
    read-write access, with typical exclusion for both modes.

    Errors result in raising of an :exc:`libxmp.XMPError` exception.

    :keyword file_path:     Path to file to open.

    .. todo::
        Documentation
    """
    def __init__(self, **kwargs ):
        self._file_path = None
        self.xmpfileptr = _cexempi.files_new()

        if 'file_path' in kwargs:
            file_path = kwargs['file_path']
            del kwargs['file_path']

            self.open_file( file_path, **kwargs )

    def __repr__(self):
        if self._file_path is None:
            return "XMPFiles()"

        msg = "XMPFiles(file_path='{0}')"
        if sys.hexversion < 0x03000000 and isinstance(self._file_path,
                                                      unicode):
            # Unicode filenames can cause trouble in python2 because __repr__
            # must return byte strings, not unicode. Get around this by
            # turning the unicode filename into escaped ASCII.  This means that
            # in this case, the result cannot be used to recreate the object
            # with the same value.
            msg = msg.format(repr(self._file_path))
        else:
            # Python3 does not suffer from this problem.
            msg = msg.format(self._file_path)

        return msg

    def __del__(self):
        """
        Free up the memory associated with the XMP file instance.
        """
        _cexempi.files_free( self.xmpfileptr )


    def open_file(self, file_path, **kwargs ):
        """
        Open a given file and read XMP from file. File must be closed again with
        :func:`close_file`

        :param str file_path: Path to file to open.
        :raises XMPError: in case of errors.

        .. todo::
            Change signature into using kwargs to set option flag
        """
        if kwargs:
            open_flags = options_mask( XMP_OPEN_OPTIONS, **kwargs )
        else:
            open_flags = XMP_OPEN_NOOPTION

        if self._file_path != None:
            raise XMPError('A file is already open - close it first.')

        _cexempi.files_open( self.xmpfileptr, file_path, open_flags )
        self._file_path = file_path

    def close_file( self, close_flags=XMP_CLOSE_NOOPTION):
        """
        Close file after use. XMP will not be written to file until
        this method has been called.

        :param close_flags: One of the close flags
        :raises XMPError: in case of errors.

        .. todo::
            Change signature into using kwargs to set option flag
        """
        _cexempi.files_close( self.xmpfileptr, close_flags )
        self._file_path = None

    def get_xmp( self ):
        """
        Get XMP from file.

        :return: A new :class:`libxmp.core.XMPMeta` instance.
        :raises XMPError: in case of errors.
        """
        xmpptr = _cexempi.files_get_new_xmp(self.xmpfileptr)

        if xmpptr:
            return XMPMeta( _xmp_internal_ref = xmpptr )
        else:
            return None

    def put_xmp(self, xmp_obj):
        """
        Write XMPMeta object to file. See also :func:`can_put_xmp`.

        :param xmp_obj: An :class:`libxmp.core.XMPMeta` object
        """
        xmpptr = xmp_obj.xmpptr
        if not self.can_put_xmp(xmp_obj):
            msg = 'Cannot write XMP packet into {filename}'
            msg = msg.format(filename=os.path.basename(self._file_path))
            raise XMPError(msg)
        _cexempi.files_put_xmp(self.xmpfileptr, xmpptr)

    def can_put_xmp( self, xmp_obj ):
        """Determine if XMP can be written into the file.

        Determines if a given :class:`libxmp.core.XMPMeta` object can be
        written into the file.

        :param xmp_obj: An :class:`libxmp.core.XMPMeta` object
        :return:  true if :class:`libxmp.core.XMPMeta` object writeable to file.
        :rtype: bool
        """
        if not isinstance( xmp_obj, XMPMeta ):
            raise XMPError('Not a XMPMeta object')

        xmpptr = xmp_obj.xmpptr

        if xmpptr != None:
            return _cexempi.files_can_put_xmp(self.xmpfileptr, xmpptr)
        else:
            return False
