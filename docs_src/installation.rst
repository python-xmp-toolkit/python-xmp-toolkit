Installation
============

Requirements
------------

 * Python 2.5+
 * Exempi 2.1.1
 * Linux or OS X (see notes below for Windows)


Python XMP Toolkit
----------------------
The short version of installation is::

  python setup.py install

Note, in case you haven't installed Exempi you will get an :exc:`ExempiLoadError` exception once you try to load :mod:`libxmp`.

Exempi
------
Python XMP Toolkit requires Exempi 2.1.1 which can be downloaded from
http://libopenraw.freedesktop.org/wiki/Exempi. To install Exempi, unpack the
distribution and run::

  ./configure
  make
  sudo make install


Mac OS X 
--------
Note Exempi requires boost (http://www.boost.org/) to compile, so on OS X you probably need to run configure with one of the following options.::

  ./configure --with-darwinports
  ./configure --with-fink 

.. warning::
   Only Exempi 2.1.1 compiles on OS X and Exempi 2.1.1 also fixes an issue over 2.1 that could lead to complete crash of the 
   Python interpreter.
   
.. note::
   Exempi 2.1.1 uses the Carbon version of QuickTime API. In Mac OS X 10.6 however Carbon support for QuickTime was dropped, so Exempi 2.1.1
   will no longer compile out-of-the-box on Snow Leopard. If you install Exempi via MacPorts, then a patch for this problem is automatically 
   fixed.  

Windows 
-------
The library has not been tested on Windows, and nor has any serious effort been made to test it. Hence, developers wanting to use the library on Windows are encouraged to try it out and let us know if it works. 

The library ought to work on Windows, if Exempi can be compiled as a DLL using e.g. Cygwin.