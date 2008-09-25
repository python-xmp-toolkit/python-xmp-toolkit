Installation
============

Requirements
------------

 * Python 2.5+
 * Exempi


Python XMP Toolkit
----------------------
The short version of installation is::

  python setup.py install

Note, in case you haven't installed Exempi you will get an :exc:`ExempiLoadError` exception once you try to load :mod:`libxmp`.

Exempi
------
Python XMP Toolkit requires Exempi 2.0.2 which can be downloaded from
http://libopenraw.freedesktop.org/wiki/Exempi. To install Exempi, unpack the
distribution and run::

  ./configure
  make
  sudo make install

Note Exempi requires boost (http://www.boost.org/) to compile, and that on OS X
you probably need to run configure with one of the following options.::

  ./configure --with-darwinports
  ./configure --with-fink 

Also, note that versions of Exempi prior to 2.0.2 does not compile on OS X.