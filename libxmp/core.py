# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, European Space Agency & European Southern Observatory (ESA/ESO)
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

"""
A component for parsing, manipulating, and serializing XMP data. The core package has 
no knowledge of files. The core API is provided by the :class:`XMPMeta`, :class:`XMPIterator`, and 
:class:`XMPUtils` classes.
"""

from ctypes import *
import datetime

from libxmp import XMPError
from libxmp import _exempi, _XMP_ERROR_CODES, _check_for_error

__all__ = ['XMPMeta','XMPIterator','XMPUtils']

def _xmp_string_new():
	# TODO: check
	return _exempi.xmp_string_new()

def _xmp_string_free(xmpstr):
	# TODO: check
	return _exempi.xmp_string_free(xmpstr)

def _xmp_string_to_str(xmpstr):
	# Note the string returned belongs to the object
	# in C++
	# TODO: check
	return _exempi.xmp_string_cstr(xmpstr)


class _XmpDateTime(Structure):
	
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


class XMPMeta:
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
		
	def __del__(self):
		"""
		Ensure memory is deallocated when destroying object.
		"""
		if self.xmpptr != None:
			if not _exempi.xmp_free(self.xmpptr):
				_check_for_error()
		
	def _get_internal_ref(self):
		"""
		Method used for internal purpose - XMPFiles need access to the internal
		representation of the XMPMeta instance.
		"""
		return  self.xmpptr
	internal_ref = property( _get_internal_ref )

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
	
	@staticmethod
	def terminate():
		"""
		After the library is no more needed, call this function.
		"""
		_exempi.xmp_terminate()
			
	# -------------------------------------
	# Global option flags
	# -------------------------------------
	@staticmethod
	def get_global_options():
		""" 
		Not Implemented - Exempi does not implement this function yet
		"""
		raise NotImplementedError

	def set_global_options(self, options):
		""" 
		Not Implemented - Exempi does not implement this function yet
		"""
		raise NotImplementedError

	@staticmethod
	def get_version_info():
		""" 
		Not Implemented - Exempi does not implement this function yet
		"""
		raise NotImplementedError

	# -------------------------------------
	# Functions for getting property values
	# -------------------------------------
	def get_property(self, schema_ns, prop_name ):
		"""  """
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
		"""  """
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
		raise NotImplementedError
	
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
		"""  """
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
		"""  """
		#bool xmp_set_array_item(XmpPtr xmp, const char *schema, 
		#						const char *name, int32_t index, const char *value,
		#						uint32_t optionBits);
		raise NotImplementedError
		
	def append_array_item( self, schema_ns, array_name, array_options, item_value, options = 0 ):
		"""  """
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
		raise NotImplementedError
	
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
		"""  """
		#bool xmp_get_property_bool(XmpPtr xmp, const char *schema, 
		#							const char *name, bool * property,
		#							uint32_t *propsBits);
		prop_value = c_int()
		_exempi.xmp_get_property_bool(self.xmpptr, schema_ns, prop_name, byref(prop_value), 0 )
		return bool(prop_value.value)
		
	def get_property_int(self, schema_ns, prop_name ):
		"""  """
		#bool xmp_get_property_int32(XmpPtr xmp, const char *schema, 
		#							const char *name, int32_t * property,
		#							uint32_t *propsBits);

		prop_value =  c_int32()
		_exempi.xmp_get_property_int32(self.xmpptr, schema_ns, prop_name, byref(prop_value), 0 )
		return prop_value.value
		
	def get_property_long(self, schema_ns, prop_name ):
		"""  """
		#bool xmp_get_property_int64(XmpPtr xmp, const char *schema, 
		#							const char *name, int64_t * property,
		#							uint32_t *propsBits);
		
		prop_value =  c_int64()
		_exempi.xmp_get_property_int64(self.xmpptr, schema_ns, prop_name, byref(prop_value), 0 )
		return prop_value.value
		
	def get_property_float(self, schema_ns, prop_name ):
		"""  """
		#bool xmp_get_property_float(XmpPtr xmp, const char *schema, 
		#							const char *name, double * property,
		#							uint32_t *propsBits);

		prop_value =  c_float()
		_exempi.xmp_get_property_float(self.xmpptr, schema_ns, prop_name, byref(prop_value), 0 )
		return prop_value.value
		
	def get_property_datetime(self, schema_ns, prop_name ):
		"""  """
		#bool xmp_get_property_date(XmpPtr xmp, const char *schema, 
		#						   const char *name, XmpDateTime * property,
		#						   uint32_t *propsBits);
		
		d = _XmpDateTime()
		_exempi.xmp_get_property_date(self.xmpptr, schema_ns, prop_name, byref(d), 0 )
		return datetime.datetime(d.year,d.month,d.day,d.hour,d.minute,d.second) #TODO: add the tzInfo stuff
		
	def set_property_bool(self, schema_ns, prop_name, prop_value, options = 0 ):
		"""  """
		#bool xmp_set_property_bool(XmpPtr xmp, const char *schema, 
		#							const char *name, bool value,
		#							uint32_t optionBits);
		prop_value = int(prop_value)
		return bool(_exempi.xmp_set_property_bool(self.xmpptr, schema_ns, prop_name, prop_value,0))

	def set_property_int(self, schema_ns, prop_name, prop_value, options = 0 ):
		"""  """
		#bool xmp_set_property_int32(XmpPtr xmp, const char *schema, 
		#							const char *name, int32_t value,
		#							uint32_t optionBits);
		return bool(_exempi.xmp_set_property_int32(self.xmpptr, schema_ns, prop_name, prop_value,0))
	
	def set_property_long(self, schema_ns, prop_name, prop_value, options = 0 ):
		"""  """
		#bool xmp_set_property_int64(XmpPtr xmp, const char *schema, 
		#							const char *name, int64_t value,
		#							uint32_t optionBits);
		return bool(_exempi.xmp_set_property_int64(self.xmpptr, schema_ns, prop_name, prop_value,0))
	
	def set_property_float(self, schema_ns, prop_name, prop_value, options = 0 ):
		"""  """
		#/** Set a float XMP property in the XMP packet
		# * @param xmp the XMP packet
		# * @param schema
		# * @param name
		# * @param value the float value
		# * @param optionBits
		# * @return false if failure
		# */
		#bool xmp_set_property_float(XmpPtr xmp, const char *schema, 
		#							const char *name, double value,
		#							uint32_t optionBits);
		prop_value = c_float(prop_value)
		return bool(_exempi.xmp_set_property_float(self.xmpptr, schema_ns, prop_name, prop_value,0))
		
	
	def set_property_datetime(self, schema_ns, prop_name, prop_value, options = 0 ):
		"""  """
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
		#			    const char *genericLang, const char *specificLang,
		#			    XmpStringPtr actualLang, XmpStringPtr itemValue,
		#			    uint32_t *propBits);
		raise NotImplementedError

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
		raise NotImplementedError
		
	def delete_localized_text( self, schema_ns, alt_text_name, generic_lang, specific_lang ):
		#bool xmp_delete_localized_text(XmpPtr xmp, const char *schema,
		#							   const char *name, const char *genericLang,
		#							   const char *specificLang);
		raise NotImplementedError
			
	# ------------------------------------------------
	# Functions for deleting and detecting properties.
	# ------------------------------------------------
	def delete_property(self, schema_ns, prop_name ):
		"""  """
		#/** Delete a property from the XMP Packet provided
		# * @param xmp the XMP packet
		# * @param schema the schema of the property
		# * @param name the name of the property
		# */
		#bool xmp_delete_property(XmpPtr xmp, const char *schema, const char *name);
		raise NotImplementedError

	def delete_array_item( self, schema_ns, array_name, item_index ):
		""" 
		Not Implemented - Exempi does not implement this function yet
		"""
		raise NotImplementedError

	def delete_struct_field( self, schema_ns, struct_name, field_ns, field_name ):
		""" 
		Not Implemented - Exempi does not implement this function yet
		"""
		raise NotImplementedError

	def delete_qualifier( self, schema_ns, prop_name, qual_ns, qual_name ):
		""" 
		Not Implemented - Exempi does not implement this function yet
		"""
		raise NotImplementedError
		
	def does_property_exist(self, schema_ns, prop_name ):
		"""  """
		#/** Determines if a property exists in the XMP Packet provided
		# * @param xmp the XMP packet
		# * @param schema the schema of the property. Can't be NULL or empty.
		# * @param name the name of the property. Can't be NULL or empty.
		# * @return true is the property exists
		# */
		#bool xmp_has_property(XmpPtr xmp, const char *schema, const char *name);
		return bool(_exempi.xmp_has_property(xmp.xmpptr, schema_ns, prop_name))
		
	def does_array_item_exist(self, schema_ns, array_name, item_index ):
		""" 
		Not Implemented - Exempi does not implement this function yet
		"""
		raise NotImplementedError("Exempi does not implement this function yet")
		
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
	def parse_from_str( self, xmp_packet_str ):
		#/** Parse the XML passed through the buffer and load
		# * it.
		# * @param xmp the XMP packet.
		# * @param buffer the buffer.
		# * @param len the length of the buffer.
		# */
		# TODO: convert string to proper data type
		l = len(xmp_packet_str)
		res = _exempi.xmp_parse(self.xmpptr, xmp_packet_str, l )
		_check_for_error()
		return res
		
	def serialize_to_str( self, options, padding, newline, indent, base_indent ):
		#/** Serialize the XMP Packet to the given buffer with formatting
		# * @param xmp the XMP Packet
		# * @param buffer the buffer to write the XMP to
		# * @param options options on how to write the XMP.  See XMP_SERIAL_*
		# * @param padding number of bytes of padding, useful for modifying
		# *                embedded XMP in place.
		# * @param newline the new line character to use
		# * @param tab the indentation character to use
		# * @param indent the initial indentation level
		# * @return TRUE if success.
		# */
		#bool xmp_serialize_and_format(XmpPtr xmp, XmpStringPtr buffer, 
		#							  uint32_t options, 
		#							  uint32_t padding, const char *newline, 
		#							  const char *tab, int32_t indent);
		raise NotImplementedError
		
	def serialize_to_str( self, options, padding = 0 ):
		#/** Serialize the XMP Packet to the given buffer
		# * @param xmp the XMP Packet
		# * @param buffer the buffer to write the XMP to
		# * @param options options on how to write the XMP.  See XMP_SERIAL_*
		# * @param padding number of bytes of padding, useful for modifying
		# *                embedded XMP in place.
		# * @return TRUE if success.
		# */
		
		#xmp_string_new()
		#bool _exempi.xmp_serialize( xmpptr, xmpstring, options, padding )
		#
		raise NotImplementedError
		
	
	# -------------------------------------
	# Misceallaneous functions
	# -------------------------------------
	def clone( self, options ):
		# TODO: check what xmp_copy can return.
		# newptr = _exempi.xmp_copy( self.xmpptr )
		
		raise NotImplementedError

	def count_array_items( self, schema_ns, array_name ):
		""" 
		Not Implemented - Exempi does not implement this function yet
		"""
		raise NotImplementedError("Exempi does not implement this function yet")
			
	# -------------------------------------
	# Namespace Functions
	# -------------------------------------
	@staticmethod
	def register_namespace( namespace_uri, suggested_prefix ):
		#/** Register a new namespace to add properties to
		# *  This is done automatically when reading the metadata block
		# *  @param namespaceURI the namespace URI to register
		# *  @param suggestedPrefix the suggested prefix
		# *  @param registeredPrefix the really registered prefix. Not necessarily
		# *  %suggestedPrefix. 
		# *  @return true if success, false otherwise.
		# */
		#bool xmp_register_namespace(const char *namespaceURI, 
		#														const char *suggestedPrefix,
		#														XmpStringPtr registeredPrefix);
		raise NotImplementedError()

	@staticmethod
	def get_namespace_prefix( namespace_uri ):
		""" 
		Not Implemented - Exempi does not implement this function yet
		"""
		raise NotImplementedError("Exempi does not implement this function yet")

	@staticmethod
	def get_namespaec_uri( namespace_prefix ):
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
		#TODO: check default value for options param
		options = c_ulong(0x0002L)
		self.xmpiteratorptr = _exempi.xmp_iterator_new(xmp_obj._get_internal_ref(), schema_ns, prop_name, 0 )
		_check_for_error()
		self.schema = schema_ns
		self.prop_name = prop_name
		self.options = options
		
#	def __init__( self, str ):
#		raise NotImplementedError
#		
		
	def __del__(self):
		#_exempi.xmp_iterator_free(self.xmpiteratorptr);
		#_check_for_error()
		pass
		
	def __iter__(self):
		return self
		
	def next(self):
		# TODO: define options			
		# TODO: pointers neeed to be passed in...hmm
		#return _exempi.xmp_iterator_next( xmpiteratorptr, self.schema, self.prop_name, XmpStringPtr propValue,
		#					   uint32_t *options);
		#raise NotImplementedError
		prop_value = _xmp_string_new()
		the_value = None
		
		options = c_ulong(0x0002L) #FIXME: hardcoded for testing purposes only
		
		if _exempi.xmp_iterator_next(self.xmpiteratorptr,self.schema, self.prop_name, prop_value,0 ):
			the_value = _exempi.xmp_string_cstr(prop_value)
		_xmp_string_free(prop_value)
		return the_value
		
		
	def skip( options ):
		# TODO: define options
		_exempi.xmp_iterator_skip( self.xmpiteratorptr, options );
		_check_for_error()
		
		

		
class XMPUtils:
	def __init__(self):
		raise NotImplementedError