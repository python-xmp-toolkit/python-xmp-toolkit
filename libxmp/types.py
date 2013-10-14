# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, European Space Agency & European Southern Observatory (ESA/ESO)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#      * Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#
#      * Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#
#      * Neither the name of the European Space Agency, European Southern
#        Observatory nor the names of its contributors may be used to endorse or
#        promote products derived from this software without specific prior
#        written permission.
#
# THIS SOFTWARE IS PROVIDED BY ESA/ESO ``AS IS'' AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL ESA/ESO BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE

import ctypes
import sys

try:
    is_64 = sys.maxsize > 2**32
except AttributeError:
    is_64 = False

__all__ = ['define_function_types']

# Following have been extracted from exempi/xmp.h
#
# Edit the file until you have one funciton prototype per line
# Search with pattern "([a-z \*]+) (xmp_[a-z0-9_]+)\((.*)\);" and replace with "    '\2' : { 'argstypes' : "\3", 'restype' : "\1" }"
_function_types = {
    'xmp_files_open' : { 'argstypes' : "XmpFilePtr xf, const char *, XmpOpenFileOptions options", 'restype' : "bool" },
    'xmp_files_close' : { 'argstypes' : "XmpFilePtr xf, XmpCloseFileOptions options", 'restype' : "bool" },
}

# Definitions of how to convert the function types to ctypes

_typeconv = {
    'XmpFilePtr' : ctypes.c_void_p,
    'const char *' : ctypes.c_char_p,
    'XmpOpenFileOptions' : ctypes.c_int,
    'XmpCloseFileOptions' : ctypes.c_int,
    'bool' : ctypes.c_int, # c_bool only defined in 2.6+
}

def _convert_type( t ):
    """
    Convert a C type into ctype type
    """
    try:
        return _typeconv[t]
    except KeyError:
        raise Exception("Type conversion from %s to ctypes type has not been defined" % t)

def _convert_args( argtypes ):
    """
    Convert the type for each argument in argtypes
    """
    if not argtypes:
        return None

    args = [x.strip() for x in argtypes.split(",")]

    tmp = []
    for a in args:
        arg = a.split(" ")
        if arg[-1][0] == "*":
            arg[-1] = "*"
        else:
            del arg[-1]

        arg =  " ".join(arg)
        tmp.append( _convert_type( arg ) )
    return tmp


def define_function_types( exempi ):
    """
    Take ctypes exempi library and set proper return/argument types.
    """
    for func, functypes in _function_types.items():
        res = _convert_type( functypes['restype'] )
        args = _convert_args( functypes['argstypes'] )
        if hasattr( exempi, func ):
            if res:
                getattr( exempi, func ).restype = res
            if args:
                getattr( exempi, func ).argtypes = args
