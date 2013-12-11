==================
Python XMP Toolkit
==================

.. image:: https://travis-ci.org/python-xmp-toolkit/python-xmp-toolkit.png?branch=master
    :target: https://travis-ci.org/python-xmp-toolkit/python-xmp-toolkit
.. image:: https://coveralls.io/repos/python-xmp-toolkit/python-xmp-toolkit/badge.png?branch=master
    :target: https://coveralls.io/r/python-xmp-toolkit/python-xmp-toolkit
.. image:: https://pypip.in/v/python-xmp-toolkit/badge.png
   :target: https://crate.io/packages/python-xmp-toolkit/
.. image:: https://pypip.in/d/python-xmp-toolkit/badge.png
   :target: https://crate.io/packages/python-xmp-toolkit/

Python XMP Toolkit is a library for working with XMP metadata, as well as
reading/writing XMP metadata stored in many different file formats.

Python XMP Toolkit is wrapping Exempi (using ctypes), a C/C++ XMP library
based on Adobe XMP Toolkit, ensuring that future updates to the XMP standard
are easily incorporated into the library with a minimum amount of work.

Python XMP Toolkit has been developed by:
 * ESA/Hubble - European Space Agency
 * ESO - European Southern Observatory
 * CRS4 - Centre for Advanced Studies, Research and Development in Sardinia

Documentation
============
Documentation is available at <http://python-xmp-toolkit.readthedocs.org> or can be build using Sphinx: ::

    pip install Sphinx
    python setup.py build_sphinx

Testing
=======
Running the tests are as simple as: ::

    python setup.py test

or (to also show test coverage) ::

    source run-coverage.sh

.. image:: https://d2weczhvl823v0.cloudfront.net/python-xmp-toolkit/python-xmp-toolkit/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free