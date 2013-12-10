# -*- coding: utf-8 -*-
"""
Test suites for exempi routine wrappers.
"""

# R0904:  Not too many methods in unittest.
# pylint: disable=R0904

import datetime
import os
import pkg_resources
import platform
import shutil
import sys
import tempfile

if sys.hexversion >= 0x02070000:
    import unittest
else:
    import unittest2 as unittest

import pytz

import libxmp
from libxmp import consts
from libxmp import exempi
from libxmp.consts import XMP_NS_CC as NS_CC
from libxmp.consts import XMP_NS_DC as NS_DC
from libxmp.consts import XMP_NS_EXIF as NS_EXIF
from libxmp.consts import XMP_NS_Photoshop as NS_PHOTOSHOP
from libxmp.consts import XMP_NS_TIFF as NS_TIFF
from libxmp.consts import XMP_NS_XMP as NS_XAP
from libxmp.consts import XMP_NS_CameraRaw as NS_CAMERA_RAW_SETTINGS
from libxmp.consts import XMP_ITERATOR_OPTIONS, XMP_SERIAL_OPTIONS
from libxmp.consts import XMP_SKIP_OPTIONS
from libxmp.consts import XMP_CLOSE_SAFEUPDATE, XMP_CLOSE_NOOPTION
from libxmp.consts import XMP_OPEN_READ, XMP_OPEN_FORUPDATE
from libxmp.consts import XMP_PROP_HAS_QUALIFIERS, XMP_PROP_IS_QUALIFIER
from libxmp.consts import XMP_PROP_COMPOSITE_MASK


class TestInit(unittest.TestCase):
    """Corresponds to testinit.cpp.

    Run this test separately because it makes multiple calls to xmp_init and
    xmp_terminate.
    """
    def test_init(self):
        """TODO:  fill in the docstring"""
        filename = pkg_resources.resource_filename(__name__,
                                                   "samples/test1.xmp")
        with open(filename, 'r') as fptr:
            strbuffer = fptr.read()

        exempi.init()
        exempi.init()

        xmp = exempi.new_empty()
        exempi.parse(xmp, strbuffer)
        exempi.free(xmp)

        exempi.terminate()

        xmp = exempi.new_empty()
        exempi.parse(xmp, strbuffer)
        exempi.free(xmp)

        exempi.terminate()
        self.assertTrue(True)

class TestPythonXmpToolkit(unittest.TestCase):
    """
    Test suite for cases added by python xmp toolkit devs.
    """
    def test_file_not_there_open_new(self):
        """
        The library does not catch comfortably, so we perform our own check.
        """
        with self.assertRaises(IOError):
            xfptr = exempi.files_open_new('notthere.xmp', XMP_OPEN_READ)

    def test_file_not_there_check_file_format(self):
        """
        The library does not catch comfortably, so we perform our own check.
        """
        with self.assertRaises(IOError):
            exempi.files_check_file_format('notthere.xmp')

