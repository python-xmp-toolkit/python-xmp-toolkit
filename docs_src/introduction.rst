Introduction
============

*Python XMP/AVM Toolkit* is a library for working with `XMP <http://www.adobe.com/products/xmp/>`_ metadata, as well as reading/writing XMP metadata stored in many different file formats. The library further includes support for working with `Astronomy Visualization Metadata (AVM) <http://www.virtualastronomy.org>`_ -- a metadata standard for print-ready and screen ready astronomical imagery based on XMP.

Python XMP/AVM Toolkit is wrapping `Exempi <http://libopenraw.freedesktop.org/wiki/Exempi>`_ (using `ctypes <http://docs.python.org/lib/module-ctypes.html>`_), a C/C++ XMP library based on `Adobe XMP Toolkit <http://www.adobe.com/devnet/xmp/>`_, ensuring that future updates to the XMP standard are easily incorporated into the library with a minimum amount of work.

Python XMP/AVM Toolkit has been developed by:
 * `ESA/Hubble - European Space Agency <http://www.spacetelescope.org>`_ 
 * `ESO - European Southern Observatory <http://www.eso.org>`_

Feature Overview
----------------
The XMP features provided are similar to that of Adobe XMP Toolkit, which are:

 * Support for parsing, manipulating, and serializing XMP data.
 * Support for locating the XMP in a file, adding XMP to a file, or updating the XMP in a file.
 * Support for nearly any file format with smart file handlers for JPEG, TIFF, PNG, PSD, MPEG, AVI, MOV, MP3, WAV, PostScript, PDF and InDesign.
 * An API very similar to Adobe XMP Toolkit.


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

What is AVM?
------------
The astronomical education and public outreach (EPO) community plays a key role in conveying the results of scientific research to the general public. A key product of EPO development is a variety of non-scientific public image resources, both derived from scientific observations and created as artistic visualizations of scientific results. This refers to general image formats such as JPEG, TIFF, PNG, GIF, not scientific FITS datasets. Such resources are currently scattered across the internet in a variety of galleries and archives, but are not searchable in any coherent or unified way.

Just as Virtual Observatory (VO) standards open up all data archives to a common query engine, the EPO community will benefit greatly from a similar mechanism for image search and retrieval. Existing metadata standards for the Virtual Observatory are tailored to the management of research datasets and only cover EPO resources (like publication quality imagery) at the “collection” level and are thus insufficient for the needs of the EPO community. 

The primary focus of the AVM is on print-ready and screen ready astronomical imagery, which has been rendered from telescopic observations (also known as “pretty pictures”). Such images can combine data acquired at different wavebands and from different observatories. While the primary intent is to cover data-derived astronomical images, there are broader uses as well. Specifically, the most general subset of this schema is also appropriate for describing artwork and illustrations of astronomical subject matter. This is covered in some detail in later sections.

The intended users of astronomical imagery cover a broad variety of fields: educators, students, journalists, enthusiasts, and scientists. The core set of required tags define the key elements needed in a practical database for identification of desired resources.  For example, one might choose to search for images of the Crab Nebula that include both X-ray and visible light elements, or for any images within 2 degrees of a specified location on the sky that include at least some data from the Spitzer Space Telescope.

Future plans include “multimedia modules” and “planetarium modules” into the AVM standard.

