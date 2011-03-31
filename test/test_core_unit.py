# -*- coding: utf-8 -*-
#
# Copyright (c) 2008-2009, European Space Agency & European Southern Observatory (ESA/ESO)
# Copyright (c) 2008-2009, CRS4 - Centre for Advanced Studies, Research and Development in Sardinia
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

import unittest
import sys
import os
import os.path

sys.path.append(os.path.pardir)

from libxmp import *
from libxmp import XMPIterator
from libxmp import _exempi
from libxmp.utils import file_to_dict, object_to_dict

from samples import samplefiles, open_flags, sampledir, make_temp_samples, remove_temp_samples
import xmpcoverage

class TestClass(object):
	def __unicode__(self):
		return xmpcoverage.RDFCoverage

class XMPMetaTestCase(unittest.TestCase):
	def setUp(self):
		make_temp_samples()
		
	def tearDown(self):
		remove_temp_samples()
		
	def test_init_del(self):
		xmp = XMPMeta()
		self.failUnless( xmp.xmpptr )
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

	def test_get_localized_text(self):
		xmp = XMPMeta()
		self.assert_( xmp.parse_from_str( xmpcoverage.RDFCoverage, xmpmeta_wrap=True ), "Could not parse valid string." )
		self.assertEqual( xmp.get_property( xmpcoverage.NS1, "SimpleProp2" ), "Simple2 value" )
		self.assertEqual( xmp.get_localized_text( xmpcoverage.NS1, "ArrayProp2", 'x-one', 'x-one' ), "Item2.1 value" )
		
		 
		del xmp
			
	def test_parse_str(self):
		xmp = XMPMeta()
		self.assert_( xmp.parse_from_str( xmpcoverage.RDFCoverage, xmpmeta_wrap=True ), "Could not parse valid string." )
		self.assertEqual( xmp.get_property( xmpcoverage.NS1, "SimpleProp1" ), "Simple1 value" ) 
		del xmp
		
	def test_shorthand_rdf(self):
		xmp = XMPMeta()
		self.assert_( xmp.parse_from_str( xmpcoverage.ShorthandRDF, xmpmeta_wrap=True ), "Could not parse valid string." )
		self.assertEqual( xmp.get_property( "http://ns.adobe.com/tiff/1.0", "Model" ), "Canon PowerShot S300" ) 
		del xmp

	def test_serialize_str(self):
		xmp = XMPMeta()
		self.assert_( xmp.parse_from_str( xmpcoverage.RDFCoverage, xmpmeta_wrap=True ), "Could not parse valid string." )
		self.assert_( isinstance( xmp.serialize_to_str(use_compact_format=True, omit_packet_wrapper=True), str ), "Result is not a 8-bit string" )
		self.assertRaises( XMPError, xmp.serialize_to_str, read_only_packet=True, omit_packet_wrapper=True )
		self.assertRaises( XMPError, xmp.serialize_to_str, include_thumbnail_pad=True, omit_packet_wrapper=True )
		self.assertRaises( XMPError, xmp.serialize_to_str, exact_packet_length=True, omit_packet_wrapper=True )
		del xmp
		
	def test_serialize_unicode(self):
		xmp = XMPMeta()
		self.assert_( xmp.parse_from_str( xmpcoverage.RDFCoverage, xmpmeta_wrap=True ), "Could not parse valid string." )
		self.assert_( isinstance( xmp.serialize_to_unicode(use_compact_format=True, omit_packet_wrapper=False), unicode ), "Result is not a unicode string" )
		self.assertRaises( XMPError, xmp.serialize_to_unicode, read_only_packet=True, omit_packet_wrapper=True )
		self.assertRaises( XMPError, xmp.serialize_to_unicode, include_thumbnail_pad=True, omit_packet_wrapper=True )
		self.assertRaises( XMPError, xmp.serialize_to_unicode, exact_packet_length=True, omit_packet_wrapper=True )
		del xmp
		
	def test_serialize_and_format(self):
		xmp = XMPMeta()
		self.assert_( xmp.parse_from_str( xmpcoverage.RDFCoverage, xmpmeta_wrap=True ), "Could not parse valid string." )
		self.assert_( isinstance( xmp.serialize_and_format( padding=0, newlinechr='NEWLINE', tabchr = 'TAB', indent=6 ), str ), "Result is not a 8-bit string" )
		self.assertRaises( XMPError, xmp.serialize_and_format, read_only_packet=True, omit_packet_wrapper=True )
		self.assertRaises( XMPError, xmp.serialize_and_format, include_thumbnail_pad=True, omit_packet_wrapper=True )
		self.assertRaises( XMPError, xmp.serialize_and_format, exact_packet_length=True, omit_packet_wrapper=True )
		del xmp
		
	def test_clone(self):
		xmp1 = XMPMeta()
		self.assert_( xmp1 == xmp1, "XMP1 not equal it self" )
		self.failIf( xmp1 != xmp1, "XMP1 is equal it self" )
		xmp2 = xmp1.clone()
		self.failIf( xmp1 == xmp2, "XMP1 is not equal XMP2" )
		self.assert_( xmp1 != xmp2, "XMP1 is not equal XMP2" )
		del xmp1
		del xmp2
	
	def test_text_property_450_file(self):
		# Currently fails on OS X 10.6 with Exempi installed from MacPorts
		files = ["fixtures/BlueSquare450.xmp","fixtures/BlueSquare450.tif"]
		options = ['open_nooption','open_read','open_forupdate','open_onlyxmp','open_cachetnail','open_strictly','open_usesmarthandler','open_usepacketscanning','open_limitscanning',]
		for f in files:
			for o in options:
				try:
					xmpfile = XMPFiles( file_path=f, ** { o : True } )
					xmp_data = xmpfile.get_xmp()
					headline = xmp_data.get_property( "http://ns.adobe.com/photoshop/1.0/", 'Headline' )
					
					self.assertEqual( headline[-5:], "=END="  )
					self.assert_( len(headline) > 450, "Not all text was extracted from headline property."  )
				except XMPError, e:
					pass
					
		
	def test_text_property_450(self):
		xmp = XMPMeta()
		self.assert_( xmp.parse_from_str( xmpcoverage.LongTextProperty, xmpmeta_wrap=True ), "Could not parse valid string." )
		headline = xmp.get_property( "http://ns.adobe.com/photoshop/1.0/", 'Headline' )
		self.assertEqual( headline[-5:], "=END="  )
		self.assert_( len(headline) > 450, "Not all text was extracted from headline property."  )
		
		
	def test_does_property_exist(self):
		xmp = XMPFiles( file_path="fixtures/BlueSquare450.tif" )
		xmp_data = xmp.get_xmp()
		self.assert_( xmp_data.does_property_exist( "http://ns.adobe.com/photoshop/1.0/", 'Headline' ) )
				
		
