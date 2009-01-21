# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, European Space Agency & European Southern Observatory (ESA/ESO)
# Copyright (c) 2008, CRS4 - Centre for Advanced Studies, Research and Development in Sardinia
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
#       Observatory, CRS4 nor the names of its contributors may be used to endorse or 
#       promote products derived from this software without specific prior 
#       written permission.
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

#TODO: make a proper testsuite for core using unittest

import sys
import os
import os.path

sys.path.append(os.path.pardir)

from libxmp import *
from libxmp.core import XMPIterator, XMPMeta
from libxmp.consts import *


def tests_xmp_core():
	XMPFiles.initialize()
	xmpfile = XMPFiles()
	xmpfile.open_file( 'samples/img1.png', XMP_OPEN_FORUPDATE )
	#xmp = xmpfile.get_xmp()
	xmp = XMPMeta()
	d = {}
	print "OK"
	
	
#	for x in xmp:
#		print x
#		if has_option(x[-1],XMP_IS_SCHEMA):
#			d[x[0]] = []
#		else:
#			d[x[0]].append(x[1:])

#bool xmp_set_property(XmpPtr xmp, const char *schema, 
#					  const char *name, const char *value,
#					  uint32_t optionBits);			
	
	xmp.set_property('http://purl.org/dc/elements/1.1/', 'dc:description', 'Ciao mamma guarda come mi diverto col cantatu',0)
	xmp.append_array_item('http://purl.org/dc/elements/1.1/', 'dc:creator', 'Gianni', XMP_PROP_ARRAY_IS_ORDERED )
	xmp.append_array_item('http://purl.org/dc/elements/1.1/', 'dc:creator', 'Pino', XMP_PROP_ARRAY_IS_ORDERED )

	print "OK2"
	xmpfile.put_xmp(xmp)
	print d.keys()
	print "ok3"
	xmpfile.close_file()
	XMPFiles.terminate()


	


def main():
	tests_xmp_core()


if __name__ == "__main__":
	main()