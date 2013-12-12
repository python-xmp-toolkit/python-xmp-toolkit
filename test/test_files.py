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

import os
import os.path
import pkg_resources
import platform
import re
import shutil
import sys
import tempfile
if sys.hexversion < 0x02070000:
    import unittest2 as unittest
else:
    import unittest

if sys.hexversion <= 0x03030000:
    from mock import patch
else:
    from unittest.mock import patch

if sys.hexversion < 0x03000000:
    from StringIO import StringIO
else:
    from io import StringIO

from libxmp import XMPFiles, XMPMeta, XMPError
from libxmp.consts import XMP_NS_Photoshop as NS_PHOTOSHOP
from libxmp.consts import XMP_FT_TEXT
from libxmp.consts import XMP_FT_PDF
from libxmp.consts import XMP_FT_ILLUSTRATOR
from libxmp.consts import XMP_FT_MOV
from libxmp.consts import XMP_FT_XML
from libxmp import exempi
from .common_fixtures import setup_sample_files
from .samples import open_flags

class XMPFilesTestCase(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.samplefiles, self.formats = setup_sample_files(self.tempdir)

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def test_repr(self):
        """Test __repr__ and __str__ on XMPFiles objects."""
        xmpf = XMPFiles()
        self.assertEqual(str(xmpf), 'XMPFiles()')
        self.assertEqual(repr(xmpf), 'XMPFiles()')

        # If the XMPFiles object has a file associated with it, then use a
        # regular expression to match the output.
        filename = pkg_resources.resource_filename(__name__,
                                                   "samples/BlueSquare.jpg")
        xmpf.open_file(file_path=filename)
        actual_value = str(xmpf)

        regex = re.compile(r"""XMPFiles\(file_path=""", re.VERBOSE)
        self.assertIsNotNone(regex.match(actual_value))
        self.assertTrue(actual_value.endswith("BlueSquare.jpg')"))



    def test_print_bom(self):
        """Should be able to print XMP packets despite BOM."""
        # The BOM cannot be decoded from utf-8 into ascii, so a 2.7 XMPMeta
        # object's __repr__ function would error out on it.

        filename = pkg_resources.resource_filename(__name__,
                                                   "samples/BlueSquare.jpg")
        xmpf = XMPFiles()
        xmpf.open_file(file_path=filename)
        xmp = xmpf.get_xmp()
        with patch('sys.stdout', new=StringIO()) as fake_out:
            print(xmp)
            repr(xmp)
        self.assertTrue(True)


    def test_init_del(self):
        xmpfile = XMPFiles()
        self.assertTrue( xmpfile.xmpfileptr )
        del xmpfile

    def test_test_files(self):
        for filename in self.samplefiles:
            self.assertTrue(os.path.exists(filename),
                            "Test file does not exists." )

    def test_open_file(self):
        # Non-existing file.
        xmpfile = XMPFiles()
        with self.assertRaises(IOError):
            xmpfile.open_file('')

        xmpfile = XMPFiles()
        xmpfile.open_file( self.samplefiles[0] )
        self.assertRaises( XMPError, xmpfile.open_file, self.samplefiles[0] )
        self.assertRaises( XMPError, xmpfile.open_file, self.samplefiles[1] )
        xmpfile.close_file()
        xmpfile.open_file( self.samplefiles[1] )
        self.assertRaises( XMPError, xmpfile.open_file, self.samplefiles[0] )

        # Open all sample files.
        for filename in self.samplefiles:
            xmpfile = XMPFiles()
            xmpfile.open_file(filename)

        # Try using init
        for filename in self.samplefiles:
            xmpfile = XMPFiles(file_path=filename)

    def test_open_file_with_options(self):
        """Try all open options"""
        for flg in open_flags:
            kwargs = { flg: True }

            for filename in self.samplefiles:
                if flg == 'open_usesmarthandler':
                    # We know these are problematic.
                    suffices = ('.ai', '.pdf', '.xmp')
                    if filename.lower().endswith(suffices):
                        continue
                if flg == 'open_limitscanning':
                    # We know these are problematic.
                    suffices = ('.pdf', '.xmp')
                    if filename.lower().endswith(suffices):
                        continue
                xmpfile = XMPFiles()
                xmpfile.open_file(filename, **kwargs)

    def test_open_use_smarthandler(self):
        """Verify this library failure."""
        # Issue 5
        filenames = [pkg_resources.resource_filename(__name__,
                                                     "samples/BlueSquare.pdf"),
                     pkg_resources.resource_filename(__name__,
                                                     "samples/BlueSquare.ai"),
                     pkg_resources.resource_filename(__name__,
                                                     "samples/BlueSquare.xmp")]
        xmpfile = XMPFiles()
        for filename in filenames:
            with self.assertRaises(XMPError):
                xmpfile.open_file(filename, open_usesmarthandler=True)


    def test_open_open_limitscanning(self):
        """Verify this library failure."""
        # Issue 5
        filenames = [pkg_resources.resource_filename(__name__,
                                                     "samples/BlueSquare.pdf"),
                     pkg_resources.resource_filename(__name__,
                                                     "samples/BlueSquare.xmp")]
        xmpfile = XMPFiles()
        for filename in filenames:
            with self.assertRaises(XMPError):
                xmpfile.open_file(filename, open_limitscanning=True)


    def test_close_file(self):
        for filename in self.samplefiles:
            xmpfile = XMPFiles( file_path=filename )
            xmpfile.close_file()

    def test_get_xmp(self):
        for flg in open_flags:
            kwargs = { flg: True }
            for filename, fmt in zip(self.samplefiles, self.formats):
                # See test_exempi_error()
                if not self.flg_fmt_combi(flg, fmt):
                    xmpfile = XMPFiles( file_path=filename, **kwargs )
                    try:
                        xmp = xmpfile.get_xmp()
                        self.assertTrue(isinstance(xmp, XMPMeta),
                                        "Not an XMPMeta object" )
                    except XMPError:
                        print(filename)
                        print(flg)
                        print(fmt)
                    xmpfile.close_file()

    def test_can_put_xmp(self):
        for flg in open_flags:
            kwargs = { flg: True }
            for filename, fmt in zip(self.samplefiles, self.formats):
                # See test_exempi_error()
                if (((not self.flg_fmt_combi(flg, fmt)) and
                     (not self.exempi_problem(flg, fmt)))):
                    xmpfile = XMPFiles()
                    xmpfile.open_file( filename, **kwargs )
                    xmp = xmpfile.get_xmp()
                    if flg == 'open_forupdate':
                        self.assertTrue( xmpfile.can_put_xmp( xmp ) )
                    else:
                        self.assertFalse( xmpfile.can_put_xmp( xmp ) )

    def flg_fmt_combi( self, flg, fmt ):
        """ See test_exempi_bad_combinations """
        if flg == 'open_usesmarthandler':
            if fmt in [XMP_FT_TEXT, XMP_FT_PDF, XMP_FT_ILLUSTRATOR]:
                return True

        if flg == 'open_limitscanning':
            if fmt in [XMP_FT_TEXT, XMP_FT_PDF]:
                return True

        return False

    def test_exempi_bad_combinations(self):
        """
        Verify bad combinations of formats and open flags.
        """
        # Certain combinations of formats and open flags will raise an XMPError
        # when you try to open the XMP
        for flg in open_flags:
            kwargs = { flg: True }
            for filename, fmt in zip(self.samplefiles, self.formats):
                if not self.flg_fmt_combi(flg, fmt):
                    xmpfile = XMPFiles()
                    xmpfile.open_file( filename, **kwargs )
                    xmpfile.get_xmp()
                else:
                    xmpfile = XMPFiles()
                    with self.assertRaises(XMPError):
                        xmpfile.open_file( filename, **kwargs )

    def exempi_problem( self, flg, fmt ):
        """
        Special case hazardous for Python because of an exempi bug.

        See exempi_error for a test case where this fails.
        """
        return ((fmt == XMP_FT_TEXT or fmt == XMP_FT_XML) and
                (flg == 'open_forupdate'))

    def exempi_error(self):
        """
        Test case that exposes an Exempi bug.

        Seems like xmp_files_can_put_xmp in exempi is missing a try/catch block.

        So loading a sidecar file and call can_put_xmp will kill python
        interpreter since a C++ exception is thrown.
        """
        filename = pkg_resources.resource_filename(__name__,
                                                   "samples/sig05-002a.xmp")
        xmpfile = XMPFiles()
        xmpfile.open_file(filename, open_forupdate = True )
        xmp = xmpfile.get_xmp()
        xmpfile.can_put_xmp( xmp )

    def test_write_in_readonly(self):
        """If not "open_forupdate = True", should raise exception"""
        # Note, the file should have been opened with "open_forupdate = True"
        # so let's check if XMPMeta is raising an Exception.
        xmpfile = XMPFiles()
        filename = os.path.join(self.tempdir, 'sig05-002a.tif')
        xmpfile.open_file(filename)
        xmp_data = xmpfile.get_xmp()
        xmp_data.set_property( NS_PHOTOSHOP, 'Headline', "Some text")
        self.assertRaises( XMPError, xmpfile.put_xmp, xmp_data )
        self.assertEqual( xmpfile.can_put_xmp( xmp_data ), False )

    def test_tiff_smarthandler(self):
        """Verify action of TIFF smarthandler when tag length > 255"""
        # See issue 12
        srcfile = pkg_resources.resource_filename(__name__,
                                                  "fixtures/zeros.tif")
        with tempfile.NamedTemporaryFile(suffix='.tif') as tfile:
            shutil.copyfile(srcfile, tfile.name)

            # Create a tag with 280 chars.
            xmpf = XMPFiles()
            xmpf.open_file(tfile.name, open_forupdate=True)
            xmp = xmpf.get_xmp()
            blurb = "Some really long text blurb "
            xmp.set_property(NS_PHOTOSHOP, 'Headline', blurb * 10)
            xmpf.put_xmp(xmp)
            xmpf.close_file()

            xmpf.open_file(tfile.name, usesmarthandler=True)
            xmp = xmpf.get_xmp()
            prop = xmp.get_property(NS_PHOTOSHOP, "Headline")
            xmpf.close_file()

            self.assertEqual(prop, blurb * 10)



def suite():
    the_suite = unittest.TestSuite()
    the_suite.addTest(unittest.makeSuite(XMPFilesTestCase))
    return the_suite

def test( verbose=2 ):
    all_tests = suite()
    runner = unittest.TextTestRunner(verbosity=verbose)
    result = runner.run(all_tests)
    return result, runner

if __name__ == "__main__":
    unittest.main()
