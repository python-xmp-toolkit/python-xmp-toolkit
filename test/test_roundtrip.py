# -*- coding: utf-8 -*-
"""
Test suite for round trip workflows.
"""

import datetime
import os
import pkg_resources
import platform
import shutil
import sys
import tempfile

import pytz

if sys.hexversion >= 0x02070000:
    import unittest
else:
    import unittest2 as unittest

from libxmp import XMPFiles, XMPMeta
from libxmp.consts import XMP_NS_CC as NS_CC
from libxmp.consts import XMP_NS_DC as NS_DC
from libxmp.consts import XMP_NS_EXIF as NS_EXIF
from libxmp.consts import XMP_NS_TIFF as NS_TIFF
from libxmp.consts import XMP_NS_XMP as NS_XAP


class TestRoundTrip(unittest.TestCase):

    def test_tiff(self):
        """Write to a TIFF that does not already have the XMP tag."""
        srcfile = pkg_resources.resource_filename(__name__,
                                                  "fixtures/zeros.tif")
        with tempfile.NamedTemporaryFile(suffix='.tif') as tfile:
            shutil.copyfile(srcfile, tfile.name)

            xmpf = XMPFiles()
            xmpf.open_file(file_path=tfile.name, open_forupdate=True)

            # Since it's a TIFF, it already has everything possible from the
            # TIFF IFD filled in into the TIFF namespace.
            xmp = xmpf.get_xmp()
            xmp.set_property(NS_DC, "rights", "no one in particular")
            xmpf.put_xmp(xmp)
            xmpf.close_file()

            xmpf.open_file(file_path=tfile.name)
            xmp = xmpf.get_xmp()
            xmpf.close_file()

            # TODO:  explain why this happened.
            prop = xmp.get_property(NS_DC, "rights")
            prop2 = xmp.get_localized_text(NS_DC, "rights", None, "x-default")
            self.assertEqual(prop2, "no one in particular")


    def test_sturm_und_drang(self):
        """Should be able to write a property which includes umlauts."""
        srcfile = pkg_resources.resource_filename(__name__,
                                                  "fixtures/zeros.tif")
        with tempfile.NamedTemporaryFile(suffix='.tif') as tfile:
            shutil.copyfile(srcfile, tfile.name)
 
            expected_value = u'Stürm und Drang'

            xmpf = XMPFiles()
            xmpf.open_file(file_path=tfile.name, open_forupdate=True)
            xmp = xmpf.get_xmp()
            xmp.set_property(NS_DC, "Title", expected_value)
            xmpf.put_xmp(xmp)
            xmpf.close_file()

            xmpf = XMPFiles()
            xmpf.open_file(file_path=tfile.name)
            xmp = xmpf.get_xmp()
            actual_value = xmp.get_property(NS_DC, "Title")
            xmpf.close_file()
            
            self.assertEqual(actual_value, expected_value)


    def test_jpeg(self):
        """Create XMP from scratch to store in a jpeg."""

        srcfile = pkg_resources.resource_filename(__name__,
                                                  "samples/BlueSquare.jpg")
        with tempfile.NamedTemporaryFile(suffix='.tif', mode='wb') as tfile:

            # Do some surgery on the file, remove existing xmp.
            # The APP1 marker segment in question starts at byte 2156, has 
            # length of 4813
            with open(srcfile, 'rb') as infptr:

                # Write the SOI marker
                tfile.write(infptr.read(2))

                # Skip over ALL the APP0, APP1 segments.
                infptr.seek(21619)
                tfile.write(infptr.read())
                tfile.flush()


            xmpf = XMPFiles()
            xmpf.open_file(file_path=tfile.name, open_forupdate=True)
            xmp = xmpf.get_xmp()

            xmp.set_property(NS_DC, "Title", u'Stürm und Drang')

            # Construct the properties that would have been filled in had the
            # APP0 segment been left in place.
            xmp.set_property(NS_TIFF, "Orientation", "1")
            xmp.set_property(NS_TIFF, "XResolution", "720000/10000")
            xmp.set_property(NS_TIFF, "YResolution", "720000/10000")
            xmp.set_property(NS_TIFF, "ResolutionUnit", "2")
            xmpf.put_xmp(xmp)
            xmpf.close_file()

            xmpf = XMPFiles()
            xmpf.open_file(file_path=tfile.name)
            xmp = xmpf.get_xmp()

            prop = xmp.get_property(NS_DC, "Title")
            self.assertEqual(prop, u'Stürm und Drang')

            prop = xmp.get_property(NS_TIFF, "Orientation")
            self.assertEqual(prop, "1")

            prop = xmp.get_property(NS_TIFF, "XResolution")
            self.assertEqual(prop, "720000/10000")

            prop = xmp.get_property(NS_TIFF, "YResolution")
            self.assertEqual(prop, "720000/10000")

            prop = xmp.get_property(NS_TIFF, "ResolutionUnit")
            self.assertEqual(prop, "2")

            xmpf.close_file()


