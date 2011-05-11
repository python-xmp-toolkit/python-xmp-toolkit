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
# Search with pattern "([a-z \*]+) (xmp_[a-z0-9_]+)\((.*)\);" and replace with "	'\2' : { 'argstypes' : "\3", 'restype' : "\1" }"
_function_types = {
	'xmp_init' : { 'argstypes' : "", 'restype' : "bool" },
	'xmp_terminate' : { 'argstypes' : "", 'restype' : "void" },
	'xmp_get_error' : { 'argstypes' : "", 'restype' : "int" },
	'xmp_files_new' : { 'argstypes' : "", 'restype' : "XmpFilePtr" },
	'xmp_files_open_new' : { 'argstypes' : "const char *, XmpOpenFileOptions options", 'restype' : "XmpFilePtr" },
	'xmp_files_open' : { 'argstypes' : "XmpFilePtr xf, const char *, XmpOpenFileOptions options", 'restype' : "bool" },
	'xmp_files_close' : { 'argstypes' : "XmpFilePtr xf, XmpCloseFileOptions options", 'restype' : "bool" },
	'xmp_files_get_new_xmp' : { 'argstypes' : "XmpFilePtr xf", 'restype' : "XmpPtr" },
	'xmp_files_get_xmp' : { 'argstypes' : "XmpFilePtr xf, XmpPtr xmp", 'restype' : "bool" },
	'xmp_files_can_put_xmp' : { 'argstypes' : "XmpFilePtr xf, XmpPtr xmp", 'restype' : "bool" },
	'xmp_files_put_xmp' : { 'argstypes' : "XmpFilePtr xf, XmpPtr xmp", 'restype' : "bool" },
	'xmp_files_free' : { 'argstypes' : "XmpFilePtr xf", 'restype' : "bool" },
	'xmp_register_namespace' : { 'argstypes' : "const char *namespaceURI, const char *suggestedPrefix, XmpStringPtr registeredPrefix", 'restype' : "bool" },
	'xmp_namespace_prefix' : { 'argstypes' : "const char *ns, XmpStringPtr prefix", 'restype' : "bool" },
	'xmp_prefix_namespace_uri' : { 'argstypes' : "const char *prefix, XmpStringPtr ns", 'restype' : "bool" },
	'xmp_new_empty' : { 'argstypes' : "", 'restype' : "XmpPtr" },
	'xmp_new' : { 'argstypes' : "const char *buffer, size_t len", 'restype' : "XmpPtr" },
	'xmp_copy' : { 'argstypes' : "XmpPtr xmp", 'restype' : "XmpPtr" },
	'xmp_free' : { 'argstypes' : "XmpPtr xmp", 'restype' : "bool" },
	'xmp_parse' : { 'argstypes' : "XmpPtr xmp, const char *buffer, size_t len", 'restype' : "bool" },
	'xmp_serialize' : { 'argstypes' : "XmpPtr xmp, XmpStringPtr buffer, uint32_t options, uint32_t padding", 'restype' : "bool" },
	'xmp_serialize_and_format' : { 'argstypes' : "XmpPtr xmp, XmpStringPtr buffer, uint32_t options, uint32_t padding, const char *newline, const char *tab, int32_t indent", 'restype' : "bool" },
	'xmp_get_property' : { 'argstypes' : "XmpPtr xmp, const char *schema, const char *name, XmpStringPtr property, uint32_t *propsBits", 'restype' : "bool" },
	'xmp_get_property_date' : { 'argstypes' : "XmpPtr xmp, const char *schema, const char *name, XmpDateTime * property, uint32_t *propsBits", 'restype' : "bool" },
	'xmp_get_property_float' : { 'argstypes' : "XmpPtr xmp, const char *schema, const char *name, double * property,uint32_t *propsBits", 'restype' : "bool" },
	'xmp_get_property_bool' : { 'argstypes' : "XmpPtr xmp, const char *schema, const char *name, bool * property,uint32_t *propsBits", 'restype' : "bool" },
	'xmp_get_property_int32' : { 'argstypes' : "XmpPtr xmp, const char *schema, const char *name, int32_t * property,uint32_t *propsBits", 'restype' : "bool" },
	'xmp_get_property_int64' : { 'argstypes' : "XmpPtr xmp, const char *schema, const char *name, int64_t * property,uint32_t *propsBits", 'restype' : "bool" },
	'xmp_get_array_item' : { 'argstypes' : "XmpPtr xmp, const char *schema, const char *name, int32_t index, XmpStringPtr property,uint32_t *propsBits", 'restype' : "bool" },
	'xmp_set_property' : { 'argstypes' : "XmpPtr xmp, const char *schema, const char *name, const char *value,uint32_t optionBits", 'restype' : "bool" },
	'xmp_set_property_date' : { 'argstypes' : "XmpPtr xmp, const char *schema, const char *name, const XmpDateTime *value,uint32_t optionBits", 'restype' : "bool" },
	'xmp_set_property_float' : { 'argstypes' : "XmpPtr xmp, const char *schema, const char *name, double value,uint32_t optionBits", 'restype' : "bool" },
	'xmp_set_property_bool' : { 'argstypes' : "XmpPtr xmp, const char *schema, const char *name, bool value,uint32_t optionBits", 'restype' : "bool" },
	'xmp_set_property_int32' : { 'argstypes' : "XmpPtr xmp, const char *schema, const char *name, int32_t value,uint32_t optionBits", 'restype' : "bool" },
	'xmp_set_property_int64' : { 'argstypes' : "XmpPtr xmp, const char *schema, const char *name, int64_t value,uint32_t optionBits", 'restype' : "bool" },
	'xmp_set_array_item' : { 'argstypes' : "XmpPtr xmp, const char *schema, const char *name, int32_t index, const char *value,uint32_t optionBits", 'restype' : "bool" },
	'xmp_append_array_item' : { 'argstypes' : "XmpPtr xmp, const char *schema, const char *name,uint32_t arrayOptions, const char *value,uint32_t optionBits", 'restype' : "bool" },
	'xmp_delete_property' : { 'argstypes' : "XmpPtr xmp, const char *schema, const char *name", 'restype' : "bool" },
	'xmp_has_property' : { 'argstypes' : "XmpPtr xmp, const char *schema, const char *name", 'restype' : "bool" },
	'xmp_get_localized_text' : { 'argstypes' : "XmpPtr xmp, const char *schema, const char *name,const char *genericLang, const char *specificLang,XmpStringPtr actualLang, XmpStringPtr itemValue,uint32_t *propBits", 'restype' : "bool" },
	'xmp_set_localized_text' : { 'argstypes' : "XmpPtr xmp, const char *schema, const char *name,const char *genericLang, const char *specificLang,const char *value, uint32_t optionBits", 'restype' : "bool" },
	'xmp_delete_localized_text' : { 'argstypes' : "XmpPtr xmp, const char *schema,const char *name, const char *genericLang,const char *specificLang", 'restype' : "bool" },
	'xmp_string_new' : { 'argstypes' : "", 'restype' : "XmpStringPtr" },
	'xmp_string_free' : { 'argstypes' : "XmpStringPtr s", 'restype' : "void" },
	'xmp_string_cstr' : { 'argstypes' : "XmpStringPtr s", 'restype' : "const char *" },
	'xmp_iterator_new' : { 'argstypes' : "XmpPtr xmp, const char * schema,const char * propName, XmpIterOptions options", 'restype' : "XmpIteratorPtr" },
	'xmp_iterator_free' : { 'argstypes' : "XmpIteratorPtr iter", 'restype' : "bool" },
	'xmp_iterator_next' : { 'argstypes' : "XmpIteratorPtr iter, XmpStringPtr schema,XmpStringPtr propName, XmpStringPtr propValue,uint32_t *options", 'restype' : "bool" },
	'xmp_iterator_skip' : { 'argstypes' : "XmpIteratorPtr iter, XmpIterSkipOptions options", 'restype' : "bool" },
}

