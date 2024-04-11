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
 * ``pyproject.toml`` -- Packaging configuration file.
 * ``MANIFEST.in`` -- Template for MANIFEST file used by Distutils.
 * ``test`` -- Tests

Documentation
-------------
Documentation is prepared using Sphinx Python Documentation Generator (see
http://sphinx.pocoo.org/). To make the documentation run the following command
in the root directory::

  pip install sphinx
  sphinx-build docs/ docs/_build/

Publishing a release
------------------------
To publish a release run::

  flit publish

For further details see `Flit <https://flit.pypa.io/en/stable/cmdline.html#flit-publish>`_

Running Tests
-------------
Tests are run by issuing the command::

  python -m pytest

For test coverage, run::

  pip install pytest-cov
  python -m pytest --cov

Distribution Configuration
--------------------------
The file ``pyproject.toml`` specifies how the distribution is packed together. Most
important to note is that version in formation is read from ``libxmp.version``
file, and that the file ``MANIFEST.in`` specifies which other files to include
in the distribution besides the Python source.

References for Developers
-------------------------
 * `ctypes <http://docs.python.org/lib/module-ctypes.html>`_
 * `Sphinx <https://www.sphinx-doc.org/en/master/>`_
 * `Flit <https://flit.pypa.io/en/stable/>`_
