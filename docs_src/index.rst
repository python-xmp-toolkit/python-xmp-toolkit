Welcome
=======

*Python XMP/AVM Toolkit* is a library for working with `XMP <http://www.adobe.com/products/xmp/>`_ metadata, as well as reading/writing XMP metadata stored in many different file formats. The library further includes support for working with `Astronomy Visualization Metadata (AVM) <http://www.virtualastronomy.org>`_ -- a metadata standard for print-ready and screen ready astronomical imagery based on XMP.

**Authors:**
 * Lars Holm Nielsen <lnielsen@eso.org>

.. warning::

	Library is under heavy development at the moment - in case you want to test it, you need to install Exempi first (http://libopenraw.freedesktop.org/wiki/Exempi). We are testing against Exempi version 2.0.1. Also note that to make Exempi compile on OS X, you need to apply a patch to the file exempi/exempi.cpp in the distribution. The library has only been tested on OS X for the moment - it will probably run on Linux. Windows is however not support, and it's unclear whether it will be (depends on if we manage to compile Exempi on Windows).

Documentation
=============

.. toctree::
   :maxdepth: 3
   
   introduction
   installation
   using
   reference
   developers
   appendix   

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
