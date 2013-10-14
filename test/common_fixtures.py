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
import pkg_resources
import shutil

import libxmp

samplefiles = {
    'sig05-002a.tif'  : libxmp.consts.XMP_FT_TIFF,
    'sig05-002a.xmp'  : libxmp.consts.XMP_FT_TEXT,
    'BlueSquare.ai'   : libxmp.consts.XMP_FT_ILLUSTRATOR,
    'BlueSquare.avi'  : libxmp.consts.XMP_FT_AVI,
    'BlueSquare.eps'  : libxmp.consts.XMP_FT_EPS,
    'BlueSquare.gif'  : libxmp.consts.XMP_FT_GIF,
    'BlueSquare.indd' : libxmp.consts.XMP_FT_INDESIGN,
    'BlueSquare.jpg'  : libxmp.consts.XMP_FT_JPEG,
    'BlueSquare.mov'  : libxmp.consts.XMP_FT_MOV,
    'BlueSquare.mp3'  : libxmp.consts.XMP_FT_MP3,
    'BlueSquare.pdf'  : libxmp.consts.XMP_FT_PDF,
    'BlueSquare.png'  : libxmp.consts.XMP_FT_PNG,
    'BlueSquare.psd'  : libxmp.consts.XMP_FT_PHOTOSHOP,
    'BlueSquare.tif'  : libxmp.consts.XMP_FT_TIFF,
    'BlueSquare.wav'  : libxmp.consts.XMP_FT_WAV,
}

def setup_sample_files(dirname):
    """
    Copy test files so that we are free to write to them.

    Parameters
    ----------
    dirname : str
        Destination directory, should be temporary.

    Returns
    -------
    Tuple of fully-qualified filenames and their formats.
    """
    copied_samplefiles = []
    fmts = []
    for samplefile, fmt in samplefiles.items():
        relsrc = os.path.join('samples', samplefile)
        full_source_file = pkg_resources.resource_filename(__name__, relsrc)
        dest_file = os.path.join(dirname, samplefile)
        shutil.copyfile(full_source_file, dest_file)
        copied_samplefiles.append(dest_file)
        fmts.append(fmt)
    return copied_samplefiles, fmts