# Definitions of how to convert the function types to ctypes

_typeconv = {
	'XmpPtr' : ctypes.c_void_p,
	'XmpStringPtr' : ctypes.c_void_p,
	'XmpFilePtr' : ctypes.c_void_p,
	'XmpIteratorPtr' : ctypes.c_void_p,
	'const char *' : ctypes.c_char_p,
	'int' : ctypes.c_int,
	'void' : None,
	'XmpIterSkipOptions' : ctypes.c_int,
	'XmpOpenFileOptions' : ctypes.c_int,
	'XmpCloseFileOptions' : ctypes.c_int,
	'XmpIterOptions' : ctypes.c_int,
	'size_t' : ctypes.c_ulonglong if is_64 else ctypes.c_uint,
	'XmpDateTime *' : ctypes.c_void_p,
	'const XmpDateTime *' : ctypes.c_void_p,
	'uint32_t' : ctypes.c_uint,
	'uint32_t *' : ctypes.c_void_p,
	'int32_t' : ctypes.c_int,
	'int32_t *' : ctypes.c_void_p,
	'int64_t' : ctypes.c_longlong,
	'int64_t *' : ctypes.c_void_p,	
	'double' : ctypes.c_double,
	'double *' : ctypes.c_void_p,
	'bool' : ctypes.c_int, # c_bool only defined in 2.6+
	'bool *' : ctypes.c_void_p,
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