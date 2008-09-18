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

#TODO: make a proper testsuite for core using unittest

from libxmp import *

def tests_xmp_core():
	XMPFiles.initialize()
	xmpfile = XMPFiles()
	xmpfile.open_file( 'samples/sig05-002a.tif', files.XMP_OPEN_READ )
	xmp = xmpfile.get_xmp()

	print xmp.set_property("http://www.communicatingastronomy.org/avm/1.0/", "Publisher", "Eric Idle")
	print xmp.get_property("http://www.communicatingastronomy.org/avm/1.0/", "Publisher")
	import datetime
	print xmp.set_property_date("http://ns.adobe.com/xap/1.0/","ModifyDate", datetime.datetime.now())
	
	print xmp.get_property_datetime("http://ns.adobe.com/xap/1.0/","ModifyDate")
	print xmp.set_property_bool("http://ns.adobe.com/camera-raw-settings/1.0/","AlreadyApplied", False)
	print xmp.get_property_bool("http://ns.adobe.com/camera-raw-settings/1.0/", "AlreadyApplied")

	
	xmpfile.close_file()
	XMPFiles.terminate()

def main():
	tests_xmp_core()

if __name__ == "__main__":
	main()
	
	