class UtilsTestCase(unittest.TestCase):
	def setUp(self):
		make_temp_samples()
		
	def tearDown(self):
		remove_temp_samples()
		
	def test_object_to_dict(self):
		for f,fmt in samplefiles.iteritems():
			xmpfile = XMPFiles( file_path=f )
			xmp = xmpfile.get_xmp()
			self.assert_( object_to_dict( xmp ), "Not an XMPMeta object" )
			xmpfile.close_file()
	
	def test_file_to_dict(self):
		for f,fmt in samplefiles.iteritems():
			self.assert_( file_to_dict( f ), "Expected dictionary" )
			
	def test_file_to_dict_nofile(self):
		self.assertRaises( IOError, file_to_dict, "nonexistingfile.ext" )
		
	def test_file_to_dict_noxmp(self):
		self.assertEqual( file_to_dict("fixtures/empty.txt"), {} )
		
	def test_object_to_dict_noxmp(self):
		self.assertEqual( object_to_dict( [] ), {} )
		
		
def suite():
	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(XMPMetaTestCase))
	suite.addTest(unittest.makeSuite(UtilsTestCase))	
	return suite

def test( verbose=2 ):
	all_tests = suite()
	runner = unittest.TextTestRunner(verbosity=verbose)
	result = runner.run(all_tests)
	return result, runner

if __name__ == "__main__":
	#test()
	unittest.main()