==================
Python XMP Toolkit
==================

.. image:: actions/workflows/python-package.yml/badge.svg
   :alt: Build status badge
   :target: actions
.. image:: https://img.shields.io/coveralls/python-xmp-toolkit/python-xmp-toolkit/master.svg?maxAge=3600
   :alt: Coverage badge
   :target: https://coveralls.io/r/python-xmp-toolkit/python-xmp-toolkit
.. image:: https://img.shields.io/pypi/v/python-xmp-toolkit.svg?maxAge=3600
   :alt: Version badge
   :target: https://pypi.org/project/python-xmp-toolkit/
.. image:: http://readthedocs.org/projects/python-xmp-toolkit/badge/?maxAge=3600
   :alt: Documentation badge
   :target: http://python-xmp-toolkit.readthedocs.io/


Python XMP Toolkit is a library for working with XMP metadata, as well as
reading/writing XMP metadata stored in many different file formats.

Python XMP Toolkit is wrapping `Exempi <https://libopenraw.freedesktop.org/wiki/Exempi/>`_
(using ctypes), a C/C++ XMP library based on Adobe XMP Toolkit, ensuring that future
updates to the XMP standard are easily incorporated into the library with a minimum
amount of work.

Python XMP Toolkit has been developed by:
 * ESA/Hubble - European Space Agency
 * ESO - European Southern Observatory
 * CRS4 - Centre for Advanced Studies, Research and Development in Sardinia


Documentation
=============
Documentation is available at `python-xmp-toolkit.readthedocs.org
<https://python-xmp-toolkit.readthedocs.org>`_ or can be built using Sphinx: ::

    pip install Sphinx
    sphinx-build docs/ docs/_build/


Testing
=======

Running the tests is as simple as:

.. code:: sh

    python -m pytest

