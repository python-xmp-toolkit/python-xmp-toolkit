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

import datetime
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

import pytz

import libxmp
from libxmp import XMPFiles, XMPMeta, XMPError
from libxmp.utils import file_to_dict, object_to_dict

from .common_fixtures import setup_sample_files
from . import xmpcoverage

from libxmp.consts import XMP_ITERATOR_OPTIONS, XMP_SKIP_OPTIONS
from libxmp.consts import XMP_NS_XMP as NS_XAP
from libxmp.consts import XMP_NS_CC as NS_CC
from libxmp.consts import XMP_NS_DC as NS_DC
from libxmp.consts import XMP_NS_EXIF as NS_EXIF
from libxmp.consts import XMP_NS_TIFF as NS_TIFF
from libxmp.consts import XMP_NS_CameraRaw as NS_CAMERA_RAW_SETTINGS
from libxmp.consts import XMP_NS_Photoshop as NS_PHOTOSHOP

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
        xmp.parse_from_str(xmpcoverage.RDFCoverage, xmpmeta_wrap=True )

        prop = xmp.get_property(xmpcoverage.NS1, "SimpleProp2" )
        self.assertEqual(prop, "Simple2 value" )

        ltext = xmp.get_localized_text(xmpcoverage.NS1,
                                       "ArrayProp2", 'x-one', 'x-one' )
        self.assertEqual(ltext, "Item2.1 value" )


        del xmp

    def test_parse_str(self):
        xmp = XMPMeta()
        xmp.parse_from_str( xmpcoverage.RDFCoverage, xmpmeta_wrap=True )
        prop = xmp.get_property( xmpcoverage.NS1, "SimpleProp1" )
        self.assertEqual(prop, "Simple1 value" )
        self.assertEqual(prop, u"Simple1 value" )
        del xmp

    def test_shorthand_rdf(self):
        """
        Tests pass so long as no error is issued.
        """
        xmp = XMPMeta()
        xmp.parse_from_str( xmpcoverage.ShorthandRDF, xmpmeta_wrap=True )
        prop = xmp.get_property( "http://ns.adobe.com/tiff/1.0", "Model" )
        self.assertEqual(prop, "Canon PowerShot S300" )
        del xmp

    def test_serialize_str(self):
        xmp = XMPMeta()
        xmp.parse_from_str( xmpcoverage.RDFCoverage, xmpmeta_wrap=True )

        obj = xmp.serialize_to_str(use_compact_format=True,
                                   omit_packet_wrapper=True)

        if sys.hexversion >= 0x03000000:
            the_unicode_type = str
        else:
            the_unicode_type = unicode
        self.assertTrue(isinstance(obj, the_unicode_type))

        with self.assertRaises(XMPError):
            xmp.serialize_to_str(read_only_packet=True,
                                 omit_packet_wrapper=True)

        with self.assertRaises(XMPError):
            xmp.serialize_to_str(include_thumbnail_pad=True,
                                 omit_packet_wrapper=True)

        with self.assertRaises(XMPError):
            xmp.serialize_to_str(exact_packet_length=True,
                                 omit_packet_wrapper=True)
        del xmp

    def test_serialize_unicode(self):
        """
        Return type is unicode in 2.7, but str in 3.x
        """
        xmp = XMPMeta()
        xmp.parse_from_str(xmpcoverage.RDFCoverage, xmpmeta_wrap=True)
        if sys.hexversion >= 0x03000000:
            the_unicode_type = str
        else:
            the_unicode_type = unicode

        obj = xmp.serialize_to_unicode(use_compact_format=True,
                                       omit_packet_wrapper=False)
        self.assertTrue(isinstance(obj, the_unicode_type ),
                        "Incorrect string result type." )

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

    def test_serialize_and_format(self):
        xmp = XMPMeta()
        xmp.parse_from_str(xmpcoverage.RDFCoverage, xmpmeta_wrap=True)

        obj = xmp.serialize_and_format(padding=0,
                                       newlinechr='NEWLINE',
                                       tabchr = 'TAB',
                                       indent=6 )
        if sys.hexversion >= 0x03000000:
            the_unicode_type = str
        else:
            the_unicode_type = unicode
        self.assertTrue(isinstance(obj, the_unicode_type),
                        "Result is not the correct string" )

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
        files = ["fixtures/BlueSquare450.xmp",
                 "fixtures/BlueSquare450.tif"]
        options = ['open_nooption',        'open_read',
                   'open_forupdate',       'open_onlyxmp',
                   'open_cachetnail',      'open_strictly',
                   'open_usesmarthandler', 'open_usepacketscanning',
                   'open_limitscanning',]
        for f in files:
            for o in options:
                try:
                    xmpfile = XMPFiles( file_path=f, ** { o : True } )
                    xmp_data = xmpfile.get_xmp()
                    headline = xmp_data.get_property(NS_PHOTOSHOP, 'Headline')

                    self.assertEqual(headline[-5:], "=END=")
                    self.assertTrue(len(headline) > 450,
                                    "Not all text was extracted."  )
                except ((IOError, XMPError)):
                    pass


    def test_text_property_450(self):
        xmp = XMPMeta()
        xmp.parse_from_str( xmpcoverage.LongTextProperty, xmpmeta_wrap=True )
        headline = xmp.get_property("http://ns.adobe.com/photoshop/1.0/",
                                    'Headline' )
        self.assertEqual( headline[-5:], "=END="  )
        self.assertTrue(len(headline) > 450,
                        "Not all text was extracted from headline property.")


    def test_does_property_exist(self):
        filename = pkg_resources.resource_filename(__name__,
                                                   "fixtures/BlueSquare450.tif")
        xmp = XMPFiles(file_path=filename)
        xmp_data = xmp.get_xmp()
        self.assertTrue( xmp_data.does_property_exist( "http://ns.adobe.com/photoshop/1.0/", 'Headline' ) )


    def test_write_new_property(self):
        """Corresponds to test-write-new-property.cpp"""

        filename = pkg_resources.resource_filename(__name__,
                                                   "samples/test1.xmp")

        with open(filename, 'r') as fptr:
            strbuffer = fptr.read()

        xmp = XMPMeta()
        xmp.parse_from_str(strbuffer, xmpmeta_wrap=False)

        XMPMeta.register_namespace(NS_CC, "cc")
        reg_prefix = XMPMeta.get_namespace_for_prefix("cc")
        self.assertEqual(reg_prefix, NS_CC)

        reg_prefix = XMPMeta.get_prefix_for_namespace(NS_CC)
        self.assertEqual(reg_prefix, "cc:")

        xmp.set_property(NS_CC, "License", "Foo")
        self.assertEqual(xmp.get_property(NS_CC, "License"), "Foo")

        the_dt = datetime.datetime(2005, 12, 25, 12, 42, 42, tzinfo=pytz.utc)
        xmp.set_property_datetime(NS_EXIF, "DateTimeOriginal", the_dt)
        self.assertEqual(xmp.get_property(NS_EXIF, "DateTimeOriginal"),
                         "2005-12-25T12:42:42")

        prop = xmp.get_property_datetime(NS_EXIF, "DateTimeOriginal")
        self.assertEqual(prop.year, 2005)
        self.assertEqual(prop.minute, 42)
        self.assertEqual(prop.tzinfo, pytz.utc)


    def test_exempi_core(self):
        """Corresponds to test_exempi.TestExempi.test_exempi_core"""
        filename = pkg_resources.resource_filename(__name__,
                                                   "samples/test1.xmp")
        with open(filename, 'r') as fptr:
            strbuffer = fptr.read()

        xmp = XMPMeta()
        xmp.parse_from_str(strbuffer)

        self.assertTrue(xmp.does_property_exist(NS_TIFF, 'Make'))
        self.assertFalse(xmp.does_property_exist(NS_TIFF, 'Foo'))

        prop = xmp.get_property(NS_TIFF, 'Make')
        self.assertEqual(prop, 'Canon')

        xmp.set_property(NS_TIFF, 'Make', 'Leica')
        prop = xmp.get_property(NS_TIFF, 'Make')
        self.assertEqual(prop, 'Leica')

        # Some tests correspond to option masks not currently returned via
        # this interface.
        item = xmp.get_localized_text(NS_DC, 'rights', None, 'x-default')
        self.assertEqual(item, "2006, Hubert Figuiere")

        xmp.set_localized_text(NS_DC, 'rights', 'en', 'en-CA', 'Foo bar')
        item = xmp.get_localized_text(NS_DC, 'rights', 'en', 'en-US')

        # Can't look at the actual lang, unlike the original test.
        self.assertEqual(item, 'Foo bar')

        xmp.delete_localized_text(NS_DC, 'rights', 'en', 'en-CA')
        self.assertFalse(xmp.does_property_exist(NS_DC, "rights[1]"))

        xmp.set_array_item(NS_DC, "creator", 2, "foo")
        xmp.append_array_item(NS_DC, "creator", "bar")

        prop = xmp.get_array_item(NS_DC, "creator", 3)
        self.assertEqual(prop, "bar")

        xmp.delete_property(NS_DC, "creator[3]")
        self.assertFalse(xmp.does_property_exist(NS_DC, "creator[3]"))

        prop = xmp.get_property(NS_EXIF, "DateTimeOriginal")
        self.assertEqual(prop, "2006-12-07T23:20:43-05:00")

        the_prop = xmp.get_property_datetime(NS_EXIF, "DateTimeOriginal")
        self.assertEqual(the_prop.year, 2006) 
        self.assertEqual(the_prop.minute, 20)
        self.assertEqual(the_prop.tzinfo, pytz.utc)

        prop = xmp.get_property(NS_XAP, "Rating")
        self.assertEqual(prop, "3")

        prop = xmp.get_property_float(NS_CAMERA_RAW_SETTINGS, "SharpenRadius")
        self.assertEqual(prop, 1.0)

        xmp.set_property_float(NS_CAMERA_RAW_SETTINGS, "SharpenRadius", 2.5)
        prop = xmp.get_property_float(NS_CAMERA_RAW_SETTINGS, "SharpenRadius")
        self.assertEqual(prop, 2.5)

        prop = xmp.get_property_bool(NS_CAMERA_RAW_SETTINGS, "AlreadyApplied")
        self.assertFalse(prop)
        xmp.set_property_bool(NS_CAMERA_RAW_SETTINGS, "AlreadyApplied", True)
        prop = xmp.get_property_bool(NS_CAMERA_RAW_SETTINGS, "AlreadyApplied")
        self.assertTrue(prop)

        prop = xmp.get_property_int(NS_EXIF, "MeteringMode")
        self.assertEqual(prop, 5)
        xmp.set_property_int(NS_EXIF, "MeteringMode", 10)
        prop = xmp.get_property_long(NS_EXIF, "MeteringMode")
        self.assertEqual(prop, 10)
        xmp.set_property_long(NS_EXIF, "MeteringMode", 32)
        prop = xmp.get_property_int(NS_EXIF, "MeteringMode")
        self.assertEqual(prop, 32)


    def test_does_array_item_exist(self):
        """Tests XMPMeta method does_array_item_exist.  Issue #03"""
        filename = pkg_resources.resource_filename(__name__,
                                                   "samples/test1.xmp")
        with open(filename, 'r') as fptr:
            strbuffer = fptr.read()

        xmp = XMPMeta()
        xmp.parse_from_str(strbuffer)

        xmp.set_array_item(NS_DC, "creator", 2, "foo")
        xmp.append_array_item(NS_DC, "creator", "bar")

        self.assertTrue(xmp.does_array_item_exist(NS_DC, "creator", "foo"))
        self.assertFalse(xmp.does_array_item_exist(NS_DC, "creator", "blah"))

    
    def test_count_array_items(self):
        """Tests XMPMeta method count_array_items."""
        filename = pkg_resources.resource_filename(__name__,
                                                   "samples/test1.xmp")
        with open(filename, 'r') as fptr:
            strbuffer = fptr.read()

        xmp = XMPMeta()
        xmp.parse_from_str(strbuffer)

        xmp.set_array_item(NS_DC, "creator", 2, "foo")
        xmp.append_array_item(NS_DC, "creator", "bar")
        xmp.append_array_item(NS_DC, "creator", "donuts")
        self.assertEqual(xmp.count_array_items(NS_DC, "creator"), 4)

    def test_skip(self):
        """Verify usage of XMPMeta skip method.
        """
        filename = pkg_resources.resource_filename(__name__,
                                                   "samples/test1.xmp")
        with open(filename, 'r') as fptr:
            strbuffer = fptr.read()

        xmp = XMPMeta()
        xmp.parse_from_str(strbuffer)

        iterator = iterator = iter(xmp)

        schemas = []
        paths = []
        props = []

        for schema, path, prop, options in iterator:

            if schema == NS_TIFF:
                iterator.skip(iter_skipsubtree=True)
            else:
                schemas.append(schema)
                paths.append(path)
                props.append(prop)

        # If the iteration modification worked, there should be no TIFF 
        # properties in the list of schemas.
        self.assertTrue(NS_TIFF not in schemas)
        self.assertTrue(NS_EXIF in schemas)
    

