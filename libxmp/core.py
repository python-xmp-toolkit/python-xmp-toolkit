# -*- coding: utf-8 -*-
#
# Copyright (c) 2008-2009, European Space Agency & European Southern Observatory (ESA/ESO)
# Copyright (c) 2008, CRS4 - Centre for Advanced Studies, Research and Development in Sardinia
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
A component for parsing, manipulating, and serializing XMP data. The core package has 
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
	""" """
	
	def __init__( self, **kwargs ):
		"""
		@param xmp_str Optional.
		@param xmp_internal_ref Optional - used for internal purposes.
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
		Ensure memory is deallocated when destroying object.
		"""
		if self.xmpptr != None:
			if not _exempi.xmp_free(self.xmpptr):
				_check_for_error()
		
		if self.iterator is not None:
			del self.iterator
			
		_exempi.xmp_terminate()
	
	def __iter__(self):
		if self.iterator is None:
			self.iterator = XMPIterator(self)
		
		return self.iterator
		
	def __repr__(self):
		"""
		Prints the serialization of the XMPMeta object.
		"""
		return self.serialize_to_str()
		
	def __eq__(self, other):
		""" Check if two XMPMeta object are equal. """
		return self.xmpptr == other.xmpptr
		
	def __ne__(self, other):
		""" Check if two XMPMeta object are not equal. """
		return self.xmpptr != other.xmpptr
	
	# -------------------------------------
	# Initialization and termination
	# -------------------------------------
	@staticmethod
	def initialize( options = None ):
		"""
		Initialize library. Must be called before anything else.
		
		@param options Not implemented - provided for future implementations.
		"""
		if not _exempi.xmp_init():
			_check_for_error()
	
			
	# -------------------------------------
	# Global option flags
	# -------------------------------------
	@staticmethod
	def get_global_options():
		""" 
		Not Implemented - Exempi does not implement this function yet
		"""
		raise NotImplementedError("Exempi does not implement this function yet")

	def set_global_options(self, options):
		""" 
		Not Implemented - Exempi does not implement this function yet
		"""
		raise NotImplementedError("Exempi does not implement this function yet")

	@staticmethod
	def get_version_info():
		""" 
		Not Implemented - Exempi does not implement this function yet
		"""
		raise NotImplementedError("Exempi does not implement this function yet")

	# -------------------------------------
	# Functions for getting property values
	# -------------------------------------
	def get_property(self, schema_ns, prop_name ):
		"""	 """
		#/** Get an XMP property and its option bits from the XMP packet
		# * @param xmp the XMP packet
		# * @param schema
		# * @param name
		# * @param property the allocated XmpStringPtr
		# * @param propsBits pointer to the option bits. Pass NULL if not needed
		# * @return true if found
		# */
		#bool xmp_get_property(XmpPtr xmp, const char *schema, 
		#					  const char *name, XmpStringPtr property,
		#					  uint32_t *propsBits);
		value = None
		the_prop = _exempi.xmp_string_new()

		if _exempi.xmp_get_property( self.xmpptr, schema_ns, prop_name, the_prop, 0 ):
			value = _exempi.xmp_string_cstr(the_prop)

		_exempi.xmp_string_free(the_prop)
		return value
		
		
	def get_array_item( self, schema_ns, array_name, item_index ):
		"""	 """
		#/** Get an item from an array property
		# * @param xmp the xmp meta
		# * @param schema the schema
		# * @param name the property name
		# * @param index the index in the array
		# * @param property the property value
		# * @param propsBits the property bits. Pass NULL is unwanted.
		# * @return TRUE if success.
		# */
		#bool xmp_get_array_item(XmpPtr xmp, const char *schema, 
		#						const char *name, int32_t index, XmpStringPtr property,
		#						uint32_t *propsBits);
		# CHANGED: implemented get_array_item
		
		the_prop = _exempi.xmp_string_new()
		options = c_int32()
		
		if _exempi.xmp_get_array_item( self.xmpptr, schema_ns, array_name, item_index, the_prop, byref(options)):
			return {_exempi.xmp_string_cstr(the_prop):options.value}
		else:
			raise Exception, "Array's over"
	
	def get_struct_field( self, schema_ns, struct_name, field_ns, field_name ):
		""" 
		Not Implemented - Exempi does not implement this function yet
		"""
		raise NotImplementedError("Exempi does not implement this function yet")
		
	def get_qualifier( self, schema_ns, prop_name, qual_ns, qual_name ):
		""" 
		Not Implemented - Exempi does not implement this function yet
		"""
		raise NotImplementedError("Exempi does not implement this function yet")
		
	# -------------------------------------
	# Functions for setting property values
	# -------------------------------------
	def set_property(self, schema_ns, prop_name, prop_value, options = 0 ):
		"""	 """
		#/** Set an XMP property in the XMP packet
		# * @param xmp the XMP packet
		# * @param schema
		# * @param name
		# * @param value 0 terminated string
		# * @param optionBits
		# * @return false if failure
		# */
		#bool xmp_set_property(XmpPtr xmp, const char *schema, 
		#					  const char *name, const char *value,
		#					  uint32_t optionBits);
		
		return bool(_exempi.xmp_set_property(self.xmpptr, schema_ns, prop_name, prop_value, 0))
		
	def set_array_item( self, schema_ns, array_name, item_index, item_value, options = 0 ):
		"""	 """
		#bool xmp_set_array_item(XmpPtr xmp, const char *schema, 
		#						const char *name, int32_t index, const char *value,
		#						uint32_t optionBits);
		return bool(_exempi.xmp_set_array_item(self.xmpptr, schema_ns, array_name, item_index, item_value, options))
		
	def append_array_item( self, schema_ns, array_name, array_options, item_value, options = 0 ):
		"""	 """
		#/** Append a value to the XMP Property array in the XMP Packet provided
		# * @param xmp the XMP packet
		# * @param schema the schema of the property
		# * @param name the name of the property
		# * @param arrayOptions option bits of the parent array
		# * @param value null-terminated string
		# * @param optionBits option bits of the value itself.
		# */
		#bool xmp_append_array_item(XmpPtr xmp, const char *schema, const char *name,
		#						   uint32_t arrayOptions, const char *value,
		#						   uint32_t optionBits);
		return bool(_exempi.xmp_append_array_item(self.xmpptr, schema_ns, array_name, item_value, options))
				
		
	
	def set_struct_field( self, schema_ns, struct_name, field_ns, field_name, field_value, options = 0 ):
		""" 
		Not Implemented - Exempi does not implement this function yet
		"""
		raise NotImplementedError("Exempi does not implement this function yet")
		
	def set_qualifier( self, schema_ns, prop_name, qual_ns, qual_name, qual_value, options = 0 ):
		""" 
		Not Implemented - Exempi does not implement this function yet
		"""
		raise NotImplementedError("Exempi does not implement this function yet")
		
	# -----------------------------------------------
	# Functions accessing properties as binary values
	# -----------------------------------------------
	def get_property_bool(self, schema_ns, prop_name ):
		"""	 """
		#bool xmp_get_property_bool(XmpPtr xmp, const char *schema, 
		#							const char *name, bool * property,
		#							uint32_t *propsBits);
		prop_value = c_int()
		_exempi.xmp_get_property_bool(self.xmpptr, schema_ns, prop_name, byref(prop_value), 0 )
		return bool(prop_value.value)
		
	def get_property_int(self, schema_ns, prop_name ):
		"""	 """
		#bool xmp_get_property_int32(XmpPtr xmp, const char *schema, 
		#							const char *name, int32_t * property,
		#							uint32_t *propsBits);

		prop_value =  c_int32()
		_exempi.xmp_get_property_int32(self.xmpptr, schema_ns, prop_name, byref(prop_value), 0 )
		return prop_value.value
		
	def get_property_long(self, schema_ns, prop_name ):
		"""	 """
		#bool xmp_get_property_int64(XmpPtr xmp, const char *schema, 
		#							const char *name, int64_t * property,
		#							uint32_t *propsBits);
		
		prop_value =  c_int64()
		_exempi.xmp_get_property_int64(self.xmpptr, schema_ns, prop_name, byref(prop_value), 0 )
		return prop_value.value
		
	def get_property_float(self, schema_ns, prop_name ):
		"""	 """
		#bool xmp_get_property_float(XmpPtr xmp, const char *schema, 
		#							const char *name, double * property,
		#							uint32_t *propsBits);

		prop_value =  c_float()
		_exempi.xmp_get_property_float(self.xmpptr, schema_ns, prop_name, byref(prop_value), 0 )
		return prop_value.value
		
	def get_property_datetime(self, schema_ns, prop_name ):
		"""	 """
		#bool xmp_get_property_date(XmpPtr xmp, const char *schema, 
		#						   const char *name, XmpDateTime * property,
		#						   uint32_t *propsBits);
		
		d = _XmpDateTime()
		_exempi.xmp_get_property_date(self.xmpptr, schema_ns, prop_name, byref(d), 0 )
		return datetime.datetime(d.year,d.month,d.day,d.hour,d.minute,d.second) #TODO: add the tzInfo stuff
		
	def set_property_bool(self, schema_ns, prop_name, prop_value, options = 0 ):
		"""	 """
		#bool xmp_set_property_bool(XmpPtr xmp, const char *schema, 
		#							const char *name, bool value,
		#							uint32_t optionBits);
		prop_value = int(prop_value)
		return bool(_exempi.xmp_set_property_bool(self.xmpptr, schema_ns, prop_name, prop_value,0))

	def set_property_int(self, schema_ns, prop_name, prop_value, options = 0 ):
		"""	 """
		#bool xmp_set_property_int32(XmpPtr xmp, const char *schema, 
		#							const char *name, int32_t value,
		#							uint32_t optionBits);
		return bool(_exempi.xmp_set_property_int32(self.xmpptr, schema_ns, prop_name, prop_value,0))
	
	def set_property_long(self, schema_ns, prop_name, prop_value, options = 0 ):
		"""	 """
		#bool xmp_set_property_int64(XmpPtr xmp, const char *schema, 
		#							const char *name, int64_t value,
		#							uint32_t optionBits);
		return bool(_exempi.xmp_set_property_int64(self.xmpptr, schema_ns, prop_name, prop_value,0))
	
	def set_property_float(self, schema_ns, prop_name, prop_value, options = 0 ):
		"""	 """
		# Set a float XMP property in the XMP packet
		# @param xmp the XMP packet
		# @param schema_ns the schema namespace's URI
		# @param prop_name the property name
		# @param value the float value
		# @param options a bitmask representing options
		# @return False if failure, True otherwise
		#
		prop_value = c_float(prop_value)
		return bool(_exempi.xmp_set_property_float(self.xmpptr, schema_ns, prop_name, prop_value,0))
		
	
	def set_property_datetime(self, schema_ns, prop_name, prop_value, options = 0 ):
		"""	 """
		#/** Set a date XMP property in the XMP packet
		# * @param xmp the XMP packet
		# * @param schema
		# * @param name
		# * @param value the date-time struct
		# * @param optionBits
		# * @return false if failure
		# */
		#bool xmp_set_property_date(XmpPtr xmp, const char *schema, 
		#						   const char *name, const XmpDateTime *value,
		#						   uint32_t optionBits);
		
		#TODO: add the tzInfo stuff on the object below
		
		d = _XmpDateTime(prop_value.year, prop_value.month, prop_value.day, prop_value.hour, prop_value.minute, prop_value.second,0,0,0)
		return bool(_exempi.xmp_set_property_date(self.xmpptr, schema_ns, prop_name, byref(d), 0))
		
	# ------------------------------------------------------------
	# Functions for accessing localized text (alt-text) properties
	# ------------------------------------------------------------
	def get_localized_text( self, schema_ns, alt_text_name, generic_lang, specific_lang ):
		#/** Get a localised text from a localisable property.
		# * @param xmp the XMP packet
		# * @param schema the schema
		# * @param name the property name.
		# * @param genericLang the generic language you may want as a fall back. 
		# * Can be NULL or empty.
		# * @param specificLang the specific language you want. Can't be NULL or empty.
		# * @param actualLang the actual language of the value. Can be NULL if 
		# * not wanted.
		# * @param itemValue the localized value. Can be NULL if not wanted.
		# * @param propBits the options flags describing the property. Can be NULL.
		# * @return true if found, false otherwise.
		# */
		#bool xmp_get_localized_text(XmpPtr xmp, const char *schema, const char *name,
		#				const char *genericLang, const char *specificLang,
		#				XmpStringPtr actualLang, XmpStringPtr itemValue,
		#				uint32_t *propBits);
		raise NotImplementedError #TODO: implement

	def set_localized_text( self, schema_ns, alt_text_name, generic_lang, specific_lang, item_value, options = 0 ):
		#/** Set a localised text in a localisable property.
		# * @param xmp the XMP packet
		# * @param schema the schema
		# * @param name the property name.
		# * @param genericLang the generic language you may want to set too. 
		# * Can be NULL or empty.
		# * @param specificLang the specific language you want. Can't be NULL or empty.
		# * @param value the localized value. Cannot be NULL.
		# * @param optionBits the options flags describing the property.
		# * @return true if set, false otherwise.
		# */
		#bool xmp_set_localized_text(XmpPtr xmp, const char *schema, const char *name,
		#							const char *genericLang, const char *specificLang,
		#							const char *value, uint32_t optionBits);
		raise NotImplementedError #TODO: implement
		
	def delete_localized_text( self, schema_ns, alt_text_name, generic_lang, specific_lang ):
		#bool xmp_delete_localized_text(XmpPtr xmp, const char *schema,
		#							   const char *name, const char *genericLang,
		#							   const char *specificLang);
		raise NotImplementedError #TODO: implement
			
	# ------------------------------------------------
	# Functions for deleting and detecting properties.
	# ------------------------------------------------
	def delete_property(self, schema_ns, prop_name ):
		"""	 """
		#/** Delete a property from the XMP Packet provided
		# * @param xmp the XMP packet
		# * @param schema the schema of the property
		# * @param name the name of the property
		# */
		_exempi.xmp_delete_property(self.xmpptr, schema_ns, prop_name);

	def delete_array_item( self, schema_ns, array_name, item_index ):
		""" 
		Not Implemented - Exempi does not implement this function yet
		"""
		raise NotImplementedError("Exempi does not implement this function yet")

	def delete_struct_field( self, schema_ns, struct_name, field_ns, field_name ):
		""" 
		Not Implemented - Exempi does not implement this function yet
		"""
		raise NotImplementedError("Exempi does not implement this function yet")

	def delete_qualifier( self, schema_ns, prop_name, qual_ns, qual_name ):
		""" 
		Not Implemented - Exempi does not implement this function yet
		"""
		raise NotImplementedError("Exempi does not implement this function yet")
		
	def does_property_exist(self, schema_ns, prop_name ):
		"""	 """
		#/** Determines if a property exists in the XMP Packet provided
		# * @param xmp the XMP packet
		# * @param schema the schema of the property. Can't be NULL or empty.
		# * @param name the name of the property. Can't be NULL or empty.
		# * @return true is the property exists
		# */
		#bool xmp_has_property(XmpPtr xmp, const char *schema, const char *name);
		return bool(_exempi.xmp_has_property(xmp.xmpptr, schema_ns, prop_name))
		
	def does_array_item_exist(self, schema_ns, array_name, item ):
		""" 
		Returns True if item is in array, False otherwise
		Implemented in pure Python - Exempi does not implement this function yet
		"""
		#CHANGED: Implemented in Python!
		

		index = 0
		
		the_prop = _exempi.xmp_string_new()
		
		while( True ):
			if _exempi.xmp_get_array_item( self.xmpptr, str(schema_ns), str(array_name), index+1, the_prop, None):
				index += 1
			else:
				break
		
		return index
		
	def does_struct_field_exist(self, schema_ns, struct_name, field_ns, field_name ):
		""" 
		Not Implemented - Exempi does not implement this function yet
		"""
		raise NotImplementedError("Exempi does not implement this function yet")

	def does_qualifier_exist(self, schema_ns, prop_name, qual_ns, qual_name ):
		""" 
		Not Implemented - Exempi does not implement this function yet
		"""
		raise NotImplementedError("Exempi does not implement this function yet")

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
		
		return (XMPMeta( internal_ref = newptr ) if newptr else None)
		

	def count_array_items( self, schema_ns, array_name ):
		""" 
		Counts the number of a given array's items
		Implemented in pure Python - Exempi does not implement this function yet
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
		@param namespace: the namespace to check.

 		Return the associated prefix if registered, None if the namespace is not registered
		"""
		associated_prefix = _exempi.xmp_string_new()
		if _exempi.xmp_namespace_prefix(namespace, associated_prefix):
			return _exempi.xmp_string_cstr(associated_prefix)
		else:
			return None

	@staticmethod
	def get_namespace_for_prefix(prefix):
		"""
		Check if a prefix is registered.
		@param prefix: the prefix to check.

 		Return the associated namespace if registered, None if the prefix is not registered
		"""
		associated_namespace = _exempi.xmp_string_new()
		if _exempi.xmp_prefix_namespace_uri(prefix, associated_namespace):
			return _exempi.xmp_string_cstr(associated_namespace)
		else:
			return None
	
	@staticmethod
	def register_namespace( namespace_uri, suggested_prefix ):
		# Register a new namespace to add properties to
		# This is done automatically when reading the metadata block
		# @param namespaceURI the namespace URI to register
		# @param suggestedPrefix the suggested prefix
		# @param registeredPrefix the really registered prefix. Not necessarily
		# %suggestedPrefix. 
		# @return the registered prefix (which is NOT necessarily suggsted_prefix if success, 
		# None otherwise.

		registered_prefix = _exempi.xmp_string_new()
		if _exempi.xmp_register_namespace(namespace_uri, suggested_prefix, registered_prefix):
			return _exempi.xmp_string_cstr(registered_prefix)
		else:
			return None

	@staticmethod
	def get_namespace_prefix( namespace_uri ):
		""" 
		Not Implemented - Exempi does not implement this function yet
		"""
		raise NotImplementedError("Exempi does not implement this function yet")

	@staticmethod
	def get_namespace_uri( namespace_prefix ):
		""" 
		Not Implemented - Exempi does not implement this function yet
		"""
		raise NotImplementedError("Exempi does not implement this function yet")
		
	@staticmethod
	def delete_namespace( namespace_uri):
		""" 
		Not Implemented - Exempi does not implement this function yet
		"""
		raise NotImplementedError("Exempi does not implement this function yet")
		
	# -------------------------------------
	# Alias Functions
	# -------------------------------------
	@staticmethod
	def register_alias( alias_ns, alias_prop, actual_ns, actual_prop, array_form = None ):
		""" 
		Not Implemented - Exempi does not implement this function yet
		"""
		raise NotImplementedError("Exempi does not implement this function yet")

	@staticmethod
	def resolve_alias( alias_ns, alias_prop ):
		""" 
		Not Implemented - Exempi does not implement this function yet
		"""
		raise NotImplementedError("Exempi does not implement this function yet")

	@staticmethod
	def delete_alias( alias_ns, alias_prop ):
		""" 
		Not Implemented - Exempi does not implement this function yet
		"""
		raise NotImplementedError("Exempi does not implement this function yet")

	@staticmethod
	def register_standard_alias( schema_ns ):
		""" 
		Not Implemented - Exempi does not implement this function yet
		"""
		raise NotImplementedError("Exempi does not implement this function yet")
	
	
class XMPIterator:
	def __init__( self, xmp_obj, schema_ns=None, prop_name=None, options = 0 ):
		self.xmpiteratorptr = _exempi.xmp_iterator_new( xmp_obj.xmpptr, schema_ns, prop_name, options)
		_check_for_error()
		self.schema = schema_ns
		self.prop_name = prop_name
		self.options = options
		
		
	def __del__(self):
		#_exempi.xmp_iterator_free(self.xmpiteratorptr)
		_check_for_error()

		
	def __iter__(self):
		return self
		
	def next(self):		
		prop_value = _XMPString()
		the_value = None
		
		schema_ns = _XMPString()
		prop_name = _XMPString()
		
		options = c_uint32()
			
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
				
	def skip( options ):
		# TODO: define options
		_exempi.xmp_iterator_skip( self.xmpiteratorptr, options );
		_check_for_error()
