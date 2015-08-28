Appendix
========

Known Issues
------------
 * The exempi library can add XMP to PDF files that already have an XMP packet
   but cannot inject XMP into PDFs that do not; therefore, neither can the
   Python XMP Toolkit. 
 * The exempi library routines "xmp_files_check_file_format" and
   "files_get_file_info" are not available on Cygwin.  This does not affect
   the functionality of the high-level XMPMeta or XMPFiles objects.

Resources
---------
 * Project website -- https://github.com/python-xmp-toolkit/python-xmp-toolkit
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
.. include:: ../LICENSE


Changes
-------

.. include:: ../CHANGELOG