class TestExempi(unittest.TestCase):
    """
    Test suite for libexempi routine wrappers.
    """
    def setUp(self):
        exempi.init()

    def tearDown(self):
        exempi.terminate()

    def test_bgo(self):
        """Corresponds to test-bgo.cpp
        """
        filename = pkg_resources.resource_filename(__name__,
                                                   "samples/fdo18635.jpg")
        xfptr = exempi.files_open_new(filename, XMP_OPEN_READ)
        xmp = exempi.files_get_new_xmp(xfptr)
        exempi.free(xmp)
        exempi.files_free(xfptr)
        self.assertTrue(True)

    def test_write_new_property(self):
        """Corresponds to test-write-new-property.cpp"""
        filename = pkg_resources.resource_filename(__name__,
                                                   "samples/test1.xmp")

        with open(filename, 'r') as fptr:
            strbuffer = fptr.read()

        xmp = exempi.new_empty()
        self.assertFalse(exempi.get_error())

        exempi.parse(xmp, strbuffer)
        self.assertFalse(exempi.get_error())

        reg_prefix = exempi.register_namespace(NS_CC, "cc")
        self.assertEqual("cc:", reg_prefix)

        reg_prefix = exempi.prefix_namespace_uri("cc")
        self.assertEqual(NS_CC, reg_prefix)

        reg_prefix = exempi.namespace_prefix(NS_CC)
        self.assertEqual("cc:", reg_prefix)

        exempi.set_property(xmp, NS_CC, "License", "Foo", 0)
        the_prop, _ = exempi.get_property(xmp, NS_CC, "License")
        self.assertEqual(the_prop, "Foo")

        the_dt = datetime.datetime(2005, 12, 25, 12, 42, 42, tzinfo=pytz.utc)
        exempi.set_property_date(xmp, NS_EXIF, "DateTimeOriginal", the_dt, 0)
        the_prop, _ = exempi.get_property(xmp, NS_EXIF, "DateTimeOriginal")
        self.assertEqual("2005-12-25T12:42:42", the_prop)

        the_prop, _ = exempi.get_property_date(xmp, NS_EXIF, "DateTimeOriginal")
        self.assertEqual(the_prop.year, 2005)
        self.assertEqual(the_prop.minute, 42)
        self.assertEqual(the_prop.tzinfo, pytz.utc)

        exempi.free(xmp)


    def test_3(self):
        """Corresponds to test3.cpp"""
        filename = pkg_resources.resource_filename(__name__,
                                                   "samples/test1.xmp")
        with open(filename, 'r') as fptr:
            strbuffer = fptr.read()
        xmp = exempi.new_empty()
        exempi.parse(xmp, strbuffer)

        options = XMP_ITERATOR_OPTIONS['iter_justleafnodes']
        iterator = exempi.iterator_new(xmp, None, None, options)

        schemas = []
        paths = []
        props = []

        while True:
            try:
                schema, path, prop, _ = exempi.iterator_next(iterator)

                schemas.append(schema)
                paths.append(path)
                props.append(prop)

            except StopIteration:
                break

        exempi.iterator_free(iterator)
        exempi.free(xmp)


    def test_exempi_core(self):
        """According to test-exempi-core.cpp"""
        filename = pkg_resources.resource_filename(__name__,
                                                   "samples/test1.xmp")
        with open(filename, 'r') as fptr:
            strbuffer = fptr.read()
        xmp = exempi.new_empty()
        exempi.parse(xmp, strbuffer)
        self.assertTrue(exempi.has_property(xmp, NS_TIFF, 'Make'))
        self.assertFalse(exempi.has_property(xmp, NS_TIFF, 'Foo'))

        prop, mask = exempi.get_property(xmp, NS_TIFF, 'Make')
        self.assertEqual(prop, "Canon")

        exempi.set_property(xmp, NS_TIFF, "Make", "Leica", 0)
        prop, mask = exempi.get_property(xmp, NS_TIFF, 'Make')
        self.assertEqual(prop, "Leica")

        # Retrieves xml:lang attribute value of 1st rights element
        prop, mask = exempi.get_property(xmp, NS_DC, "rights[1]/?xml:lang")
        self.assertTrue(mask & XMP_PROP_IS_QUALIFIER)

        prop, mask = exempi.get_property(xmp, NS_DC, "rights[1]")
        self.assertTrue(mask & XMP_PROP_HAS_QUALIFIERS)

        item, mask, actual_lang = exempi.get_localized_text(xmp, NS_DC,
                                                            "rights",
                                                            None, "x-default")
        self.assertEqual(item, "2006, Hubert Figuiere")
        self.assertEqual(actual_lang, "x-default")

        exempi.set_localized_text(xmp, NS_DC, "rights",
                                  "en", "en-CA", "Foo bar", 0)

        # Ask for a US alternative.
        item, mask, actual_lang = exempi.get_localized_text(xmp, NS_DC,
                                                            "rights",
                                                            "en", "en-US")
        # And we only got the "en-CA" as the only "en"
        self.assertNotEqual(actual_lang, "en-US")
        self.assertEqual(actual_lang, "en-CA")
        # Check its value
        self.assertEqual(item, "Foo bar")

        # Remove the property x-default.
        exempi.delete_localized_text(xmp, NS_DC, "rights", "en", "en-CA")
        self.assertFalse(exempi.has_property(xmp, NS_DC, "rights[1]"))
        self.assertFalse(exempi.has_property(xmp, NS_DC, "rights[1]"))

        exempi.set_array_item(xmp, NS_DC, "creator", 2, "foo", 0)
        the_prop, bits = exempi.get_array_item(xmp, NS_DC, "creator", 2)
        self.assertTrue((bits & XMP_PROP_COMPOSITE_MASK) == 0)

        exempi.append_array_item(xmp, NS_DC, "creator", 0, "bar", 0)
        the_prop, bits = exempi.get_array_item(xmp, NS_DC, "creator", 3)
        self.assertTrue((bits & XMP_PROP_COMPOSITE_MASK) == 0)
        self.assertEqual(the_prop, "bar")

        exempi.delete_property(xmp, NS_DC, "creator[3]")
        self.assertFalse(exempi.has_property(xmp, NS_DC, "creator[3]"))

        the_prop, _ = exempi.get_property(xmp, NS_EXIF, "DateTimeOriginal")
        self.assertEqual(the_prop, "2006-12-07T23:20:43-05:00")

        # When the time information is read back, it is UTC.
        the_prop, _ = exempi.get_property_date(xmp, NS_EXIF, "DateTimeOriginal")
        self.assertEqual(the_prop.year, 2006)
        self.assertEqual(the_prop.minute, 20)
        self.assertEqual(the_prop.tzinfo, pytz.utc)

        the_prop, _ = exempi.get_property(xmp, NS_XAP, "Rating")
        self.assertEqual(the_prop, "3")

        # testing float get set
        the_prop, _ = exempi.get_property_float(xmp,
                                                NS_CAMERA_RAW_SETTINGS,
                                                "SharpenRadius")
        self.assertEqual(the_prop, 1.0)
        exempi.set_property_float(xmp, NS_CAMERA_RAW_SETTINGS,
                                  "SharpenRadius", 2.5, 0)
        the_prop, _ = exempi.get_property_float(xmp, NS_CAMERA_RAW_SETTINGS,
                                                "SharpenRadius")
        self.assertEqual(the_prop, 2.5)

        # testing bool get set
        the_prop, _ = exempi.get_property_bool(xmp, NS_CAMERA_RAW_SETTINGS,
                                               "AlreadyApplied")
        self.assertFalse(the_prop)
        exempi.set_property_bool(xmp, NS_CAMERA_RAW_SETTINGS,
                                 "AlreadyApplied", True, 0)
        the_prop, _ = exempi.get_property_bool(xmp, NS_CAMERA_RAW_SETTINGS,
                                               "AlreadyApplied")
        self.assertTrue(the_prop)


        # testing int get set
        the_prop, _ = exempi.get_property_int32(xmp, NS_EXIF, "MeteringMode")
        self.assertEqual(the_prop, 5)
        exempi.set_property_int32(xmp, NS_EXIF, "MeteringMode", 10, 0)
        the_prop, _ = exempi.get_property_int64(xmp, NS_EXIF, "MeteringMode")
        self.assertEqual(the_prop, 10)
        exempi.set_property_int64(xmp, NS_EXIF, "MeteringMode", 32, 0)
        the_prop, _ = exempi.get_property_int32(xmp, NS_EXIF, "MeteringMode")
        self.assertEqual(the_prop, 32)


        exempi.free(xmp)
        self.assertTrue(True)


    def test_xmpfiles_write(self):
        """According to test-xmpfiles-write.cpp"""
        filename = pkg_resources.resource_filename(__name__,
                                                   "samples/BlueSquare.jpg")

        fmt = exempi.files_check_file_format(filename)
        self.assertEqual(fmt, libxmp.consts.XMP_FT_JPEG)

        xfptr = exempi.files_open_new(filename, XMP_OPEN_READ)
        xmp = exempi.files_get_new_xmp(xfptr)
        exempi.files_free(xfptr)

        with tempfile.NamedTemporaryFile(suffix=".jpg") as tfile:
            shutil.copyfile(filename, tfile.name)

            xfptr = exempi.files_open_new(tfile.name, XMP_OPEN_FORUPDATE)

            exempi.set_property(xmp, NS_PHOTOSHOP, "ICCProfile", "foo", 0)
            self.assertTrue(exempi.files_can_put_xmp(xfptr, xmp))
            exempi.files_put_xmp(xfptr, xmp)
            exempi.free(xmp)
            exempi.files_close(xfptr, XMP_CLOSE_SAFEUPDATE)
            exempi.files_free(xfptr)

            xfptr = exempi.files_open_new(tfile.name, XMP_OPEN_READ)
            xmp = exempi.files_get_new_xmp(xfptr)
            the_prop, _ = exempi.get_property(xmp, NS_PHOTOSHOP, "ICCProfile")
            self.assertEqual("foo", the_prop)

            exempi.free(xmp)
            exempi.files_close(xfptr, XMP_CLOSE_NOOPTION)
            exempi.files_free(xfptr)


    def test_serialize(self):
        """Corresponds to test-serialize.cpp"""
        filename = pkg_resources.resource_filename(__name__,
                                                   "samples/test1.xmp")
        with open(filename, 'r') as fptr:
            strbuffer = fptr.read()

        self.assertFalse(exempi.get_error())

        xmp = exempi.new_empty()
        self.assertFalse(exempi.get_error())

        exempi.parse(xmp, strbuffer)
        self.assertFalse(exempi.get_error())

        options = XMP_SERIAL_OPTIONS['omit_packet_wrapper']
        # TODO:  test this somehow.
        output = exempi.serialize_and_format(xmp, options, 0, '\n', ' ', 0)
        self.assertFalse(exempi.get_error())

        exempi.free(xmp)


    def test_tiff_leak(self):
        """Corresponds to test-tiff-leak.cpp"""
        orig_file = pkg_resources.resource_filename(__name__,
                                                    "samples/BlueSquare.tif")

        with tempfile.NamedTemporaryFile(suffix='.tif') as tfile:
            shutil.copyfile(orig_file, tfile.name)

            xfptr = exempi.files_open_new(tfile.name, XMP_OPEN_FORUPDATE)

            xmp = exempi.files_get_new_xmp(xfptr)
            exempi.set_localized_text(xmp, NS_DC, "description", "en", "en-US",
                                      "foo", 0)
            exempi.files_put_xmp(xfptr, xmp)
            exempi.files_close(xfptr, XMP_CLOSE_NOOPTION)
            exempi.free(xmp)
            exempi.files_free(xfptr)
        self.assertTrue(True)


    def test_write_new_date_property(self):
        """
        TODO:  fill in the doc string
        """
        filename = pkg_resources.resource_filename(__name__,
                                                   "samples/test1.xmp")

        with open(filename, 'r') as fptr:
            strbuffer = fptr.read()

        xmp = exempi.new_empty()
        self.assertFalse(exempi.get_error())

        exempi.parse(xmp, strbuffer)
        self.assertFalse(exempi.get_error())

        the_dt = datetime.datetime(2005, 12, 25, 12, 42, 42)

        exempi.set_property_date(xmp, NS_EXIF, "DateTimeOriginal", the_dt, 0)
        the_prop, _ = exempi.get_property(xmp, NS_EXIF, "DateTimeOriginal")
        self.assertEqual("2005-12-25T12:42:42", the_prop)

        the_prop, _ = exempi.get_property_date(xmp, NS_EXIF, "DateTimeOriginal")
        self.assertEqual(the_prop.year, 2005)
        self.assertEqual(the_prop.minute, 42)
        self.assertEqual(the_prop, datetime.datetime(2005, 12, 25, 12, 42, 42,
                                   tzinfo=pytz.utc))

        exempi.free(xmp)



    def test_xmp_files(self):
        """Corresponds to test_xmp_files.cpp"""
        filename = pkg_resources.resource_filename(__name__,
                                                   "samples/BlueSquare.jpg")

        xfptr = exempi.files_open_new(filename, XMP_OPEN_READ)
        fmt = exempi.files_check_file_format(filename)
        self.assertEqual(fmt, libxmp.consts.XMP_FT_JPEG)

        file_path, options, file_format, flags = exempi.files_get_file_info(xfptr)
        self.assertEqual(options, XMP_OPEN_READ)
        self.assertEqual(file_format, libxmp.consts.XMP_FT_JPEG)
        self.assertEqual(flags, 0x27f)  # 0x27f?
        self.assertEqual(filename, file_path)

        xmp = exempi.files_get_xmp(xfptr)
        the_prop, _ = exempi.get_property(xmp, NS_PHOTOSHOP, "ICCProfile")
        self.assertEqual(the_prop, "sRGB IEC61966-2.1")
        exempi.files_free(xfptr)

    def test_formats(self):
        """Verify that check_file_format function works as expected."""
        pairs = { 'avi':  libxmp.consts.XMP_FT_AVI,
                  'eps':  libxmp.consts.XMP_FT_EPS,
                  'gif':  libxmp.consts.XMP_FT_GIF,
                  'indd': libxmp.consts.XMP_FT_INDESIGN,
                  'jpg':  libxmp.consts.XMP_FT_JPEG,
                  'mov':  libxmp.consts.XMP_FT_MOV,
                  'mp3':  libxmp.consts.XMP_FT_MP3,
                  'png':  libxmp.consts.XMP_FT_PNG,
                  'psd':  libxmp.consts.XMP_FT_PHOTOSHOP,
                  'tif':  libxmp.consts.XMP_FT_TIFF,
                  'wav':  libxmp.consts.XMP_FT_WAV,
                  }
        for suffix, expected_format in pairs.items():
            relpath = os.path.join('samples', 'BlueSquare' + '.' + suffix)
            filename = pkg_resources.resource_filename(__name__, relpath)
            xfptr = exempi.files_open_new(filename, XMP_OPEN_READ)
            actual_format = exempi.files_check_file_format(filename)
            self.assertEqual(actual_format, expected_format)
            exempi.files_free(xfptr)


    @unittest.skip("Issue 26")
    def test_bad_formats(self):
        """Verify check_file_format on PDF, Adobe Illustrator, XMP."""
        # Issue 26
        filename = pkg_resources.resource_filename(__name__,
                                                   "samples/BlueSquare.pdf")
        xfptr = exempi.files_open_new(filename, XMP_OPEN_READ)
        fmt = exempi.files_check_file_format(filename)
        self.assertEqual(fmt, libxmp.consts.XMP_FT_PDF)
        exempi.files_free(xfptr)

        filename = pkg_resources.resource_filename(__name__,
                                                   "samples/BlueSquare.ai")
        xfptr = exempi.files_open_new(filename, XMP_OPEN_READ)
        fmt = exempi.files_check_file_format(filename)
        self.assertEqual(fmt, libxmp.consts.XMP_FT_ILLUSTRATOR)
        exempi.files_free(xfptr)

        filename = pkg_resources.resource_filename(__name__,
                                                   "samples/BlueSquare.xmp")
        xfptr = exempi.files_open_new(filename, XMP_OPEN_READ)
        fmt = exempi.files_check_file_format(filename)
        self.assertEqual(fmt, libxmp.consts.XMP_FT_XML)
        exempi.files_free(xfptr)


