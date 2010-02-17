Introduction
============

*Python XMP Toolkit* is a library for working with `XMP <http://www.adobe.com/products/xmp/>`_ metadata, as well as reading/writing XMP metadata stored in many different file formats. 

Python XMP Toolkit is wrapping `Exempi <http://libopenraw.freedesktop.org/wiki/Exempi>`_ (using `ctypes <http://docs.python.org/lib/module-ctypes.html>`_), a C/C++ XMP library based on `Adobe XMP Toolkit <http://www.adobe.com/devnet/xmp/>`_, ensuring that future updates to the XMP standard are easily incorporated into the library with a minimum amount of work.

Python XMP Toolkit has been developed by:

 * `ESA/Hubble - European Space Agency <http://www.spacetelescope.org>`_ 
 * `ESO - European Southern Observatory <http://www.eso.org>`_
 * `CRS4 - Centre for Advanced Studies, Research and Development in Sardinia <http://www.crs4.it/>`_

Feature Overview
----------------
The XMP features provided are similar to that of Adobe XMP Toolkit, which are:

 * Support for parsing, manipulating, and serializing XMP data.
 * Support for locating the XMP in a file, adding XMP to a file, or updating the XMP in a file.
 * Support for nearly any file format with smart file handlers for JPEG, TIFF, GIF, PNG, PSD, InDesign, MOV, MP3, MPEG2, MPEG4, AVI, FLV, SWF, ASF, PostScript, P2, SonyHDV, AVCHD, UCF, WAV, XDCAM, XDCAMEX.
 * An API very similar to Adobe XMP Toolkit.
 * Based on Exempi 2.1.1 and Adobe XMP Toolkit 4.4.2

Following important features from Adobe XMP Toolkit are not available in Python XMP Toolkit:

  * Localized text support
  * Methods for working with XMP structs.
  * Methods for working with XMP qualifiers
  * Methods for working with XMP Aliases

What is XMP?
------------
The Adobe Extensible Metadata Platform (XMP) specification describes a 
widely used method for embedding descriptive metadata within images. XMP 
tags are stored within the image header of all common image formats (JPEG, 
TIFF, PNG, GIF, PSD) and can be read by popular image processing and 
cataloging packages. The XMP standard is also widely used by photographers 
and the publication industry. Users of consumer and professional digital cameras may already be familiar with Exchangeable Image File Format (EXIF) metadata tags that include camera and exposure information within the digital photo file as a set of XMP tags. In practice an XMP header is a block of XML text included in the header block of the image file and is only supported in image types with header/comment blocks.

The advantages of embedded image identity metadata are numerous. Including 
metadata effectively makes the images self-documenting, which is particularly 
useful when the source URL for an image is lost. This information can now be 
accessed by multimedia management packages, or indexed by databases 
designed to read the embedded information. For instance, an online or desktop 
planetarium program could load an image from the web and extract the 
appropriate metadata to place it in the proper position in the sky. 