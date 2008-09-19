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

import unittest
import sys
import os
sys.path.append('../')

from libxmp import *
from libxmp import XMPIterator
from libxmp import _exempi

from samples import samplefiles, open_flags, sampledir, make_temp_samples, remove_temp_samples
import xmpcoverage

class TestClass(object):
	def __unicode__(self):
		return xmpcoverage.RDFCoverage

class XMPMetaTestCase(unittest.TestCase):
	def setUp(self):
		make_temp_samples()
		XMPMeta.initialize()
		
	def tearDown(self):
		XMPMeta.terminate()
		remove_temp_samples()
		
	def test_init_del(self):
		xmp = XMPMeta()
		self.failUnless( xmp.internal_ref )
		del xmp
		
	def test_test_files(self):
		for f in samplefiles.iterkeys():
			self.assert_( os.path.exists(f), "Test file does not exists." )
		
	def test_get_xmp(self):
		for f,fmt in samplefiles.iteritems():
			xmpfile = XMPFiles( file_path=f )
			xmp = xmpfile.get_xmp()
			self.assert_( isinstance(xmp, XMPMeta), "Not an XMPMeta object" )
			xmpfile.close_file()
			
	def test_parse_str(self):
		xmp = XMPMeta()
		self.assert_( xmp.parse_from_str( xmpcoverage.RDFCoverage, xmpmeta_wrap=True ), "Could not parse valid string." )
		self.assertEqual( xmp.get_property( xmpcoverage.NS1, "SimpleProp1" ), "Simple1 value" ) 
		print xmp.serialize_to_str(use_compact_format=True, omit_packet_wrapper=True)
		del xmp
		
def suite():
	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(XMPMetaTestCase))	
	return suite

def test( verbose=2 ):
	all_tests = suite()
	runner = unittest.TextTestRunner(verbosity=verbose)
	result = runner.run(all_tests)
	return result, runner

if __name__ == "__main__":
	test()
	#unittest.main()