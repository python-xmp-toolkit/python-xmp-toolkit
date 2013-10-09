"""
Test suites for exempi routine wrappers.
"""

# R0904:  Not too many methods in unittest.
# pylint: disable=R0904

import pkg_resources
import shutil
import tempfile
import unittest

import libxmp
from libxmp import exempi


class TestBgo(unittest.TestCase):
    """Corresponds to test-bgo.cpp"""
    def test_init(self):
        """
        TODO:  fill in the doc string
        """
        exempi.init()

        filename = pkg_resources.resource_filename(__name__,
                                                   "samples/fdo18635.jpg")
        exempi.init()
        xfptr = exempi.files_open_new(filename, exempi.OpenFileOptions.read)
        self.assertNotEqual(xfptr, 0)

        xmp = exempi.files_get_new_xmp(xfptr)
        exempi.free(xmp)
        exempi.files_free(xfptr)

        exempi.terminate()


class TestInit(unittest.TestCase):
    """Corresponds to testinit.cpp"""
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

class TestExempi(unittest.TestCase):
    """
    Test suite for libexempi routine wrappers.
    """
    def setUp(self):
        exempi.init()

    def tearDown(self):
        exempi.terminate()

    def test_3(self):
        """Corresponds to test3.cpp"""
        filename = pkg_resources.resource_filename(__name__,
                                                   "samples/test1.xmp")
        with open(filename, 'r') as fptr:
            strbuffer = fptr.read()
        xmp = exempi.new_empty()
        exempi.parse(xmp, strbuffer)

        iterator = exempi.iterator_new(xmp, None, None,
                                       exempi.IterOptions.just_leaf_nodes)

        schemas = []
        paths = []
        props = []

        while True:
            try:
                schema, path, prop, _ = exempi.iterator_next(iterator)

                schemas.append(exempi.string_cstr(schema))
                paths.append(exempi.string_cstr(path))
                props.append(exempi.string_cstr(prop))

                exempi.string_free(schema)
                exempi.string_free(path)
                exempi.string_free(prop)

            except StopIteration:
                break

        #for j in range(len(props)):
        #    print('"{0}":  "{1}"  "{2}"'.format(schemas[j],
        #                                        paths[j],
        #                                        props[j]))
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
        self.assertTrue(exempi.has_property(xmp, exempi.NS_TIFF, 'Make'))
        self.assertFalse(exempi.has_property(xmp,
                                             exempi.NS_TIFF,
                                             'Foo'))

        prop, mask = exempi.get_property(xmp, exempi.NS_TIFF, 'Make')
        prop = exempi.string_cstr(prop)
        self.assertEqual(prop, "Canon")

        exempi.set_property(xmp, exempi.NS_TIFF, "Make", "Leica", 0)
        prop, mask = exempi.get_property(xmp, exempi.NS_TIFF, 'Make')
        prop = exempi.string_cstr(prop)
        self.assertEqual(prop, "Leica")

        # Retrieves xml:lang attribute value of 1st rights element
        prop, mask = exempi.get_property(xmp, exempi.NS_DC,
                                         "rights[1]/?xml:lang")
        prop = exempi.string_cstr(prop)
        self.assertTrue(mask & exempi.XmpPropsBits.is_qualifier)

        prop, mask = exempi.get_property(xmp, exempi.NS_DC, "rights[1]")
        self.assertTrue(mask & exempi.XmpPropsBits.has_qualifier)

        item, mask, actual_lang = exempi.get_localized_text(xmp,
                                                            exempi.NS_DC,
                                                            "rights",
                                                            None, "x-default")
        self.assertEqual(exempi.string_cstr(item), "2006, Hubert Figuiere")
        self.assertEqual(exempi.string_cstr(actual_lang), "x-default")

        exempi.set_localized_text(xmp, exempi.NS_DC, "rights",
                                  "en", "en-CA", "Foo bar", 0)

        # Ask for a US alternative.
        item, mask, actual_lang = exempi.get_localized_text(xmp, exempi.NS_DC,
                                                            "rights",
                                                            "en", "en-US")
        # And we only got the "en-CA" as the only "en"
        self.assertNotEqual(exempi.string_cstr(actual_lang), "en-US")
        self.assertEqual(exempi.string_cstr(actual_lang), "en-CA")
        # Check its value
        self.assertEqual(exempi.string_cstr(item), "Foo bar")

        # Remove the property x-default.
        exempi.delete_localized_text(xmp, exempi.NS_DC, "rights",
                                     "en", "en-CA")
        self.assertFalse(exempi.has_property(xmp, exempi.NS_DC, "rights[1]"))
        self.assertFalse(exempi.has_property(xmp, exempi.NS_DC, "rights[1]"))

        exempi.string_free(actual_lang)

        exempi.set_array_item(xmp, exempi.NS_DC, "creator", 2, "foo", 0)
        the_prop, bits = exempi.get_array_item(xmp, exempi.NS_DC,
                                               "creator", 2)
        self.assertTrue(exempi.is_prop_simple(bits))
        exempi.string_free(the_prop)

        exempi.append_array_item(xmp, exempi.NS_DC, "creator", 0, "bar", 0)
        the_prop, bits = exempi.get_array_item(xmp, exempi.NS_DC,
                                               "creator", 3)
        self.assertTrue(exempi.is_prop_simple(bits))
        self.assertEqual(exempi.string_cstr(the_prop), "bar")
        exempi.string_free(the_prop)

        exempi.delete_property(xmp, exempi.NS_DC, "creator[3]")
        self.assertFalse(exempi.has_property(xmp, exempi.NS_DC, "creator[3]"))

        the_prop, _ = exempi.get_property(xmp, exempi.NS_EXIF,
                                          "DateTimeOriginal")
        self.assertEqual(exempi.string_cstr(the_prop),
                         "2006-12-07T23:20:43-05:00")
        exempi.string_free(the_prop)

        the_prop, _ = exempi.get_property_date(xmp, exempi.NS_EXIF,
                                               "DateTimeOriginal")
        self.assertEqual(the_prop.year, 2006)
        self.assertEqual(the_prop.minute, 20)
        self.assertEqual(the_prop.tzSign, exempi.TimeSign.west)

        the_prop, _ = exempi.get_property(xmp, exempi.NS_XAP, "Rating")
        self.assertEqual(exempi.string_cstr(the_prop), "3")
        exempi.string_free(the_prop)

        # testing float get set
        the_prop, _ = exempi.get_property_float(xmp,
                                                exempi.NS_CAMERA_RAW_SETTINGS,
                                                "SharpenRadius")
        self.assertEqual(the_prop, 1.0)
        exempi.set_property_float(xmp, exempi.NS_CAMERA_RAW_SETTINGS,
                                  "SharpenRadius", 2.5, 0)
        the_prop, _ = exempi.get_property_float(xmp,
                                                exempi.NS_CAMERA_RAW_SETTINGS,
                                                "SharpenRadius")
        self.assertEqual(the_prop, 2.5)

        # testing bool get set
        the_prop, _ = exempi.get_property_bool(xmp,
                                               exempi.NS_CAMERA_RAW_SETTINGS,
                                               "AlreadyApplied")
        self.assertFalse(the_prop)
        exempi.set_property_bool(xmp, exempi.NS_CAMERA_RAW_SETTINGS,
                                 "AlreadyApplied", True, 0)
        the_prop, _ = exempi.get_property_bool(xmp,
                                               exempi.NS_CAMERA_RAW_SETTINGS,
                                               "AlreadyApplied")
        self.assertTrue(the_prop)


        # testing int get set
        the_prop, _ = exempi.get_property_int32(xmp, exempi.NS_EXIF,
                                                "MeteringMode")
        self.assertEqual(the_prop, 5)
        exempi.set_property_int32(xmp, exempi.NS_EXIF, "MeteringMode", 10, 0)
        the_prop, _ = exempi.get_property_int64(xmp, exempi.NS_EXIF,
                                                "MeteringMode")
        self.assertEqual(the_prop, 10)
        exempi.set_property_int64(xmp, exempi.NS_EXIF, "MeteringMode", 32, 0)
        the_prop, _ = exempi.get_property_int32(xmp, exempi.NS_EXIF,
                                                "MeteringMode")
        self.assertEqual(the_prop, 32)


        exempi.free(xmp)
        self.assertTrue(True)


    def test_xmpfiles_write(self):
        """According to test-xmpfiles-write.cpp"""
        filename = pkg_resources.resource_filename(__name__,
                                                   "samples/BlueSquare.jpg")

        fmt = exempi.files_check_file_format(filename)
        self.assertEqual(fmt, exempi.FileType.jpeg)

        xfptr = exempi.files_open_new(filename, exempi.OpenFileOptions.read)
        xmp = exempi.files_get_new_xmp(xfptr)
        exempi.files_free(xfptr)

        with tempfile.NamedTemporaryFile(suffix=".jpg") as tfile:
            shutil.copyfile(filename, tfile.name)

            xfptr = exempi.files_open_new(tfile.name,
                                          exempi.OpenFileOptions.for_update)

            exempi.set_property(xmp, exempi.NS_PHOTOSHOP, "ICCProfile", "foo", 0)
            self.assertTrue(exempi.files_can_put_xmp(xfptr, xmp))
            exempi.files_put_xmp(xfptr, xmp)
            exempi.free(xmp)
            exempi.files_close(xfptr, exempi.CloseFileOptions.safe_update)
            exempi.files_free(xfptr)

            xfptr = exempi.files_open_new(tfile.name,
                                          exempi.OpenFileOptions.read)
            xmp = exempi.files_get_new_xmp(xfptr)
            the_prop, _ = exempi.get_property(xmp, exempi.NS_PHOTOSHOP,
                                              "ICCProfile")
            self.assertEqual("foo", exempi.string_cstr(the_prop))
            exempi.string_free(the_prop)

            exempi.free(xmp)
            exempi.files_close(xfptr, exempi.CloseFileOptions.no_option)
            exempi.files_free(xfptr)



