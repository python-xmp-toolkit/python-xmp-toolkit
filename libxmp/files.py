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

class XMPFiles:
	def __init__(self, file_path, format = ..., open_flags = 0):
		pass
		
	def __init__(self, xmp_files_obj ):
		pass
	
	def __init__(self):
		pass
		
	def __del__(self):
		pass
		
	def open_file(self, file_path, format = ... , open_flags=0 ):
		pass
	
	def close_file( self, close_flags = 0 ):
		pass
		
	def get_file_info( self ):
		pass
		
	def get_xmp( self ):
		pass
		
	def get_thumbnail( self ):
		pass
		
	def put_xmp( self, xmp_obj ):
		pass
		
	def can_put_xmp( sef, xmp_obj ):
		pass
		
	@static
	def get_version_info():
		pass
		
	@static
	def initialize():
		pass
		
	@static
	def initialize( options ):
		pass
	
	@static	
	def terminate():
		pass
		
	@static
	def get_format_info( format ):
		pass