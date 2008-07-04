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


class XMPMeta:
	""" """
	
	def __init__( self, xmp_str ):
		""" """
		pass

	def __init__( self):
		""" """
		pass
		
	def __del__(self):
		pass

	# -------------------------------------
	# Initialization and termination
	# -------------------------------------
	@static
	def initialize():
		pass
		
	@static
	def terminate():
		pass
	
	@static
	def get_version_info():
		pass
		
	# -------------------------------------
	# Global option flags
	# -------------------------------------
	@static
	def get_global_options():
		pass

	def set_global_options(self, options):
		pass

	@static
	def get_version_info():
		pass

	# -------------------------------------
	# Functions for getting property values
	# -------------------------------------
	def get_property(self, schema_ns, prop_name ):
		"""  """
		# throw exeception on error
		pass
		
	def get_array_item( self, schema_ns, array_name, item_index ):
		"""  """
		# throw exeception on error
		pass
	
	def get_struct_field( self, schema_ns, struct_name, field_ns, field_name ):
		"""  """
		# throw exeception on error
		pass
		
	def get_qualifier( self, schema_ns, prop_name, qual_ns, qual_name ):
		"""  """
		# throw exeception on error
		pass
		
	# -------------------------------------
	# Functions for setting property values
	# -------------------------------------
	def set_property(self, schema_ns, prop_name, prop_value, options = 0 ):
		"""  """
		# throw exeception on error
		pass
		
	def set_array_item( self, schema_ns, array_name, item_index, item_value, options = 0 ):
		"""  """
		# throw exeception on error
		pass
		
	def append_array_item( self, schema_ns, array_name, array_options, item_value, options = 0 ):
		"""  """
		# throw exeception on error
		pass
	
	def set_struct_field( self, schema_ns, struct_name, field_ns, field_name, field_value, options = 0 ):
		"""  """
		# throw exeception on error
		pass
		
	def set_qualifier( self, schema_ns, prop_name, qual_ns, qual_name, qual_value, options = 0 ):
		"""  """
		# throw exeception on error
		pass
		
	# -----------------------------------------------
	# Functions accessing properties as binary values
	# -----------------------------------------------
	def get_property_bool(self, schema_ns, prop_name ):
		"""  """
		# throw exeception on error
		pass
		
	def get_property_int(self, schema_ns, prop_name ):
		"""  """
		# throw exeception on error
		pass
		
	def get_property_long(self, schema_ns, prop_name ):
		"""  """
		# throw exeception on error
		pass
		
	def get_property_float(self, schema_ns, prop_name ):
		"""  """
		# throw exeception on error
		pass
		
	def get_property_datetime(self, schema_ns, prop_name ):
		"""  """
		# throw exeception on error
		pass
		
	def set_property_bool(self, schema_ns, prop_name, prop_value, options = 0 ):
		"""  """
		# throw exeception on error
		pass

	def set_property_int(self, schema_ns, prop_name, prop_value, options = 0 ):
		"""  """
		# throw exeception on error
		pass
	
	def set_property_long(self, schema_ns, prop_name, prop_value, options = 0 ):
		"""  """
		# throw exeception on error
		pass
	
	def set_property_float(self, schema_ns, prop_name, prop_value, options = 0 ):
		"""  """
		# throw exeception on error
		pass
		
	
	def set_property_date(self, schema_ns, prop_name, prop_value, options = 0 ):
		"""  """
		# throw exeception on error
		pass
		
	# ------------------------------------------------------------
	# Functions for accessing localized text (alt-text) properties
	# ------------------------------------------------------------
	def get_localized_text( self, schema_ns, alt_text_name, generic_lang, specific_lang ):
		pass

	def set_localized_text( self, schema_ns, alt_text_name, generic_lang, specific_lang, item_value, options = 0 ):
		pass
			
	# ------------------------------------------------
	# Functions for deleting and detecting properties.
	# ------------------------------------------------
	def delete_property(self, schema_ns, prop_name ):
		"""  """
		# throw exeception on error
		pass

	def delete_array_item( self, schema_ns, array_name, item_index ):
		"""  """
		# throw exeception on error
		pass

	def delete_struct_field( self, schema_ns, struct_name, field_ns, field_name ):
		"""  """
		# throw exeception on error
		pass

	def delete_qualifier( self, schema_ns, prop_name, qual_ns, qual_name ):
		"""  """
		# throw exeception on error
		pass
		
	def does_property_exist(self, schema_ns, prop_name ):
		"""  """
		pass
		
	def does_array_item_exist(self, schema_ns, array_name, item_index ):
		"""  """
		pass
		
	def does_struct_field_exist(self, schema_ns, struct_name, field_ns, field_name ):
		"""  """
		pass

	def does_qualifier_exist(self, schema_ns, prop_name, qual_ns, qual_name ):
		"""  """
		pass

	# -------------------------------------
	# Functions for parsing and serializing
	# -------------------------------------
	def parse_from_str( self, str ):
		pass
		
	def serialize_to_str( self, options, padding, newline, indent, base_indent ):
		pass
		
	def serialize_to_str( self, options, padding = 0 ):
		pass
		
	
	# -------------------------------------
	# Misceallaneous functions
	# -------------------------------------
	def clone( self, options ):
		pass

	def count_array_items( self, schema_ns, array_name ):
		pass
			
	# -------------------------------------
	# Namespace Functions
	# -------------------------------------
	@static
	def register_namespace( namespace_uri, suggested_prefix ):
		pass

	@static
	def get_namespace_prefix( namespace_uri ):
		pass

	@static
	def get_namespaec_uri( namespace_prefix ):
		pass
		
	@static
	def delete_namespace( namespace_uri):
		pass
		
	# -------------------------------------
	# Alias Functions
	# -------------------------------------
	@static
	def register_alias( alias_ns, alias_prop, actual_ns, actual_prop, array_form = ... ):
		pass

	@static
	def resolve_alias( alias_ns, alias_prop ):
		pass

	@static
	def delete_alias( alias_ns, alias_prop ):
		pass

	@static
	def register_standard_alias( schema_ns ):
		pass
		
class XMPIterator:
	
	def __init__( self, str ):
		pass
		
	def __init__( self, xmp_obj, schema_ns, prop_name, options = 0 ):
		pass

	def __init__( self, schema_ns, prop_name, options = 0 ):
		pass
		
	def __del__(self):
		pass
		
	def next():
		pass
		
	def skip():
		pass

		
class XMPUtils:
	pass