class TestSerialize(unittest.TestCase):
    """Corresponds to test-serialize.cpp"""
    def test_serialize(self):
        """
        TODO:  fill in the doc string
        """
        filename = pkg_resources.resource_filename(__name__,
                                                   "samples/test1.xmp")
        with open(filename, 'r') as fptr:
            strbuffer = fptr.read()

        exempi.init()
        self.assertFalse(exempi.get_error())

        xmp = exempi.new_empty()
        self.assertFalse(exempi.get_error())

        exempi.parse(xmp, strbuffer)
        self.assertFalse(exempi.get_error())

        options = exempi.Serialize.omit_packet_wrapper
        xmp_output = exempi.serialize_and_format(xmp, options, 0, '\n', ' ', 0)
        self.assertFalse(exempi.get_error())

        # TODO:  test this somehow.
        output = exempi.string_cstr(xmp_output)

        exempi.string_free(xmp_output)
        exempi.free(xmp)

        exempi.terminate()


class TestTiffLeak(unittest.TestCase):
    """Corresponds to test-tiff-leak.cpp"""
    def test_tiff_leak(self):
        """
        TODO:  fill in the doc string
        """
        orig_file = pkg_resources.resource_filename(__name__,
                                                    "samples/BlueSquare.tif")

        with tempfile.NamedTemporaryFile(suffix='.tif') as tfile:
            shutil.copyfile(orig_file, tfile.name)

            exempi.init()
            xfptr = exempi.files_open_new(tfile.name,
                                          exempi.OpenFileOptions.for_update)

            xmp = exempi.files_get_new_xmp(xfptr)
            exempi.set_localized_text(xmp, exempi.NS_DC, "description",
                                      "en", "en-US", "foo", 0)
            exempi.files_put_xmp(xfptr, xmp)
            exempi.files_close(xfptr, exempi.CloseFileOptions.no_option)
            exempi.free(xmp)
            exempi.files_free(xfptr)
            exempi.terminate()
        self.assertTrue(True)


