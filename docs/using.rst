Using Python XMP Toolkit
============================

This little tutorial will show you two different methods for how to
read/write XMP documents from files as well as manipulate them metadata
once extracted from the file.

The tutorial is meant to be understood without prior knowledge of
XMP. However, readers who decides to use the library are strongly
encouraged to gain basic knowledge and understanding of:

  * XMP Data Model
  * XMP Serialization

A basic understanding of these two concepts can save yourself from common
misunderstandings of what XMP is and what XMP can do. Good resources
are e.g. the wiki page or the XMP Specification Part 1 available from:

 * http://en.wikipedia.org/wiki/Extensible_Metadata_Platform
 * http://www.adobe.com/devnet/xmp/

Method 1: Read XMP
------------------
One of the most basic uses of the library is:

>>> from libxmp.utils import file_to_dict
>>> xmp = file_to_dict( "test/samples/BlueSquare.xmp" )


This will read the XMP embedded in the file and return it as a
dictionary. The keys in the dictionary are XMP namespaces so to e.g. get
all Dublin Core properties use:


>>> from libxmp import consts
>>> dc = xmp[consts.XMP_NS_DC]

or to be explicit:

>>> dc = xmp["http://purl.org/dc/elements/1.1/"]

This will give you a list of all Dublin Core properties, where each
element in the list is a tuple. The first element is the property name,
the second element is the value and the third element is options associated
with the element (describing e.g the type of the property):

First tuple element:

>>> print(dc[0][0])
dc:format

Second tuple element:

>>> print(dc[0][1])
application/vnd.adobe.photoshop

Third tuple element is a dict with options:

>>> dc[0][2]['IS_SCHEMA']
False

Method 2: Read/Write XMP
------------------------
Example 1 focused on just extracting the XMP from a file an determine the
value of a property. If you however want to extract the XMP from a file,
update it, *and* write it back again you need to do like the following

Read file:

>>> from libxmp import XMPFiles, consts
>>> xmpfile = XMPFiles( file_path="test/samples/BlueSquare.jpg", open_forupdate=True )

Get XMP from file:

>>> xmp = xmpfile.get_xmp()

Print the property ``dc:format``:

>>> print(xmp.get_property(consts.XMP_NS_DC, 'format' ))
image/jpeg

Change the XMP property:

>>> xmp.set_property(consts.XMP_NS_DC, u'format', u'application/vnd.adobe.illustrator' )
>>> print(xmp.get_property(consts.XMP_NS_DC, 'format' ))
application/vnd.adobe.illustrator

Check if XMP document can be written to file and write it:

>>> xmpfile.can_put_xmp(xmp)
True
>>> xmpfile.put_xmp(xmp)

XMP document is not written to the file, before the file
is closed:

>>> xmpfile.can_put_xmp(xmp)
>>> xmpfile.close_file()

Further Examples
----------------
Append an array item to the XMP packet.::

Read file:

>>> from libxmp import XMPFiles, consts
>>> xmpfile = XMPFiles( file_path="test/samples/BlueSquare.xmp" )

Get XMP from file:

>>> xmp = xmpfile.get_xmp()

Create a new array item and append a value:

>>> xmp.append_array_item(consts.XMP_NS_DC, 'creator', 'Your Name Here', {'prop_array_is_ordered': True, 'prop_value_is_array': True})
