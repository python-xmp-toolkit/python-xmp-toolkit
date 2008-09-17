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
# THIS SOFTWARE IS PROVIDED BY ESA/ESO ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL ESA/ESO BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE

import sys
sys.path.append('../')

from libxmp import *
from libxmp import _exempi


def tests_xmp_files():
	XMPFiles.initialize()
	assert(_exempi.xmp_get_error() == 0)
	xmpfile = XMPFiles()
	assert(_exempi.xmp_get_error() == 0)
	xmpfile.open_file( 'sig05-002a.tif', files.XMP_OPEN_READ )
	assert(_exempi.xmp_get_error() == 0)
	xmp = xmpfile.get_xmp()
	assert(_exempi.xmp_get_error() == 0)

	assert( xmp.get_property( "http://www.communicatingastronomy.org/avm/1.0/", "Publisher" ) == "Spitzer Science Center" )
	
	#
	#if xmpfile_image.can_put_xmp( xmp ):
	#	print "Putting XMP"
	#	xmpfile_image.put_xmp( xmp )
	#else:
	#	print "Cannot put XMP"
	#	
	xmpfile.close_file()
	#xmpfile_image.close_file()
	XMPFiles.terminate()
	

def main():
	tests_xmp_files()

if __name__ == "__main__":
	main()
	
	
	
#	assert(exempi.xmp_init())
#	assert(exempi.xmp_get_error() == 0)
#
#	f = exempi.xmp_files_open_new("sig05-002a.tif", 1);
#	assert(exempi.xmp_get_error() == 0)
#	assert(f)
#
#	xmp = exempi.xmp_files_get_new_xmp(f)
#	assert(exempi.xmp_get_error() == 0)
#	assert(xmp)
#
#	the_prop = exempi.xmp_string_new();
#	exempi.xmp_string_cstr.restype = c_char_p
#	exempi.xmp_get_property(xmp, "http://www.communicatingastronomy.org/avm/1.0/", "Publisher", the_prop, 0 )
#	text = exempi.xmp_string_cstr(the_prop); 
#	print text
#	exempi.xmp_string_free(the_prop);
#
#	exempi.xmp_free(xmp)
#	assert(exempi.xmp_get_error() == 0)
#
#	exempi.xmp_files_free(f)
#	assert(exempi.xmp_get_error() == 0)
#
#	exempi.xmp_terminate()
