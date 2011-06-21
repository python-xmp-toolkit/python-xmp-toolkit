Appendix
========

Known Issues
------------
 * The TIFF smart handler have troubles reading the XMP packet correctly - this is either due
   to Exempi 2.1.1 being installed via MacPorts or it is a 64-bit issue. To circumvent the problem,
   please use packet scanning when opening a TIFF file::
   
     xmp = XMPFiles(file_path="../test.tif", open_usepacketscanning=True )

Resources
---------
 * Project website -- http://code.google.com/p/python-xmp-toolkit/
 * XMP -- http://www.adobe.com/products/xmp/
 * Exempi -- http://libopenraw.freedesktop.org/wiki/Exempi
 * Adobe XMP Toolkit -- http://www.adobe.com/devnet/xmp/

Glossary
--------

.. glossary::

	XMP
		eXtensible Metadata Platform

TODO list
---------

.. todolist::

License
-------
Copyright (c) 2008-2009, European Space Agency & European Southern Observatory (ESA/ESO)

Copyright (c) 2008-2009, CRS4 - Centre for Advanced Studies, Research and Development in Sardinia
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.

    * Neither the name of the European Space Agency, European Southern 
      Observatory, CRS4 nor the names of its contributors may be used to endorse or 
      promote products derived from this software without specific prior 
      written permission.

THIS SOFTWARE IS PROVIDED BY ESA/ESO AND CRS4 ``AS IS'' AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
EVENT SHALL ESA/ESO BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.


Changes
-------
Release 1.0.2 ( June 21, 2011 )
  * Fixed python 2.5 issue (ctypes.c_bool are not available in 2.5, so it was changed to ctypes.c_int).
Release 1.0.1 ( April 11, 2011 )
  * Fixed issue on 32-bit systems.
Release 1.0 ( March 31, 2010 )
  * Known issue #7 documented - issue with TIFF smart handler.
  * Fixed issue #15 - 64-bit issues on Linux and Mac.
  * Fixed issue #11 - Typo in does_property_exist.
  * Thanks to marialaura.clemente for bug reports and patches.
Release 1.0rc2 (Feburary 16, 2010)
  * Fixed issue #4, #5 and related to XMPIterator, file_to_dict and object_to_dict. 
  * Fixed issue in file_to_dict which didn't pass parameters to XMPFiles.open_file() properly.
  * Fixed issue #9 file_to_dict now raises IOError instead of returning  
    an empty dictionary for non-existing files. (*backward incompatible*)
  * Fixed issue #8 - spelling mistake in function call in XMPMeta.append_array_items
  * Based on Exempi 2.1.1 and Adobe XMP Toolkit 4.4.2
  * Thanks to olsenpk, pitymushroom, rmarianski, cfarrell1980 for bug reports and patches
**Release 1.0rc1 (March 6, 2009)**
  * Backwards incompatible with previous releases.
  * Based on Exempi 2.1.0 and Adobe XMP Toolkit 4.4.2
  * Initialise and Terminate should no longer be called before usage. 
**Release 1.0beta1 (July 6, 2008)**
  * First public release.