class TestIteration(unittest.TestCase):
    """
    Test suite for iteration configurations.
    """
    def setUp(self):
        exempi.init()

    def collect_iteration(self, schema, prop, options):
        """Run thru an iteration for a given configuration."""
        filename = pkg_resources.resource_filename(__name__,
                                                   "samples/test1.xmp")
        with open(filename, 'r') as fptr:
            strbuffer = fptr.read()
        xmp = exempi.new_empty()
        exempi.parse(xmp, strbuffer)

        iterator = exempi.iterator_new(xmp, schema, prop, options)

        schemas = []
        paths = []
        props = []

        while True:
            try:
                schema, path, prop, _ = exempi.iterator_next(iterator)

                schemas.append(schema)
                paths.append(path)
                props.append(prop)

            except StopIteration:
                break

        exempi.iterator_free(iterator)
        exempi.free(xmp)


        return schemas, paths, props

    @unittest.skip("Issue 27")
    def test_namespaces(self):
        """Iterate through the namespaces."""
        options = XMP_ITERATOR_OPTIONS['iter_namespaces']
        schemas, paths, props = self.collect_iteration(None, None, options)

    def test_single_namespace_single_path_leaf_nodes(self):
        """Get all the leaf nodes from a single path, single namespace."""
        options = XMP_ITERATOR_OPTIONS['iter_justleafnodes']
        schemas, paths, props = self.collect_iteration(NS_DC, "rights", options)

        for j in range(len(props)):
            self.assertEqual(schemas[j], NS_DC)

        self.assertEqual(paths[0], "dc:rights[1]")
        self.assertEqual(paths[1], "dc:rights[1]/?xml:lang")

        self.assertEqual(props[0], "2006, Hubert Figuiere")
        self.assertEqual(props[1], "x-default")


    def test_single_namespace_single_path_children(self):
        """Get just child nodes from a single path, single namespace."""
        # This does not result in retrieving dc:rights[1]/?xml:lang
        options = XMP_ITERATOR_OPTIONS['iter_justchildren']
        schemas, paths, props = self.collect_iteration(NS_DC, "rights", options)

        self.assertEqual(schemas, [NS_DC])
        self.assertEqual(paths, ["dc:rights[1]"])
        self.assertEqual(props, ["2006, Hubert Figuiere"])


    def test_single_namespace_single_path_leaf_names(self):
        """Get just leaf names from a single path, single namespace."""
        # TODO:  why?
        options = XMP_ITERATOR_OPTIONS['iter_justleafname']
        schemas, paths, props = self.collect_iteration(NS_DC, "rights", options)

        self.assertEqual(schemas, [NS_DC, NS_DC, NS_DC])
        self.assertEqual(paths,
                         ['dc:rights',
                          '[1]',
                          'xml:lang'])
        self.assertEqual(props,
                         ['',
                          '2006, Hubert Figuiere',
                          'x-default'])


    def test_single_namespace_leaf_nodes(self):
        """Get all the leaf nodes from a single namespace."""
        options = XMP_ITERATOR_OPTIONS['iter_justleafnodes']
        schemas, paths, props = self.collect_iteration(NS_DC, None, options)

        for j in range(len(props)):
            self.assertEqual(schemas[j], NS_DC)

        self.assertEqual(paths[0], "dc:creator[1]")
        self.assertEqual(paths[1], "dc:rights[1]")

        # TODO:  why is this one here?
        self.assertEqual(paths[2], "dc:rights[1]/?xml:lang")

        self.assertEqual(paths[3], "dc:subject[1]")
        self.assertEqual(paths[4], "dc:subject[2]")
        self.assertEqual(paths[5], "dc:subject[3]")
        self.assertEqual(paths[6], "dc:subject[4]")

        self.assertEqual(props[0], "unknown")
        self.assertEqual(props[1], "2006, Hubert Figuiere")
        self.assertEqual(props[2], "x-default")
        self.assertEqual(props[3], "night")
        self.assertEqual(props[4], "ontario")
        self.assertEqual(props[5], "ottawa")
        self.assertEqual(props[6], "parliament of canada")

    @unittest.skip("Issue 28.")
    def test_no_namespace_single_prop_leaf_nodes(self):
        """Get all the leaf nodes from a single property."""
        options = XMP_ITERATOR_OPTIONS['iter_justleafnodes']
        schemas, paths, props = self.collect_iteration(None, "rights", options)

    def test_single_namespace_leaf_nodes_omit_qualifiers(self):
        """Get all the leaf nodes (no qualifiers) from a single namespace."""
        # TODO:  explain
        options = XMP_ITERATOR_OPTIONS['iter_justleafnodes']
        options &= XMP_ITERATOR_OPTIONS['iter_omitqualifiers']
        schemas, paths, props = self.collect_iteration(NS_DC, None, options)

        self.assertEqual(schemas, [NS_DC] * 11)
        self.assertEqual(paths, ['',
                                 'dc:creator',
                                 'dc:creator[1]',
                                 'dc:rights',
                                 'dc:rights[1]',
                                 'dc:rights[1]/?xml:lang',
                                 'dc:subject',
                                 'dc:subject[1]',
                                 'dc:subject[2]',
                                 'dc:subject[3]',
                                 'dc:subject[4]'])
        self.assertEqual(props, ['',
                                 '',
                                 'unknown',
                                 '',
                                 '2006, Hubert Figuiere',
                                 'x-default',
                                 '',
                                 'night',
                                 'ontario',
                                 'ottawa',
                                 'parliament of canada'])

    def test_single_namespace_properties(self):
        """Get all the properties from a single namespace."""
        # TODO:  same as above, must explain
        options = XMP_ITERATOR_OPTIONS['iter_properties']
        schemas, paths, props = self.collect_iteration(NS_DC, None, options)

        self.assertEqual(schemas, [NS_DC] * 11)
        self.assertEqual(paths, ['',
                                 'dc:creator',
                                 'dc:creator[1]',
                                 'dc:rights',
                                 'dc:rights[1]',
                                 'dc:rights[1]/?xml:lang',
                                 'dc:subject',
                                 'dc:subject[1]',
                                 'dc:subject[2]',
                                 'dc:subject[3]',
                                 'dc:subject[4]'])
        self.assertEqual(props, ['',
                                 '',
                                 'unknown',
                                 '',
                                 '2006, Hubert Figuiere',
                                 'x-default',
                                 '',
                                 'night',
                                 'ontario',
                                 'ottawa',
                                 'parliament of canada'])

    def test_iter_skip_subtree(self):
        """Alter the iteration midstream."""
        options = XMP_ITERATOR_OPTIONS['iter_properties']

        filename = pkg_resources.resource_filename(__name__,
                                                   "samples/test1.xmp")
        with open(filename, 'r') as fptr:
            strbuffer = fptr.read()
        xmp = exempi.new_empty()
        exempi.parse(xmp, strbuffer)

        iterator = exempi.iterator_new(xmp, None, None, options)

        schemas = []
        paths = []
        props = []

        while True:
            try:
                schema, path, prop, _ = exempi.iterator_next(iterator)

                if schema == NS_TIFF:
                    exempi.iterator_skip(iterator,
                                         XMP_SKIP_OPTIONS['iter_skipsubtree'])
                    continue

                schemas.append(schema)
                paths.append(path)
                props.append(prop)

            except StopIteration:
                break

        exempi.iterator_free(iterator)
        exempi.free(xmp)

        # If the iteration modification worked, there should be no TIFF 
        # properties in the list of schemas.
        self.assertTrue(NS_TIFF not in schemas)
