Installation
============

Requirements
------------

 * Python 2.5+
 * Exempi


Python XMP/AVM Toolkit
----------------------
The short version of installation is::

  python setup.py install

Note, in case you haven't installed Exempi you will get an :exc:`ExempiLoadError` exception once you try to load :mod:`libxmp` or :mod:`libavm`.

Exempi
------
Python XMP/AVM Toolkit requires Exempi 2.0.1 which can be downloaded from
http://libopenraw.freedesktop.org/wiki/Exempi. To install Exempi, unpack the
distribution and run::

  ./configure
  make
  sudo make install

Note Exempi requires boost (http://www.boost.org/) to compile and that Exempi
2.0.1 doesn't compile on OS X before the distribution have been patched.