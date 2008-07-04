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
from libxmp import _exempi, _XMP_ERROR_CODES

class XMPMeta:
	""" """
	
	def __init__( self, **kwargs ):
		"""
		@param xmp_str Optional.
		"""
		if kwargs.has_key('xmp_internal_ref'):
			self.xmpptr = kwargs['xmp_internal_ref']
		else:
			self.xmpptr = None
		
			if kwargs.has_key('xmp_str'):
				self.parse_from_str( kwargs['xmp_str'] )
		
	def __del__(self):
		pass
		
	def _get_internal_ref(self):
		return  self.xmpptr
		
	def _check_for_error(self):
		"""
		Check if an error occured when executing last operation. Raise an
		exception in case of an error.
		"""
		err = _exempi.xmp_get_error()
		if err != 0:
			raise XMPError( _XMP_ERROR_CODES[err] )

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
			self._check_for_error()
	
	@staticmethod
	def terminate():
		_exempi.xmp_terminate()
	
	@staticmethod
	def get_version_info():
		raise NotImplementedError
		
	# -------------------------------------
	# Global option flags
	# -------------------------------------
	@staticmethod
	def get_global_options():
		raise NotImplementedError

	def set_global_options(self, options):
		raise NotImplementedError

	@staticmethod
	def get_version_info():
		raise NotImplementedError

	# -------------------------------------
	# Functions for getting property values
	# -------------------------------------
	def get_property(self, schema_ns, prop_name ):
		"""  """
		# throw exeception on error
		raise NotImplementedError
		
	def get_array_item( self, schema_ns, array_name, item_index ):
		"""  """
		# throw exeception on error
		raise NotImplementedError
	
	def get_struct_field( self, schema_ns, struct_name, field_ns, field_name ):
		"""  """
		# throw exeception on error
		raise NotImplementedError
		
	def get_qualifier( self, schema_ns, prop_name, qual_ns, qual_name ):
		"""  """
		# throw exeception on error
		raise NotImplementedError
		
	# -------------------------------------
	# Functions for setting property values
	# -------------------------------------
	def set_property(self, schema_ns, prop_name, prop_value, options = 0 ):
		"""  """
		# throw exeception on error
		raise NotImplementedError
		
	def set_array_item( self, schema_ns, array_name, item_index, item_value, options = 0 ):
		"""  """
		# throw exeception on error
		raise NotImplementedError
		
	def append_array_item( self, schema_ns, array_name, array_options, item_value, options = 0 ):
		"""  """
		# throw exeception on error
		raise NotImplementedError
	
	def set_struct_field( self, schema_ns, struct_name, field_ns, field_name, field_value, options = 0 ):
		"""  """
		# throw exeception on error
		raise NotImplementedError
		
	def set_qualifier( self, schema_ns, prop_name, qual_ns, qual_name, qual_value, options = 0 ):
		"""  """
		# throw exeception on error
		raise NotImplementedError
		
	# -----------------------------------------------
	# Functions accessing properties as binary values
	# -----------------------------------------------
	def get_property_bool(self, schema_ns, prop_name ):
		"""  """
		# throw exeception on error
		raise NotImplementedError
		
	def get_property_int(self, schema_ns, prop_name ):
		"""  """
		# throw exeception on error
		raise NotImplementedError
		
	def get_property_long(self, schema_ns, prop_name ):
		"""  """
		# throw exeception on error
		raise NotImplementedError
		
	def get_property_float(self, schema_ns, prop_name ):
		"""  """
		# throw exeception on error
		raise NotImplementedError
		
	def get_property_datetime(self, schema_ns, prop_name ):
		"""  """
		# throw exeception on error
		raise NotImplementedError
		
	def set_property_bool(self, schema_ns, prop_name, prop_value, options = 0 ):
		"""  """
		# throw exeception on error
		raise NotImplementedError

	def set_property_int(self, schema_ns, prop_name, prop_value, options = 0 ):
		"""  """
		# throw exeception on error
		raise NotImplementedError
	
	def set_property_long(self, schema_ns, prop_name, prop_value, options = 0 ):
		"""  """
		# throw exeception on error
		raise NotImplementedError
	
	def set_property_float(self, schema_ns, prop_name, prop_value, options = 0 ):
		"""  """
		# throw exeception on error
		raise NotImplementedError
		
	
	def set_property_date(self, schema_ns, prop_name, prop_value, options = 0 ):
		"""  """
		# throw exeception on error
		raise NotImplementedError
		
	# ------------------------------------------------------------
	# Functions for accessing localized text (alt-text) properties
	# ------------------------------------------------------------
	def get_localized_text( self, schema_ns, alt_text_name, generic_lang, specific_lang ):
		raise NotImplementedError

	def set_localized_text( self, schema_ns, alt_text_name, generic_lang, specific_lang, item_value, options = 0 ):
		raise NotImplementedError
			
	# ------------------------------------------------
	# Functions for deleting and detecting properties.
	# ------------------------------------------------
	def delete_property(self, schema_ns, prop_name ):
		"""  """
		# throw exeception on error
		raise NotImplementedError

	def delete_array_item( self, schema_ns, array_name, item_index ):
		"""  """
		# throw exeception on error
		raise NotImplementedError

	def delete_struct_field( self, schema_ns, struct_name, field_ns, field_name ):
		"""  """
		# throw exeception on error
		raise NotImplementedError

	def delete_qualifier( self, schema_ns, prop_name, qual_ns, qual_name ):
		"""  """
		# throw exeception on error
		raise NotImplementedError
		
	def does_property_exist(self, schema_ns, prop_name ):
		"""  """
		raise NotImplementedError
		
	def does_array_item_exist(self, schema_ns, array_name, item_index ):
		"""  """
		raise NotImplementedError
		
	def does_struct_field_exist(self, schema_ns, struct_name, field_ns, field_name ):
		"""  """
		raise NotImplementedError

	def does_qualifier_exist(self, schema_ns, prop_name, qual_ns, qual_name ):
		"""  """
		raise NotImplementedError

	# -------------------------------------
	# Functions for parsing and serializing
	# -------------------------------------
	def parse_from_str( self, str ):
		raise NotImplementedError
		
	def serialize_to_str( self, options, padding, newline, indent, base_indent ):
		raise NotImplementedError
		
	def serialize_to_str( self, options, padding = 0 ):
		raise NotImplementedError
		
	
	# -------------------------------------
	# Misceallaneous functions
	# -------------------------------------
	def clone( self, options ):
		raise NotImplementedError

	def count_array_items( self, schema_ns, array_name ):
		raise NotImplementedError
			
	# -------------------------------------
	# Namespace Functions
	# -------------------------------------
	@staticmethod
	def register_namespace( namespace_uri, suggested_prefix ):
		raise NotImplementedError

	@staticmethod
	def get_namespace_prefix( namespace_uri ):
		raise NotImplementedError

	@staticmethod
	def get_namespaec_uri( namespace_prefix ):
		raise NotImplementedError
		
	@staticmethod
	def delete_namespace( namespace_uri):
		raise NotImplementedError
		
	# -------------------------------------
	# Alias Functions
	# -------------------------------------
	@staticmethod
	def register_alias( alias_ns, alias_prop, actual_ns, actual_prop, array_form = None ):
		raise NotImplementedError

	@staticmethod
	def resolve_alias( alias_ns, alias_prop ):
		raise NotImplementedError

	@staticmethod
	def delete_alias( alias_ns, alias_prop ):
		raise NotImplementedError

	@staticmethod
	def register_standard_alias( schema_ns ):
		raise NotImplementedError
		
class XMPIterator:
	def __init__( self, **kwargs ):
		raise NotImplementedError
	
#	def __init__( self, str ):
#		raise NotImplementedError
#		
#	def __init__( self, xmp_obj, schema_ns, prop_name, options = 0 ):
#		raise NotImplementedError
#
#	def __init__( self, schema_ns, prop_name, options = 0 ):
#		raise NotImplementedError
		
	def __del__(self):
		pass
		
	def __iter__(self):
		return self
		
	def next():
		raise NotImplementedError
		# raise StopIteration when no more
		
	def skip():
		raise NotImplementedError

		
class XMPUtils:
	pass