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

import os
import os.path
import shutil
import sys
sys.path.append(os.path.pardir)

import libxmp

#
# 
#
open_flags = [
	'open_nooption',
	'open_read',
	'open_forupdate',
	'open_onlyxmp',
	'open_cachetnail',
	'open_strictly',
	'open_usesmarthandler',
	'open_usepacketscanning',
	'open_limitscanning',
	'open_inbackground'
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