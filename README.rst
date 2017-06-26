==================
Python XMP Toolkit
==================

.. image:: https://img.shields.io/travis/python-xmp-toolkit/python-xmp-toolkit/master.svg?maxAge=3600
   :alt: Build status badge
   :target: https://travis-ci.org/python-xmp-toolkit/python-xmp-toolkit
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
Documentation is available at `python-xml-toolkit.readthedocs.org
<https://python-xmp-toolkit.readthedocs.org>`_ or can be built using Sphinx: ::

    pip install Sphinx
    python setup.py build_sphinx

Testing
=======
Running the tests is as simple as: ::

    python setup.py test

or (to also show test coverage): ::

    source run-coverage.sh