class UtilsTestCase(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.samplefiles, self.formats = setup_sample_files(self.tempdir)

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def test_object_to_dict(self):
        for filename in self.samplefiles:
            xmpfile = XMPFiles( file_path=filename )
            xmp = xmpfile.get_xmp()
            self.assertTrue( object_to_dict( xmp ), "Not an XMPMeta object" )
            xmpfile.close_file()

    def test_file_to_dict(self):
        for filename in self.samplefiles:
            self.assertTrue( file_to_dict(filename), "Expected dictionary" )

    def test_file_to_dict_nofile(self):
        self.assertRaises( IOError, file_to_dict, "nonexistingfile.ext" )

    def test_file_to_dict_noxmp(self):
        filename = pkg_resources.resource_filename(__name__,
                                                   "fixtures/empty.txt")
        self.assertEqual( file_to_dict(filename), {} )

    def test_object_to_dict_noxmp(self):
        self.assertEqual( object_to_dict( [] ), {} )



class NegativeTestCases(unittest.TestCase):

    def test_delete_property(self):
        """
        Verify the deleting a phony property does not raise an exception.
        """
        xmp = XMPMeta()
        xmp.parse_from_str(xmpcoverage.RDFCoverage, xmpmeta_wrap=True )
        xmp.delete_property(xmpcoverage.NS1, "NotReallyThere" )

    def test_delete_property_bad_schema(self):
        """
        Specifying a bad schema trigger an exception.
        """
        xmp = XMPMeta()
        xmp.parse_from_str(xmpcoverage.RDFCoverage, xmpmeta_wrap=True )
        with self.assertRaises(XMPError):
            xmp.delete_property("not really a schema", "NotReallyThere" )


class UnicodeTestCase(unittest.TestCase):

    # TODO:  need a latin-1 case, both positive and negative.
    def test_get_localized_text(self):
        """
        Verify that unicode string literals are properly interpreted.
        """
        xmp = XMPMeta()
        xmp.parse_from_str(xmpcoverage.RDFCoverage, xmpmeta_wrap=True )

        prop = xmp.get_property(xmpcoverage.NS1, "SimpleProp2" )
        self.assertEqual(prop, u'Simple2 value' )

        ltext = xmp.get_localized_text(xmpcoverage.NS1,
                                       "ArrayProp2", 'x-one', 'x-one' )
        self.assertEqual(ltext, u'Item2.1 value' )


        del xmp


    def test_2bytes_codepoint(self):
        """
        Verify that we can create and read back utf-8 where some characters
        takes 2 bytes to encode.
        """
        xmp = XMPMeta()
        rdf = xmpcoverage.RDFCoverage

        # Replace 'Simple2 value' with 'stürm'
        # ü has code point 252, so takes 5+1=6 bytes to encode.
        expectedValue = u'stürm'
        if sys.hexversion < 0x03000000:
            rdf = unicode(rdf[0:272]) + expectedValue + unicode(rdf[285:])
        else:
            rdf = rdf[0:272] + expectedValue + rdf[285:]

        xmp.parse_from_str(rdf, xmpmeta_wrap=True )

        prop = xmp.get_property(xmpcoverage.NS1, "SimpleProp2" )
        self.assertEqual(prop, expectedValue)

        del xmp

    def test_parse_from_str_3_bytes_per_codepoint(self):
        """
        Verify that we can create and read back utf-8 where each character
        takes 3 bytes to encode.
        """
        xmp = XMPMeta()
        rdf = xmpcoverage.RDFCoverage

        # Replace 'Simple2 value' with 'शिव'
        # This is 'Shiva' in Devanagari
        # शिव has code points [2358, 2367, 2357]
        expectedValue = u'शिव'
        if sys.hexversion < 0x03000000:
            rdf = unicode(rdf[0:272]) + expectedValue + unicode(rdf[285:])
            #rdf = rdf[0:272] + expectedValue.encode('utf-8') + rdf[285:]
            #rdf = unicode(rdf)
        else:
            rdf = rdf[0:272] + expectedValue + rdf[285:]

        xmp.parse_from_str(rdf, xmpmeta_wrap=True )

        prop = xmp.get_property(xmpcoverage.NS1, "SimpleProp2" )
        self.assertEqual(prop, expectedValue)

        del xmp

    def test_libxmp_version(self):
        """Verify that the version attribute is accessible."""
        self.assertTrue(hasattr(libxmp, '__version__'))

    def test_xmpmeta_str(self):
        """In 2.7, str must return a byte string.  In 3.x, it is a str."""
        xmp = XMPMeta()
        xmp.set_property(NS_DC, "Title", 'Huckleberry Finn')
        self.assertTrue(isinstance(str(xmp), str))

        xmp = XMPMeta()
        xmp.set_property(NS_DC, "Title", u'Stürm und Drang')
        self.assertTrue(isinstance(str(xmp), str))

        # Something in Devanagari
        xmp = XMPMeta()
        xmp.set_property(NS_DC, "Title", u'शिव')
        self.assertTrue(isinstance(str(xmp), str))

    def test_xmpmeta_repr(self):
        """Should be a str in both 2.x and 3.x"""
        xmp = XMPMeta()
        self.assertTrue(isinstance(repr(xmp), str))

    def test_xmpmeta_unicode_27(self):
        """In 2.7, unicode(xmp) should return a unicode object."""
        xmp = XMPMeta()
        rdf = xmpcoverage.RDFCoverage
        xmp.parse_from_str(rdf)
        if sys.hexversion < 0x03000000:
            self.assertTrue(isinstance(unicode(xmp), unicode))
        else:
            # It's a no-op in 3.x.
            self.assertTrue(True)

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
