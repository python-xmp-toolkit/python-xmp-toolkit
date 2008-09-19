# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, European Space Agency & European Southern Observatory (ESA/ESO)
# Copyright (c) 2008, CRS4 - Centre for Advanced Studies, Research and Development in Sardinia
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

import os
import shutil
import sys
sys.path.append('../')

import libxmp

#
# The 
#
open_flags = [
	libxmp.files.XMP_OPEN_NOOPTION,  #< No open option
	libxmp.files.XMP_OPEN_READ, #< Open for read-only access.
	libxmp.files.XMP_OPEN_FORUPDATE, #< Open for reading and writing.
	libxmp.files.XMP_OPEN_ONLYXMP, #< Only the XMP is wanted, allows space/time optimizations.
	libxmp.files.XMP_OPEN_CACHETNAIL, #< Cache thumbnail if possible,  GetThumbnail will be called.
	libxmp.files.XMP_OPEN_STRICTLY, #< Be strict about locating XMP and reconciling with other forms. 
	libxmp.files.XMP_OPEN_USESMARTHANDLER, #< Require the use of a smart handler.
	libxmp.files.XMP_OPEN_USEPACKETSCANNING, #< Force packet scanning, don't use a smart handler.
	libxmp.files.XMP_OPEN_LIMITSCANNING, #< Only packet scan files "known" to need scanning.
	libxmp.files.XMP_OPEN_INBACKGROUND,
]


sampledir = '.tempsamples/'
""" Name of temporary sample directory. """

"""
Definitions of test files
"""
samplefiles = {
	'sig05-002a.tif' : libxmp.files.XMP_FT_TIFF,
	'sig05-002a.xmp' : libxmp.files.XMP_FT_TEXT,
	'BlueSquare.ai' : libxmp.files.XMP_FT_ILLUSTRATOR,
	'BlueSquare.avi' : libxmp.files.XMP_FT_AVI,
	'BlueSquare.eps' : libxmp.files.XMP_FT_EPS,
	'BlueSquare.gif' : libxmp.files.XMP_FT_GIF,
	'BlueSquare.indd' : libxmp.files.XMP_FT_INDESIGN,
	'BlueSquare.jpg' : libxmp.files.XMP_FT_JPEG,
	'BlueSquare.mov' : libxmp.files.XMP_FT_MOV,
	'BlueSquare.mp3' : libxmp.files.XMP_FT_MP3,
	'BlueSquare.pdf' : libxmp.files.XMP_FT_PDF,
	'BlueSquare.png' : libxmp.files.XMP_FT_PNG,
	'BlueSquare.psd' : libxmp.files.XMP_FT_PHOTOSHOP,
	'BlueSquare.tif' : libxmp.files.XMP_FT_TIFF,
	'BlueSquare.wav' : libxmp.files.XMP_FT_WAV,
}

files = {}
for k,v in samplefiles.iteritems():
	files[sampledir + k] = v
samplefiles = files

def make_temp_samples():
	global sampledir
	if os.path.exists( sampledir ):
		remove_temp_samples()
		
	shutil.copytree('samples', sampledir)
	
def remove_temp_samples():
	global sampledir
	if os.path.exists( sampledir ):
		if not os.path.isdir( sampledir):
			raise StandardError('Cannot remove .tempsamples - it is not a directory. Please manually remove it.')
		shutil.rmtree( sampledir )