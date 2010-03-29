# -*- coding: utf-8 -*-
#
# Copyright (c) 2008-2009, European Space Agency & European Southern Observatory (ESA/ESO)
# Copyright (c) 2008-2009, CRS4 - Centre for Advanced Studies, Research and Development in Sardinia
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#	  * Redistributions of source code must retain the above copyright
#		notice, this list of conditions and the following disclaimer.
# 
#	  * Redistributions in binary form must reproduce the above copyright
#		notice, this list of conditions and the following disclaimer in the
#		documentation and/or other materials provided with the distribution.
# 
#	  * Neither the name of the European Space Agency, European Southern 
#		Observatory, CRS4 nor the names of its contributors may be used to endorse or 
#		promote products derived from this software without specific prior 
#		written permission.
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
A module for parsing, manipulating, and serializing XMP data. The core module has 
no knowledge of files. The core API is provided by the :class:`XMPMeta` and :class:`XMPIterator` classes.
"""

from ctypes import *
import datetime

from libxmp import XMPError
from libxmp import _exempi, _XMP_ERROR_CODES, _check_for_error
from libxmp.consts import *
from libxmp import consts

__all__ = ['XMPMeta','XMPIterator']



class _XMPString(object):
	"""
	Helper class (not intended to be exposed) to help managed strings in Exempi
	"""
	def __init__(self):
		self._ptr  = _exempi.xmp_string_new()

	def __del__(self):
		_exempi.xmp_string_free(self._ptr)
		
	def get_ptr(self):
		return self._ptr
	ptr = property(get_ptr)
		
	def __str__(self):
		# Returns a UTF-8 encode 8-bit string. With a encoding specified so it cannot be
		# decoded into a unicode string. This is needed when writing it to a file e.g. 
		return _exempi.xmp_string_cstr(self._ptr)
		
	def __unicode__(self):
		"""
		Note string cannot be used to be written to file, as it the special encoding character
		is not included.
		"""
		s = _exempi.xmp_string_cstr(self._ptr)
		return s.decode('utf-8') #,errors='ignore')
	
def _encode_as_utf8( obj, input_encoding=None ):
	"""
	Helper function to ensure that a proper string object in UTF-8 encoding.
	
	If obj is not a string, it will try to convert the object into a unicode
	string and thereafter encode as UTF-8.
	"""
	if isinstance( obj, unicode ):
		return obj.encode('utf-8')
	elif isinstance( obj, str ):
		if not input_encoding or input_encoding == 'utf-8':
			return obj
		else:
			return obj.decode(input_encoding).encode('utf-8')
	else:
		return unicode( obj ).encode('utf-8')



class _XmpDateTime(Structure):
	"""
	Helper class (not intended to be exposed) to manage datetimes in Exempi
	""" 
	_fields_ = [
					('year', c_int32),
					('month', c_int32),
					('day', c_int32),
					('hour', c_int32),
					('minute', c_int32),
					('second', c_int32),
					('tzSign', c_int32),
					('tzHour', c_int32),
					('tzMinute', c_int32),
					('nanoSecond', c_int32),
				]
				

class XMPMeta(object):
	""" 
	XMPMeta is the class providing the core services of the library
	"""
	
	def __init__( self, **kwargs ):
		"""
		:param xmp_str Optional.
		:param xmp_internal_ref Optional - used for internal purposes.
		"""
		if '_xmp_internal_ref' in kwargs:
			self.xmpptr = kwargs['_xmp_internal_ref']
		else:
			self.xmpptr = _exempi.xmp_new_empty()
			_check_for_error()
		
			if 'xmp_str' in kwargs:
				self.parse_from_str( kwargs['xmp_str'] )
		
		self.iterator = None
		
	def __del__(self):
		"""
		Ensures memory is deallocated when destroying object.
		"""
		if self.xmpptr != None:
			if not _exempi.xmp_free(self.xmpptr):
				_check_for_error()
		
		if self.iterator is not None:
			del self.iterator
			
	
	def __iter__(self):
		"""
		Defines XMPIterator as an iterator for this class' instances
		"""
		
		if self.iterator is None:
			self.iterator = XMPIterator(self)
		
		return self.iterator
		
	def __repr__(self):
		"""
		Prints the serialization of the XMPMeta object.
		"""
		return self.serialize_to_str()
		
	def __eq__(self, other):
		""" Checks if two XMPMeta object are equal. """
		return self.xmpptr == other.xmpptr
		
	def __ne__(self, other):
		""" Checks if two XMPMeta object are not equal. """
		return self.xmpptr != other.xmpptr
	
	# -------------------------------------
	# Functions for getting property values
	# -------------------------------------
	def get_property(self, schema_ns, prop_name):
		"""
		get_property() reports whether a property exists, and retrieves its value.

		This is the simplest property accessor: use this to retrieve the values of top-level simple properties.

		:param schema_ns 	The namespace URI for the property; can be null or the empty string if the first component of the prop_name path contains a namespace prefix.
		:param prop_name 	The name of the property. Can be a general path expression, must not be null or the empty string. The first component can be a namespace prefix; if present without a schema_ns value, the prefix specifies the namespace. 

		:return: The property's value if the property exists, None otherwise.
		
		.. todo:: Make get_property optionally return keywords describing property's options
		"""
		value = None
		the_prop = _exempi.xmp_string_new()

		if _exempi.xmp_get_property( self.xmpptr, schema_ns, prop_name, the_prop, 0 ): #we're never returning options
			value = _exempi.xmp_string_cstr(the_prop)

		_exempi.xmp_string_free(the_prop)
		return value
		
		
	def get_array_item( self, schema_ns, array_name, item_index ):
		"""
		get_array_item() provides access to items within an array.
		

		Reports whether the item exists; if it does, and if it has a value, the function retrieves the value.; if it doesn't it raises Exception.
		Items are accessed by an integer index, where the first item has index 1.
		
		.. todo:: Make get_array_item optionally return keywords describing array item's options
		"""	
		the_prop = _exempi.xmp_string_new()
		options = c_int32()
		
		if _exempi.xmp_get_array_item( self.xmpptr, schema_ns, array_name, item_index, the_prop, byref(options)): #we're never returning options
			return {_exempi.xmp_string_cstr(the_prop):options.value}
		else:
			raise Exception, "Array's over"
	
	
	# -------------------------------------
	# Functions for setting property values
	# -------------------------------------
	def set_property(self, schema_ns, prop_name, prop_value, **kwargs ):
		"""
		set_property() creates or sets a property value.

		The method takes optional keyword aguments that describe the property. 
		You can use these functions to create empty arrays and structs by setting appropriate option flags. 
		When you assign a value, all levels of a struct that are implicit in the assignment are created if necessary; append_array_item() implicitly creates the named array if necessary.
		
		:param schema_ns:	The namespace URI; see get_property().
		:param prop_name: 	The name of the property. Can be a general path expression, must not be null or the empty string; see get_property() for namespace prefix usage.
		:param **kwargs:	Optional keyword arguments describing the options; must much an already existing option from consts.XMP_PROP_OPTIONS					

		:return True if the property was set correctly, False otherwise.
		"""
		options = options_mask(XMP_PROP_OPTIONS, **kwargs) if kwargs else 0		
		return bool(_exempi.xmp_set_property(self.xmpptr, schema_ns, prop_name, prop_value, options))
		
	def set_array_item( self, schema_ns, array_name, item_index, item_value, **kwargs ):
		"""	
		set_array_item() creates or sets the value of an item within an array.

		Items are accessed by an integer index, where the first item has index 1. T
		This function creates the item if necessary, but the array itself must already exist: use append_array_item() to create arrays. 
		A new item is automatically appended if the index is the array size plus 1; to insert a new item before or after an existing item, use kwargs.

		:param schema_ns:	The namespace URI; see get_property().
		:param array_mame: 	The name of the array. Can be a general path expression, must not be null or the empty string; see get_property() for namespace prefix usage.
		:param item_index: 	The 1-based index of the desired item. 
		:param item_value: 	The new item value, a string, if the array item has a value.
		:param **kwargs: 	Optional keywork arguments describing the array type and insertion location for a new item
		            		The type, if specified, must match the existing array type, prop_array_is_ordered, prop_array_is_alternate, or prop_array_is_alt_text. Default (no keyword parameters) matches the existing array type.		
		:return True if the array item was set correctly, False otherwise.
		:rtype bool
		"""
		options = options_mask(XMP_PROP_OPTIONS, **kwargs) if kwargs else 0
		return bool(_exempi.xmp_set_array_item(self.xmpptr, schema_ns, array_name, item_index, item_value, options))
		
	def append_array_item( self, schema_ns, array_name,  item_value, array_options={}, **kwargs ):
		"""	 
		append_array_item() adds an item to an array, creating the array if necessary.

		This function simplifies construction of an array by not requiring that you pre-create an empty array. T
		The array that is assigned is created automatically if it does not yet exist. If the array exists, it must have the form specified by the options. 
		Each call appends a new item to the array.

		:param schema_ns 	  The namespace URI; see GetProperty().
		:param array_name 	  The name of the array. Can be a general path expression, must not be null or the empty string; see GetProperty() for namespace prefix usage.
		:param item_value 	  The new item value, a null-terminated UTF-8 string, if the array item has a value.
		:param array_options An optional dictionary of keywords from XMP_PROP_OPTIONS describing the array type to create.	
		:param **kwargs	  Optional keyword arguments describing the item type to create.
		:return True if the array item was appended correctly, False otherwise.
		:rtype bool
		"""
		array_options = options_mask(XMP_PROP_OPTIONS, **array_options) if array_options else 0
		options = options_mask(XMP_PROP_OPTIONS, **kwargs) if kwargs else 0
		return bool(_exempi.xmp_append_array_item(self.xmpptr, schema_ns, array_name, array_options, item_value, options))

		
	# -----------------------------------------------
	# Functions accessing properties as binary values
	# -----------------------------------------------
	def get_property_bool(self, schema_ns, prop_name ):
		"""
		get_property_bool is just like get_property(), but it's only to be used to get boolean properties.

		:param schema_ns 	The namespace URI for the property; can be null or the empty string if the first component of the prop_name path contains a namespace prefix.
		:param prop_name 	The name of the property. Can be a general path expression, must not be null or the empty string. The first component can be a namespace prefix; if present without a schema_ns value, the prefix specifies the namespace. 

		:return The property's value if the property exists, None otherwise.
		
		.. todo:: Make get_property_bool optionally return keywords describing property's options
		"""					
		prop_value = c_int()
		_exempi.xmp_get_property_bool(self.xmpptr, schema_ns, prop_name, byref(prop_value), 0 ) #we never return options
		return bool(prop_value.value)
		
	def get_property_int(self, schema_ns, prop_name ):
		"""
		get_property_int is just like get_property(), but it's only to be used to get integer properties.

		:param schema_ns 	The namespace URI for the property; can be null or the empty string if the first component of the prop_name path contains a namespace prefix.
		:param prop_name 	The name of the property. Can be a general path expression, must not be null or the empty string. The first component can be a namespace prefix; if present without a schema_ns value, the prefix specifies the namespace. 
		:return The property's value if the property exists, None otherwise.
		
		.. todo:: Make get_property_int optionally return keywords describing property's options
		"""	
		prop_value =  c_int32()
		_exempi.xmp_get_property_int32(self.xmpptr, schema_ns, prop_name, byref(prop_value), 0 )
		return prop_value.value
		
	def get_property_long(self, schema_ns, prop_name ):
		"""
		get_property_long is just like get_property(), but it's only to be used to get long nteger properties.

		:param schema_ns 	The namespace URI for the property; can be null or the empty string if the first component of the prop_name path contains a namespace prefix.
		:param prop_name 	The name of the property. Can be a general path expression, must not be null or the empty string. The first component can be a namespace prefix; if present without a schema_ns value, the prefix specifies the namespace. 
		:return The property's value if the property exists, None otherwise.
		
		.. todo:: Make get_property_long optionally return keywords describing property's options
		"""		
		prop_value =  c_int64()
		_exempi.xmp_get_property_int64(self.xmpptr, schema_ns, prop_name, byref(prop_value), 0 )
		return prop_value.value
		
	def get_property_float(self, schema_ns, prop_name ):
		"""
		get_property_float is just like get_property(), but it's only to be used to get float properties.

		:param schema_ns 	The namespace URI for the property; can be null or the empty string if the first component of the prop_name path contains a namespace prefix.
		:param prop_name 	The name of the property. Can be a general path expression, must not be null or the empty string. The first component can be a namespace prefix; if present without a schema_ns value, the prefix specifies the namespace. 
		:return The property's value if the property exists, None otherwise.
		
		.. todo:: Make get_property_float optionally return keywords describing property's options
		"""	
		prop_value =  c_float()
		_exempi.xmp_get_property_float(self.xmpptr, schema_ns, prop_name, byref(prop_value), 0 )
		return prop_value.value
		
	def get_property_datetime(self, schema_ns, prop_name ):
		"""
		get_property_date is just like get_property(), but it's only to be used to get datetime properties.
		It returns a standart datetime.datetime instance.

		:param schema_ns 	The namespace URI for the property; can be null or the empty string if the first component of the prop_name path contains a namespace prefix.
		:param prop_name 	The name of the property. Can be a general path expression, must not be null or the empty string. The first component can be a namespace prefix; if present without a schema_ns value, the prefix specifies the namespace. 
		:return The property's value if the property exists, None otherwise.
		
		.. todo:: Make get_property_int optionally return keywords describing property's options
		.. todo:: Ad the tzInfo to the datetime.datetime object
		"""	
		d = _XmpDateTime()
		_exempi.xmp_get_property_date(self.xmpptr, schema_ns, prop_name, byref(d), 0 )
		return datetime.datetime(d.year,d.month,d.day,d.hour,d.minute,d.second)
	
	def get_localized_text(self, schema_ns, alt_text_name, generic_lang, specific_lang, **kwargs ):
		""" 
		get_localized_text() returns information about a selected item in an alt-text array.

		:param schema_ns	The namespace URI for the alt-text array. Has the same usage as in GetProperty.
		:param alt_text_name	The name of the alt-text array. May be a general path expression, must not be null or the empty string. Has the same namespace prefix usage as propName in GetProperty.
		:param generic_lang	The name of the generic language as an RFC 3066 primary subtag. May be null or the empty string if no generic language is wanted.
		:param specific_lang	The name of the specific language as an RFC 3066 tag. Must not be null or the empty string.
		
		:return: The property's value if the property exists, None otherwise.
		"""
		value = None
		value_lang = None
		the_prop = _exempi.xmp_string_new()
		actual_lang = _exempi.xmp_string_new()
		options = c_int32()
		
		if _exempi.xmp_get_localized_text( self.xmpptr, schema_ns, alt_text_name, generic_lang, specific_lang, actual_lang, the_prop, byref(options) ):
			value = _exempi.xmp_string_cstr(the_prop)
			value_lang = _exempi.xmp_string_cstr(actual_lang)

		_exempi.xmp_string_free(the_prop)
		_exempi.xmp_string_free(actual_lang)
			
		return value	
		
	def set_property_bool(self, schema_ns, prop_name, prop_value, **kwargs ):
		"""
		set_property_bool is just like set_property(), but it's only to be used to set boolean properties
		"""
		options = options_mask(XMP_PROP_OPTIONS, **kwargs) if kwargs else 0	
		prop_value = int(prop_value)
		return bool(_exempi.xmp_set_property_bool(self.xmpptr, schema_ns, prop_name, prop_value, options))

	def set_property_int(self, schema_ns, prop_name, prop_value, **kwargs ):
		"""
		set_property_int is just like set_property(), but it's only to be used to set integer properties
		"""
		options = options_mask(XMP_PROP_OPTIONS, **kwargs) if kwargs else 0								
		return bool(_exempi.xmp_set_property_int32(self.xmpptr, schema_ns, prop_name, prop_value,options))
	
	def set_property_long(self, schema_ns, prop_name, prop_value, **kwargs ):
		"""
		set_property_long is just like set_property(), but it's only to be used to set long integer properties
		"""
		options = options_mask(XMP_PROP_OPTIONS, **kwargs) if kwargs else 0	
		return bool(_exempi.xmp_set_property_int64(self.xmpptr, schema_ns, prop_name, prop_value, options))
	
	def set_property_float(self, schema_ns, prop_name, prop_value, **kwargs ):
		"""
		set_property_float is just like set_property(), but it's only to be used to set float properties
		"""
		options = options_mask(XMP_PROP_OPTIONS, **kwargs) if kwargs else 0	
		prop_value = c_float(prop_value)
		return bool(_exempi.xmp_set_property_float(self.xmpptr, schema_ns, prop_name, prop_value, options))
		
	
	def set_property_datetime(self, schema_ns, prop_name, prop_value, **kwargs ):
		"""
		set_property_datetime is just like set_property(), but it's only to be used to set datetime properties
		
		.. todo:: Add tzInfo support
		"""
		options = options_mask(XMP_PROP_OPTIONS, **kwargs) if kwargs else 0		
		d = _XmpDateTime(prop_value.year, prop_value.month, prop_value.day, prop_value.hour, prop_value.minute, prop_value.second,0,0,0)
		return bool(_exempi.xmp_set_property_date(self.xmpptr, schema_ns, prop_name, byref(d), options))
	
	def set_localized_text(self, schema_ns, alt_text_name, generic_lang, specific_lang, prop_value, **kwargs):
		"""
		set_localized_text() creates or sets a localized text value.	
		
		:param schema_ns:	The namespace URI; see get_property().
		:param alt_text_name:	The name of the property. Can be a general path expression, must not be null or the empty string. The first component can be a namespace prefix.
		:param generic_lang:	A valid generic language tag from RFC 3066 specification (i.e. en for English).  Passing "x" for a generic language is allow, but considered poor practice.  An empty string may be specified.
		:param specific_lang:	A specific language tag from RFC 3066 specification (i.e en-US for US English).  
		:param prop_value:	Item value
		:param **kwargs:	Optional keyword arguments describing the options; must much an already existing option from consts.XMP_PROP_OPTIONS					

		:return True if the property was set correctly, False otherwise.
		"""
		options = options_mask(XMP_PROP_OPTIONS, **kwargs) if kwargs else 0
		return bool(_exempi.xmp_set_localized_text(self.xmpptr, schema_ns, alt_text_name, generic_lang, specific_lang, prop_value, options))
	
			
	# ------------------------------------------------
	# Functions for deleting and detecting properties.
	# ------------------------------------------------
	def delete_property(self, schema_ns, prop_name ):
		"""
		delete_property() deletes an XMP subtree rooted at a given property.
		It is not an error if the property does not exist.			
		"""
		_exempi.xmp_delete_property(self.xmpptr, schema_ns, prop_name);
		return None
		
	def does_property_exist(self, schema_ns, prop_name ):
		"""
		does_property_exist() reports whether a property currently exists.

		:param schema_ns	The namespace URI for the property; see get_property().
		:param prop_name 	The name of the property; see get_property().

		:return True if the property exists, False otherwise.	
		"""
		return bool(_exempi.xmp_has_property(self.xmpptr, schema_ns, prop_name))
		
	def does_array_item_exist(self, schema_ns, array_name, item ):
		""" 
		does_array_item_exist() reports whether an array's item currently exists.

		:return: True if item is in array, False otherwise
		:rtype: bool
		"""
		index = 0
		
		the_prop = _exempi.xmp_string_new()
		
		while( True ):
			if _exempi.xmp_get_array_item( self.xmpptr, str(schema_ns), str(array_name), index+1, the_prop, None):
				index += 1
			else:
				break
		
		return index

	# -------------------------------------
	# Functions for parsing and serializing
	# -------------------------------------
	# These functions support parsing serialized RDF into an XMP object, and serailizing an XMP object into RDF. 
	# Serialization is always as UTF-8. 
	def parse_from_str( self, xmp_packet_str, xmpmeta_wrap = False, input_encoding = None ):
		"""
		Parses RDF from a string into a XMP object. The input for parsing may be any valid 
		Unicode encoding. ISO Latin-1 is also recognized, but its use is strongly discouraged.
		
		Note RDF string must contain an outermost <x:xmpmeta> object.
		
		:param xmp_packet_str: String to parse.
		:param xmpmeta_wrap: Optional - If True, the string will be wrapped in an <x:xmpmeta> element.
		:param input_encoding: Optional - If `xmp_packet_str` is a 8-bit string, it will by default be assumed to be UTF-8 encoded.
		:return:  true if :class:`libxmp.core.XMPMeta` object can be written in file.
		:rtype: bool
		"""
		xmp_packet_str = _encode_as_utf8( xmp_packet_str, input_encoding )
		
		if xmpmeta_wrap:
			xmp_packet_str = "<x:xmpmeta xmlns:x='adobe:ns:meta/'>%s</x:xmpmeta>" % xmp_packet_str
		
		l = len(xmp_packet_str)
		res = _exempi.xmp_parse(self.xmpptr, xmp_packet_str, l )
		_check_for_error()
		return res		
		
	def serialize_and_format( self, padding=0, newlinechr='\n', tabchr = '\t', indent=0, **kwargs ):
		"""
		Serializes an XMPMeta object into a string as RDF. Note, normally it is sufficient to use either
		`serialize_to_str` or `serialize_to_unicode` unless you need high degree of control over the serialization.
		
		The specified parameters must be logically consistent, an exception is raised if not. You cannot specify 
		both `omit_packet_wrapper` along with `read_only_packet`, `include_thumbnail_pad`, or `exact_packet_length`.
		
		:param padding: The number of bytes of padding, useful for modifying embedded XMP in place.
		:param newlinechr: The new line character to use.
		:param tabchr: The indentation character to use.
		:param indent: The initial indentation level.
		:param omit_packet_wrapper: Do not include an XML packet wrapper.
		:param read_only_packet: Create a read-only XML packet wapper.
		:param use_compact_format: Use a highly compact RDF syntax and layout.
		:param include_thumbnail_pad: Include typical space for a JPEG thumbnail in the padding if no xmp:Thumbnails property is present.
		:param exact_packet_length: The padding parameter provides the overall packet length.
		:param write_alias_comments: Include XML comments for aliases.
		:param omit_all_formatting: Omit all formatting whitespace.
		:return: XMPMeta object serialized into a string as RDF.
		:rtype: `unicode` string.
		"""
		res_str = None
		
		# Ensure padding is an int.
		padding = int(padding)
		indent = int(indent)	
		tabchr = str(tabchr)	
		newlinechr = str(newlinechr)
		
		# Define options bitmask
		options = options_mask( XMP_SERIAL_OPTIONS, **kwargs )
		
		# Serialize
		xmpstring = _XMPString()
		res = _exempi.xmp_serialize_and_format( self.xmpptr, xmpstring.ptr, options, padding, newlinechr, tabchr, indent )
		_check_for_error()
		
		# Get string
		if res:
			res_str = xmpstring.__str__()
			
		del xmpstring
		return res_str

	
	def serialize_to_unicode( self, **kwargs ):
		"""
		Serializes an XMPMeta object into a Unicode string as RDF and format. Note, this is 
		wrapper around `serialize_to_str`.
		
		The specified parameters must be logically consistent, an exception is raised if not. You cannot specify 
		both `omit_packet_wrapper` along with `read_only_packet`, `include_thumbnail_pad`, or `exact_packet_length`.
		
		:param padding: The number of bytes of padding, useful for modifying embedded XMP in place.
		:param omit_packet_wrapper: Do not include an XML packet wrapper.
		:param read_only_packet: Create a read-only XML packet wapper.
		:param use_compact_format: Use a highly compact RDF syntax and layout.
		:param include_thumbnail_pad: Include typical space for a JPEG thumbnail in the padding if no xmp:Thumbnails property is present.
		:param exact_packet_length: The padding parameter provides the overall packet length.
		:param write_alias_comments: Include XML comments for aliases.
		:param omit_all_formatting: Omit all formatting whitespace.
		:return: XMPMeta object serialized into a string as RDF.
		:rtype: `unicode` string.
		"""
		tmp =  self.serialize_to_str( **kwargs )
		
		return (tmp.decode('utf-8') if tmp else None)
		
		
	def serialize_to_str( self, padding = 0, **kwargs ):
		"""
		Serializes an XMPMeta object into a string (8-bit, UTF-8 encoded) as RDF and format. 
		
		:param padding: The number of bytes of padding, useful for modifying embedded XMP in place.
		:param omit_packet_wrapper: Do not include an XML packet wrapper.
		:param read_only_packet: Create a read-only XML packet wapper.
		:param use_compact_format: Use a highly compact RDF syntax and layout.
		:param include_thumbnail_pad: Include typical space for a JPEG thumbnail in the padding if no xmp:Thumbnails property is present.
		:param exact_packet_length: The padding parameter provides the overall packet length.
		:param write_alias_comments: Include XML comments for aliases.
		:param omit_all_formatting: Omit all formatting whitespace.
		:return: XMPMeta object serialized into a string as RDF.
		:rtype: `str` 8-bit string in UTF-8 encoding (ready to e.g. be writtin to a file).
		"""
		res_str = None
		
		# Ensure padding is an int.
		padding = int(padding)		

		# Define options bitmask
		options = options_mask( XMP_SERIAL_OPTIONS, **kwargs )
		
		# Serialize
		xmpstring = _XMPString()
		res = _exempi.xmp_serialize( self.xmpptr, xmpstring.ptr, options, padding )
		_check_for_error()
		
		# Get string
		if res:
			res_str = xmpstring.__str__()
			
		del xmpstring
		return res_str
		
	
	# -------------------------------------
	# Misceallaneous functions
	# -------------------------------------
	def clone( self ):
		"""
		Create a new XMP packet from this one.
		"""
		newptr = _exempi.xmp_copy( self.xmpptr )
		
		return (XMPMeta( _xmp_internal_ref = newptr ) if newptr else None)
		

	def count_array_items( self, schema_ns, array_name ):
		""" 
		count_array_items returns the number of a given array's items
		"""
		index = 0
		
		the_prop = _exempi.xmp_string_new()
		
		while( True ):
			if _exempi.xmp_get_array_item( self.xmpptr, str(schema_ns), str(array_name), index+1, the_prop, None):
				index += 1
			else:
				break
		
		return index
			
	# -------------------------------------
	# Namespace Functions
	# -------------------------------------
	@staticmethod
	def get_prefix_for_namespace(namespace):
		"""		
		Check if a namespace is registered.
		
		Parameters:
		namespace: the namespace to check.

 		Returns the associated prefix if registered, None if the namespace is not registered
		"""
		associated_prefix = _exempi.xmp_string_new()
		if _exempi.xmp_namespace_prefix(namespace, associated_prefix):
			return _exempi.xmp_string_cstr(associated_prefix)
		else:
			return None

	@staticmethod
	def get_namespace_for_prefix(prefix):
		"""
		Checks if a prefix is registered.
		Parameters:
		prefix: the prefix to check.

 		Returns the associated namespace if registered, None if the prefix is not registered
		"""
		associated_namespace = _exempi.xmp_string_new()
		if _exempi.xmp_prefix_namespace_uri(prefix, associated_namespace):
			return _exempi.xmp_string_cstr(associated_namespace)
		else:
			return None
	
	@staticmethod
	def register_namespace( namespace_uri, suggested_prefix ):
		"""
		Register a new namespace to save properties to.
		
		Parameters:
		namespace_uri: the new namespace's URI
		suggested prefix: the suggested prefix: note that is NOT guaranteed it'll be the actual namespace's prefix
		
		Returns the actual registered prefix for the namespace of None if the namespace wasn't created.
		"""


		registered_prefix = _exempi.xmp_string_new()
		if _exempi.xmp_register_namespace(namespace_uri, suggested_prefix, registered_prefix):
			return _exempi.xmp_string_cstr(registered_prefix)
		else:
			return None
		
	
	
class XMPIterator:
	"""
	XMPIterator provides a uniform means to iterate over the schema and properties within an XMP object. 
	It's implemented according to Python's iterator protocol and it's the iterator for XMPMeta class.
	:param  xmp_obj  : an XMPMeta instance
	:param  schema_ns: Optional namespace URI to restrict the iteration.
	:param  prop_name: Optional property name to restrict the iteration.
	:param **kwargs : Optional keyword arguments from XMP_ITERATOR_OPTIONS
	:returns: an iterator for the given xmp_obj
	"""
	def __init__( self, xmp_obj, schema_ns=None, prop_name=None, **kwargs ):
		self.options = options_mask(consts.XMP_ITERATOR_OPTIONS, **kwargs) if kwargs else 0
		self.xmpiteratorptr = _exempi.xmp_iterator_new( xmp_obj.xmpptr, schema_ns, prop_name, self.options)
		_check_for_error()
		self.schema = schema_ns
		self.prop_name = prop_name
		
	def __del__(self):
		_check_for_error()

		
	def __iter__(self):
		return self
		
	def next(self):		
		prop_value = _XMPString()
		the_value = None
		
		schema_ns = _XMPString()
		prop_name = _XMPString()
		
		options = c_int32(self.options)
			
		if _exempi.xmp_iterator_next(self.xmpiteratorptr, schema_ns.get_ptr(), prop_name.get_ptr(), prop_value.get_ptr(), 
byref(options)):
			#decode option bits into a human-readable format (that is, a dict)
			opts = {
				'VALUE_IS_URI' : False,
				'IS_QUALIFIER' : False,
				'HAS_QUALIFIERS' : False,
				'HAS_LANG' : False,
				'HAS_TYPE' : False,
				'VALUE_IS_STRUCT' : False,
				'VALUE_IS_ARRAY' : False,
				'ARRAY_IS_ORDERED' : False,
				'ARRAY_IS_ALT' : False,
				'ARRAY_IS_ALTTEXT' : False,
				'IS_ALIAS' : False,
				'HAS_ALIASES' : False,
				'IS_INTERNAL' : False, 
				'IS_STABLE' : False,
				'IS_DERIVED' : False,
				'IS_SCHEMA' : False,
			}
			
			for opt in opts:
				if has_option(options.value, getattr(consts,'XMP_PROP_'+opt)):
					opts[opt] = True
			
			return (unicode(schema_ns),unicode(prop_name),unicode(prop_value), opts)
		else:
			raise StopIteration
				
	def skip(**kwargs ):
		"""
		skip() skips some portion of the remaining iterations.
		
		:param **kwargs: Optional keyword parameters from XMP_SKIP_OPTIONS to control the iteration
		:returns: None
		:rtype: NoneType
		"""
		options = options_mask(consts.XMP_SKIP_OPTIONS, **kwargs) if kwargs else 0
		_exempi.xmp_iterator_skip( self.xmpiteratorptr, options );
		_check_for_error()
		return None
