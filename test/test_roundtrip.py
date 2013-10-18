"""
Test suite for round trip workflows.
"""

import datetime
import os
import pkg_resources
import shutil
import sys
import tempfile

if sys.hexversion >= 0x02070000:
    import unittest
else:
    import unittest2 as unittest

try:
    import skimage
    relpath = os.path.join('data', 'multipage.tif')
    skimage_tiff = pkg_resources.resource_filename(skimage.__name__, relpath)
except ImportError:
    skimage_tiff = None

import pytz

from libxmp import XMPFiles, XMPMeta
from libxmp.consts import XMP_NS_CC as NS_CC
from libxmp.consts import XMP_NS_DC as NS_DC
from libxmp.consts import XMP_NS_EXIF as NS_EXIF
from libxmp.consts import XMP_NS_TIFF as NS_TIFF
from libxmp.consts import XMP_NS_XMP as NS_XAP


class TestRoundTrip(unittest.TestCase):

    @unittest.skipIf(skimage_tiff is None, "scikits-image tiff not available")
    def test_tiff(self):
        """Create a tiff from scratch with the intent of writing the XMP tag."""

        with tempfile.NamedTemporaryFile(suffix='.tif') as tfile:
            shutil.copyfile(skimage_tiff, tfile.name)

            xmpf = XMPFiles()
            xmpf.open_file(file_path=tfile.name, open_forupdate=True)
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


    def test_jpeg(self):
        """Create XMP from scratch to store in a jpeg."""

        filename = pkg_resources.resource_filename(__name__,
                                                   "samples/BlueSquare.jpg")
        with tempfile.NamedTemporaryFile(suffix='.tif') as tfile:
            shutil.copyfile(filename, tfile.name)

            # Do some surgery on the file, remove existing xmp.

            xmpf = XMPFiles()
            xmpf.open_file(file_path=tfile.name, open_forupdate=True)
            xmp = xmpf.get_xmp()


