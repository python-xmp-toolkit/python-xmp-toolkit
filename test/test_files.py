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
import platform

sys.path.append(os.path.pardir)

from libxmp import *
from libxmp.consts import *
from libxmp import _exempi

from samples import samplefiles, open_flags, sampledir, make_temp_samples, remove_temp_samples

class XMPFilesTestCase(unittest.TestCase):
	def setUp(self):
		make_temp_samples()
		
	def tearDown(self):
		remove_temp_samples()
		
	def test_init_del(self):
		xmpfile = XMPFiles()
		self.failUnless( xmpfile.xmpfileptr )
		del xmpfile
		
	def test_test_files(self):
		for f in samplefiles.iterkeys():
			self.assert_( os.path.exists(f), "Test file does not exists." )
		
	def test_open_file(self):
		# Non-existing file.
		xmpfile = XMPFiles()
		self.assertRaises( XMPError, xmpfile.open_file, '' )
		
		xmpfile = XMPFiles()
		xmpfile.open_file( samplefiles.keys()[0] )
		self.assertRaises( XMPError, xmpfile.open_file, samplefiles.keys()[0] )
		self.assertRaises( XMPError, xmpfile.open_file, samplefiles.keys()[1] )
		xmpfile.close_file()
		xmpfile.open_file( samplefiles.keys()[1] )
		self.assertRaises( XMPError, xmpfile.open_file, samplefiles.keys()[0] )
		
		# Open all sample files.
		for f in samplefiles.iterkeys():
			xmpfile = XMPFiles()
			xmpfile.open_file( f )
						
		# Try using init
		for f,fmt in samplefiles.iteritems():
			xmpfile = XMPFiles( file_path=f )

		# Try all open options
		for flg in open_flags:
			kwargs = { flg: True }
			
			for f,fmt in samplefiles.iteritems():
				xmpfile = XMPFiles()
				xmpfile.open_file( f, **kwargs )
		
	def test_close_file(self):
		for f,fmt in samplefiles.iteritems():
			xmpfile = XMPFiles( file_path=f )
			xmpfile.close_file()	
		
	def test_get_xmp(self):
		for flg in open_flags:
			kwargs = { flg: True }
			for f,fmt in samplefiles.iteritems():
				# See test_exempi_error()
				if not self.flg_fmt_combi(flg,fmt):
					xmpfile = XMPFiles( file_path=f, **kwargs )
					try:
						xmp = xmpfile.get_xmp()
						self.assert_( isinstance(xmp, XMPMeta), "Not an XMPMeta object" )
					except XMPError, e:
						print f
						print flg
						print fmt
					xmpfile.close_file()
					
	def test_can_put_xmp(self):
		for flg in open_flags:
			kwargs = { flg: True }
			for f,fmt in samplefiles.iteritems():
				# See test_exempi_error()
				if not self.flg_fmt_combi(flg,fmt) and not self.exempi_problem(flg, fmt):
					xmpfile = XMPFiles()
					xmpfile.open_file( f, **kwargs )
					xmp = xmpfile.get_xmp()
					if flg == 'open_forupdate':
						self.assert_( xmpfile.can_put_xmp( xmp ) )
					else:
						self.failIf( xmpfile.can_put_xmp( xmp ) )
	
	def test_put_xmp(self):
		pass
		
	def flg_fmt_combi( self, flg, fmt ):
		""" See test_exempi_bad_combinations """	
		is_snow_leopard = platform.system() =='Darwin' and int(platform.release().split(".")[0]) >= 10
		# Note, exempi for OS X 10.6 don't have smart handlers for MOV due to large changes in Quicktime from 10.5 to 10.6  
		
		return (((fmt == XMP_FT_TEXT or fmt == XMP_FT_PDF or fmt == XMP_FT_ILLUSTRATOR or (fmt == XMP_FT_MOV and is_snow_leopard)) and flg == 'open_usesmarthandler' ) or 
				((fmt == XMP_FT_TEXT or fmt == XMP_FT_PDF or (fmt == XMP_FT_MOV and is_snow_leopard)) and flg == 'open_limitscanning' )
				)
				
	def test_exempi_bad_combinations(self):
		""" 
		Certain combinations of formats and open flags will raise an XMPError when you try to open the XMP
		"""
		for flg in open_flags:
			kwargs = { flg: True }
			for f,fmt in samplefiles.iteritems():
				if not self.flg_fmt_combi(flg,fmt):
					xmpfile = XMPFiles()
					xmpfile.open_file( f, **kwargs )
					xmpfile.get_xmp()
				else:
					xmpfile = XMPFiles()
					xmpfile.open_file( f, **kwargs )
					self.assertRaises( XMPError, xmpfile.get_xmp )

	def exempi_problem( self, flg, fmt ):
		""" 
		Special case hazardous for Python because of an exempi bug.
		
		See exempi_error for a test case where this fails.
		"""
		return ((fmt == XMP_FT_TEXT or fmt == XMP_FT_XML) and flg == 'open_forupdate' )
		
	def exempi_error(self):
		""" 
		Test case that exposes an Exempi bug.
		
		Seems like xmp_files_can_put_xmp in exempi is missing a try/catch block.
		
		So loading a sidecar file and call can_put_xmp will kill python interpreter since 
		a C++ exception is thrown.
		"""
		xmpfile = XMPFiles()
		xmpfile.open_file( '.tempsamples/sig05-002a.xmp', open_forupdate = True )
		xmp = xmpfile.get_xmp()
		xmpfile.can_put_xmp( xmp )
		
	def test_write_in_readonly(self):
		# Note, the file should have been opened with "open_forupdate = True"
		# so let's check if XMPMeta is raising an Exception.
		xmpfile = XMPFiles()
		xmpfile.open_file( '.tempsamples/sig05-002a.tif')   
		xmp_data = xmpfile.get_xmp()
		xmp_data.set_property( "http://ns.adobe.com/photoshop/1.0/", 'Headline', "Some really long text blurb which clearly goes longer than 255 characters because it repeats three times because it is some really long text blurb which clearly goes longer than 255 characters because it repeats three times because it is some really long text blurb which clearly goes longer than 255 characters because it repeats three times." )
		self.assertRaises( XMPError, xmpfile.put_xmp, xmp_data )
		self.assertEqual( xmpfile.can_put_xmp( xmp_data ), False )
		#xmp = XMPFiles( file_path="/home/clr/ruby/rails/spitzer.caltech.edu/spec/fixtures/test.tif" )
	
	

def suite():
	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(XMPFilesTestCase))	
	return suite

def test( verbose=2 ):
	all_tests = suite()
	runner = unittest.TextTestRunner(verbosity=verbose)
	result = runner.run(all_tests)
	return result, runner

if __name__ == "__main__":
	#test()
	unittest.main()