Developers
==========
This section is intended for developers of Python XMP Toolkit.

To obtain a source distribution go to GitHub at
https://github.com/python-xmp-toolkit/python-xmp-toolkit and clone the
repository.

Overview of Source Distribution
-------------------------------

 * ``docs/`` -- Source code for documentation.
 * ``libxmp/`` -- Source files for XMP Toolkit
 * ``setup.py`` -- Distutils configuration file.
 * ``MANIFEST.in`` -- Template for MANIFEST file used by Distutils.
 * ``test`` -- Tests

Documentation
-------------
Documentation is prepared using Sphinx Python Documentation Generator (see
http://sphinx.pocoo.org/). To make the documentation run the following command
in the root directory::

  pip install sphinx
  python setup.py build_sphinx

Packaging a Distribution
------------------------
To package a distribution run::

  python setup.py sdist

This will prepare the documentation and use distutils to package together a
distribution that will be placed in ``dist/``.

Running Tests
-------------
Tests are run by issuing the command::

  python setup.py test

For test coverage, run::

  pip install coverage
  source run-coverage.sh

To run tests in Python 2.6, 2.7, or python3, using tox, run::

  pip install tox
  tox

Distribution Configuration
--------------------------
The file ``setup.py`` specify how the distribution is packed together. Most
important to note is that version in formation is read from ``libxmp.version``
file, and that the file ``MANIFEST.in`` specifies which other files to include
in the distribution besides the Python source.

References for Developers
-------------------------
 * `ctypes <http://docs.python.org/lib/module-ctypes.html>`_
 * `Sphinx <http://sphinx.pocoo.org/contents.html>`_
 * `Distutils <http://docs.python.org/dist/dist.html>`_
