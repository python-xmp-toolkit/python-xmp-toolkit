Using Python XMP Toolkit
============================

This little tutorial will show you two different methods for how to read/write XMP documents from files as well as manipulate them metadata once extracted from the file. 

The tutorial is meant to be understood without prior knowledge of XMP. However, readers who decides to use the library are strongly encouraged to gain basic knowledge and understanding of:

  * XMP Data Model
  * XMP Serialization

A basic understanding of these two concepts can save yourself from common misunderstandings of what XMP is and what XMP can do. Good resources are e.g. the wiki page or the XMP Specification Part 1 available from:

 * http://en.wikipedia.org/wiki/Extensible_Metadata_Platform
 * http://www.adobe.com/devnet/xmp/

Method 1: Read XMP
------------------
One of the most basic uses of the library is::

	from libxmp import *

	xmp = file_to_dict( "/path/to/some/file_with_xmp.ext" )

This will read the XMP embedded in the file and return it as a dictionary. The keys in the dictionary are XMP namespaces so to e.g. get all Dublin Core properties use::

	dc = xmp[consts.XMP_NS_DC]
	# or to be explicit
	dc = xmp["http://purl.org/dc/elements/1.1/"]
	
This will give you a list of all Dublin Core properties, where each element in the list is a tuple such as::

	( 
		u'dc:format', 
		u'application/vnd.adobe.photoshop', 
		{
			'IS_SCHEMA': False, 
			'IS_ALIAS': False, 
			'HAS_TYPE': False, 
			'ARRAY_IS_ALT': False, 
			'IS_INTERNAL': False, 
			'IS_DERIVED': False, 
			'HAS_ALIASES': False, 
			'HAS_LANG': False, 
			'VALUE_IS_STRUCT': False, 
			'HAS_QUALIFIERS': False, 
			'ARRAY_IS_ALTTEXT': False, 
			'VALUE_IS_URI': False, 
			'VALUE_IS_ARRAY': False, 
			'ARRAY_IS_ORDERED': False, 
			'IS_QUALIFIER': False, 
			'IS_STABLE': False
		}
	)
	
The first element is the property name, the second element is the value and the third element is options associated with the element (describing e.g the type of the property).	

Method 2: Read/Write XMP
------------------------
Example 1 focused on just extracting the XMP from a file an determine the value of a property. If you however want to extract the XMP from a file, update it, *and* write it back again you need to do like the following::


	from libxmp import *

	# Read file
	xmpfile = XMPFiles( file_path="/path/to/some/file", open_forupdate=True )
	
	# Get XMP from file.
	xmp = xmpfile.get_xmp()
	
	# Print the property dc:format 
	print xmp.get_property( libxmp.consts.XMP_NS_DC, 'format' )
	
	# Change the XMP property
	xmp.set_property( libxmp.consts.XMP_NS_DC, 'format','application/vnd.adobe.illustrator' )
	
	# Check if XMP document can be written to file and write it.
	if xmpfile.can_put_xmp(xmp):
		xmpfile.put_xmp(xmp)
		
	# XMP document is not written to the file, before the file 
	# is closed.
	xmpfile.close_file()

Further Examples
-------------
Append an array item to the XMP packet.::

	from libxmp import *
	
	# Read file
	xmpfile = XMPFiles( file_path="/path/to/some/file" )
	
	# Get XMP from file
	xmp = xmpfile.get_xmp()
	
	# Create a new array item and append a value
	xmp.append_array_item(files.XMP_NS_DC, 'creator', 'Your Name Here', {'prop_array_is_ordered': True, 'prop_value_is_array': True})	