class TestWriteNewProperty(unittest.TestCase):
    """Corresponds to test-write-new-property.cpp"""
    def test_write_new_property(self):
        """
        TODO:  fill in the doc string
        """
        filename = pkg_resources.resource_filename(__name__,
                                                   "samples/test1.xmp")

        exempi.init()
        with open(filename, 'r') as fptr:
            strbuffer = fptr.read()

        xmp = exempi.new_empty()
        self.assertFalse(exempi.get_error())

        exempi.parse(xmp, strbuffer)
        self.assertFalse(exempi.get_error())

        reg_prefix = exempi.register_namespace(exempi.NS_CC, "cc")
        self.assertEqual("cc:", exempi.string_cstr(reg_prefix))
        exempi.string_free(reg_prefix)

        reg_prefix = exempi.prefix_namespace_uri("cc")
        self.assertEqual(exempi.NS_CC, exempi.string_cstr(reg_prefix))
        exempi.string_free(reg_prefix)

        reg_prefix = exempi.namespace_prefix(exempi.NS_CC)
        self.assertEqual("cc:", exempi.string_cstr(reg_prefix))
        exempi.string_free(reg_prefix)

        exempi.set_property(xmp, exempi.NS_CC, "License", "Foo", 0)
        the_prop, _ = exempi.get_property(xmp, exempi.NS_CC, "License")
        self.assertEqual(exempi.string_cstr(the_prop), "Foo")
        exempi.string_free(the_prop)

        the_dt = exempi.XmpDateTime()
        the_dt.year = 2005
        the_dt.month = 12
        the_dt.day = 25
        the_dt.hour = 12
        the_dt.minute = 42
        the_dt.second = 42
        the_dt.tzSign = exempi.TimeSign.utc
        the_dt.tzHour = 0
        the_dt.tzMinute = 0
        the_dt.nanoSecond = 0

        exempi.set_property_date(xmp, exempi.NS_EXIF, "DateTimeOriginal",
                                 the_dt, 0)
        the_prop, _ = exempi.get_property(xmp, exempi.NS_EXIF,
                                          "DateTimeOriginal")
        self.assertEqual("2005-12-25T12:42:42", exempi.string_cstr(the_prop))
        exempi.string_free(the_prop)

        the_prop, _ = exempi.get_property_date(xmp, exempi.NS_EXIF,
                                               "DateTimeOriginal")
        self.assertEqual(the_prop.year, 2005)
        self.assertEqual(the_prop.minute, 42)
        self.assertEqual(the_prop.tzSign, exempi.TimeSign.utc)

        exempi.free(xmp)

        exempi.terminate()

    def test_write_new_date_property(self):
        """
        TODO:  fill in the doc string
        """
        filename = pkg_resources.resource_filename(__name__,
                                                   "samples/test1.xmp")

        exempi.init()
        with open(filename, 'r') as fptr:
            strbuffer = fptr.read()

        xmp = exempi.new_empty()
        self.assertFalse(exempi.get_error())

        exempi.parse(xmp, strbuffer)
        self.assertFalse(exempi.get_error())

        the_dt = exempi.XmpDateTime()
        the_dt.year = 2005
        the_dt.month = 12
        the_dt.day = 25
        the_dt.hour = 12
        the_dt.minute = 42
        the_dt.second = 42
        the_dt.tzSign = exempi.TimeSign.utc
        the_dt.tzHour = 0
        the_dt.tzMinute = 0
        the_dt.nanoSecond = 0

        exempi.set_property_date(xmp, exempi.NS_EXIF, "DateTimeOriginal",
                                 the_dt, 0)
        the_prop, _ = exempi.get_property(xmp, exempi.NS_EXIF,
                                          "DateTimeOriginal")
        self.assertEqual("2005-12-25T12:42:42", exempi.string_cstr(the_prop))
        exempi.string_free(the_prop)

        the_prop, _ = exempi.get_property_date(xmp, exempi.NS_EXIF,
                                               "DateTimeOriginal")
        self.assertEqual(the_prop.year, 2005)
        self.assertEqual(the_prop.minute, 42)
        self.assertEqual(the_prop.tzSign, exempi.TimeSign.utc)

        exempi.free(xmp)

        exempi.terminate()



