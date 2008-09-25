Welcome
=======

*Python XMP Toolkit* is a library for working with `XMP <http://www.adobe.com/products/xmp/>`_ metadata, as well as reading/writing XMP metadata stored in many different file formats. 

**Authors:**
 * Lars Holm Nielsen <lnielsen@eso.org>
 * Federico Caboni <federico.caboni@me.com>
 * Fabien Chereau <fchereau@eso.org>

.. warning::

	The library is at the moment in an unusable state. A development sprint is going on to bring the library up in a feature complete usable state. Further updates will follow just after the sprint. 
	
	In case you want to test the library, you need to install Exempi first (http://libopenraw.freedesktop.org/wiki/Exempi). Be aware that only Exempi version 2.0.2 compiles on Mac, as version 2.0.1 where using compiler features not available for GCC on OS X. We suggest installing Exempi's own dependencies (i.e.: Boost) using the excellent MacPorts (formerly known as Darwin Ports). The library is being tested with OS X and Linux (Ubuntu) for the moment: Microsoft Windows is not currently supported, and it's unclear whether it will ever be (depends on if we manage to compile Exempi on Windows, which is quite low on our priority list right now). Further documentation can be found in docs_src/ in the source code.

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
