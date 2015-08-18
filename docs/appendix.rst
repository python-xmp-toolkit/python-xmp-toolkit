Appendix
========

Known Issues
------------
 * The version of libexempi that comes via Macports refuses to load via ctypes.
   As a workaround, you should compile libexempi from source.
 * The exempi library can add XMP to PDF files that already have an XMP packet
   but cannot inject XMP into PDFs that do not; therefore, neither can the
   Python XMP Toolkit. 

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