class TestXmpFiles(unittest.TestCase):
    """Corresponds to test_xmp_files"""
    def test_xmp_files(self):
        """
        Returns basic information about an XMP file.
        """
        filename = pkg_resources.resource_filename(__name__,
                                                   "samples/BlueSquare.jpg")

        xfptr = exempi.files_open_new(filename, exempi.OpenFileOptions.read)
        exempi.init()

        fmt = exempi.files_check_file_format(filename)
        self.assertEqual(fmt, exempi.FileType.jpeg)

        file_path, options, file_format, flags = exempi.files_get_file_info(xfptr)
        self.assertEqual(options, exempi.OpenFileOptions.read)
        self.assertEqual(file_format, exempi.FileType.jpeg)
        self.assertEqual(flags, 0x27f)  # 0x27f?
        self.assertEqual(filename, exempi.string_cstr(file_path))
        exempi.string_free(file_path)

        xmp = exempi.files_get_xmp(xfptr)
        the_prop, _ = exempi.get_property(xmp, exempi.NS_PHOTOSHOP,
                                          "ICCProfile")
        self.assertEqual(exempi.string_cstr(the_prop), "sRGB IEC61966-2.1")
        exempi.string_free(the_prop)
        exempi.files_free(xfptr)

        exempi.terminate()


class TestFloat(unittest.TestCase):
    """
    Test suite for libexempi routine wrappers.
    """
    def setUp(self):
        exempi.init()

    def tearDown(self):
        exempi.terminate()

    def test_exempi_core(self):
        """According to test-exempi-core.cpp"""
        filename = pkg_resources.resource_filename(__name__,
                                                   "samples/test1.xmp")
        with open(filename, 'r') as fptr:
            strbuffer = fptr.read()
        xmp = exempi.new_empty()
        exempi.parse(xmp, strbuffer)

        # testing float get set
        the_prop, _ = exempi.get_property_float(xmp,
                                                exempi.NS_CAMERA_RAW_SETTINGS,
                                                "SharpenRadius")
        self.assertEqual(the_prop, 1.0)
        exempi.set_property_float(xmp, exempi.NS_CAMERA_RAW_SETTINGS,
                                  "SharpenRadius", 2.5, 0)
        the_prop, _ = exempi.get_property_float(xmp,
                                                exempi.NS_CAMERA_RAW_SETTINGS,
                                                "SharpenRadius")
        self.assertEqual(the_prop, 2.5)

        exempi.free(xmp)
        self.assertTrue(True)
