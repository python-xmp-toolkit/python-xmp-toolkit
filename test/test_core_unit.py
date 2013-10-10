# -*- coding: utf-8 -*-
#
# Copyright (c) 2008-2009, European Space Agency & European Southern
# Observatory (ESA/ESO)
# Copyright (c) 2008-2009, CRS4 - Centre for Advanced Studies, Research and
# Development in Sardinia
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
#       Observatory, CRS4 nor the names of its contributors may be used to
#       endorse or promote products derived from this software without specific
#       prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY ESA/ESO AND CRS4 ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL ESA/ESO BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER # IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE

import sys
if sys.hexversion < 0x02070000:
    import unittest2 as unittest
else:
    import unittest
import os
import os.path
import pkg_resources
import shutil
import tempfile

sys.path.append(os.path.pardir)

from libxmp import *
from libxmp import XMPIterator
from libxmp import _exempi
from libxmp.utils import file_to_dict, object_to_dict

from .common_fixtures import setup_sample_files
from .samples import open_flags
from . import xmpcoverage

class TestClass(object):
    def __unicode__(self):
        return xmpcoverage.RDFCoverage

class XMPMetaTestCase(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.samplefiles, self.formats = setup_sample_files(self.tempdir)

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def test_init_del(self):
        xmp = XMPMeta()
        self.assertTrue( xmp.xmpptr )
        del xmp

    def test_test_files(self):
        for f in self.samplefiles:
            self.assertTrue( os.path.exists(f), "Test file does not exists." )

    def test_get_xmp(self):
        for f in self.samplefiles:
            xmpfile = XMPFiles( file_path=f )
            xmp = xmpfile.get_xmp()
            self.assertTrue( isinstance(xmp, XMPMeta), "Not an XMPMeta object" )
            xmpfile.close_file()

    def test_get_localized_text(self):
        xmp = XMPMeta()
        self.assertTrue(xmp.parse_from_str(xmpcoverage.RDFCoverage,
                                           xmpmeta_wrap=True ),
                        "Could not parse valid string." )

        prop = xmp.get_property(xmpcoverage.NS1, "SimpleProp2" )
        self.assertEqual(prop, "Simple2 value" )

        ltext = xmp.get_localized_text(xmpcoverage.NS1,
                                       "ArrayProp2", 'x-one', 'x-one' )
        self.assertEqual(ltext, "Item2.1 value" )


        del xmp

    def test_parse_str(self):
        xmp = XMPMeta()
        self.assertTrue( xmp.parse_from_str( xmpcoverage.RDFCoverage, xmpmeta_wrap=True ), "Could not parse valid string." )
        self.assertEqual( xmp.get_property( xmpcoverage.NS1, "SimpleProp1" ), "Simple1 value" )
        del xmp

    def test_shorthand_rdf(self):
        xmp = XMPMeta()
        self.assertTrue( xmp.parse_from_str( xmpcoverage.ShorthandRDF, xmpmeta_wrap=True ), "Could not parse valid string." )
        self.assertEqual( xmp.get_property( "http://ns.adobe.com/tiff/1.0", "Model" ), "Canon PowerShot S300" )
        del xmp

    def test_serialize_str(self):
        xmp = XMPMeta()
        self.assertTrue( xmp.parse_from_str( xmpcoverage.RDFCoverage, xmpmeta_wrap=True ), "Could not parse valid string." )
        self.assertTrue( isinstance( xmp.serialize_to_str(use_compact_format=True, omit_packet_wrapper=True), str ), "Result is not a 8-bit string" )
        self.assertRaises( XMPError, xmp.serialize_to_str, read_only_packet=True, omit_packet_wrapper=True )
        self.assertRaises( XMPError, xmp.serialize_to_str, include_thumbnail_pad=True, omit_packet_wrapper=True )
        self.assertRaises( XMPError, xmp.serialize_to_str, exact_packet_length=True, omit_packet_wrapper=True )
        del xmp

    #@unittest.skipIf(sys.hexversion < 0x02070000,
    #                 "Testing infrastructure requires 2.7 or better.")
    def test_serialize_unicode(self):
        xmp = XMPMeta()
        self.assertTrue(xmp.parse_from_str(xmpcoverage.RDFCoverage, xmpmeta_wrap=True),
                        "Could not parse valid string." )
        if sys.hexversion >= 0x03000000:
            the_unicode_type = str
        else:
            the_unicode_type = unicode

        obj = xmp.serialize_to_unicode(use_compact_format=True,
                                       omit_packet_wrapper=False)
        self.assertTrue(isinstance(obj, the_unicode_type ),
                        "Result is not a unicode string" )

        with self.assertRaises(XMPError):
            xmp.serialize_to_unicode(read_only_packet=True,
                                     omit_packet_wrapper=True)

        with self.assertRaises(XMPError):
            xmp.serialize_to_unicode(include_thumbnail_pad=True,
                                     omit_packet_wrapper=True )

        with self.assertRaises(XMPError):
            xmp.serialize_to_unicode(exact_packet_length=True,
                                     omit_packet_wrapper=True )

        del xmp

    #@unittest.skipIf(sys.hexversion < 0x02070000,
    #                 "Testing infrastructure requires 2.7 or better.")
    def test_serialize_and_format(self):
        xmp = XMPMeta()
        self.assertTrue(xmp.parse_from_str(xmpcoverage.RDFCoverage,xmpmeta_wrap=True),
                        "Could not parse valid string." )

        obj = xmp.serialize_and_format(padding=0,
                                       newlinechr='NEWLINE',
                                       tabchr = 'TAB',
                                       indent=6 )
        self.assertTrue(isinstance(obj, str),
                        "Result is not a 8-bit string" )

        with self.assertRaises(XMPError):
            xmp.serialize_and_format(read_only_packet=True,
                                     omit_packet_wrapper=True)

        with self.assertRaises(XMPError):
            xmp.serialize_and_format(include_thumbnail_pad=True,
                                     omit_packet_wrapper=True)

        with self.assertRaises(XMPError):
            xmp.serialize_and_format(exact_packet_length=True,
                                     omit_packet_wrapper=True )

        del xmp

    def test_clone(self):
        xmp1 = XMPMeta()
        self.assertTrue( xmp1 == xmp1, "XMP1 not equal it self" )
        self.assertFalse( xmp1 != xmp1, "XMP1 is equal it self" )
        xmp2 = xmp1.clone()
        self.assertFalse( xmp1 == xmp2, "XMP1 is not equal XMP2" )
        self.assertTrue( xmp1 != xmp2, "XMP1 is not equal XMP2" )
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
                    self.assertTrue( len(headline) > 450, "Not all text was extracted from headline property."  )
                except XMPError as e:
                    pass


    def test_text_property_450(self):
        xmp = XMPMeta()
        self.assertTrue( xmp.parse_from_str( xmpcoverage.LongTextProperty, xmpmeta_wrap=True ), "Could not parse valid string." )
        headline = xmp.get_property( "http://ns.adobe.com/photoshop/1.0/", 'Headline' )
        self.assertEqual( headline[-5:], "=END="  )
        self.assertTrue( len(headline) > 450, "Not all text was extracted from headline property."  )


    def test_does_property_exist(self):
        filename = pkg_resources.resource_filename(__name__,
                                                   "fixtures/BlueSquare450.tif")
        xmp = XMPFiles(file_path=filename)
        xmp_data = xmp.get_xmp()
        self.assertTrue( xmp_data.does_property_exist( "http://ns.adobe.com/photoshop/1.0/", 'Headline' ) )


class UtilsTestCase(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.samplefiles, self.formats = setup_sample_files(self.tempdir)

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def test_object_to_dict(self):
        for f in self.samplefiles:
            xmpfile = XMPFiles( file_path=f )
            xmp = xmpfile.get_xmp()
            self.assertTrue( object_to_dict( xmp ), "Not an XMPMeta object" )
            xmpfile.close_file()

    def test_file_to_dict(self):
        for f in self.samplefiles:
            self.assertTrue( file_to_dict( f ), "Expected dictionary" )

    def test_file_to_dict_nofile(self):
        self.assertRaises( IOError, file_to_dict, "nonexistingfile.ext" )

    def test_file_to_dict_noxmp(self):
        filename = pkg_resources.resource_filename(__name__,
                                                   "fixtures/empty.txt")
        self.assertEqual( file_to_dict(filename), {} )

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
