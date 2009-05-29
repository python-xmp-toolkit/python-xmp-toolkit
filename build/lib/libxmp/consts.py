# -*- coding: utf-8 -*-
#
# Copyright (c) 2008-2009, European Space Agency & European Southern Observatory (ESA/ESO)
# Copyright (c) 2008-2009, CRS4 - Centre for Advanced Studies, Research and Development in Sardinia
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#	  * Redistributions of source code must retain the above copyright
#		notice, this list of conditions and the following disclaimer.
# 
#	  * Redistributions in binary form must reproduce the above copyright
#		notice, this list of conditions and the following disclaimer in the
#		documentation and/or other materials provided with the distribution.
# 
#	  * Neither the name of the European Space Agency, European Southern 
#		Observatory, CRS4 nor the names of its contributors may be used to endorse or 
#		promote products derived from this software without specific prior 
#		written permission.
# 
# THIS SOFTWARE IS PROVIDED BY ESA/ESO AND CRS4 ``AS IS'' AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL ESA/ESO BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE

### XMP FILES 

"""
"""

#
# Open options
#
XMP_OPEN_NOOPTION = 0x00000000 #< No open option
XMP_OPEN_READ = 0x00000001 #< Open for read-only access.
XMP_OPEN_FORUPDATE = 0x00000002 #< Open for reading and writing.
XMP_OPEN_ONLYXMP = 0x00000004 #< Only the XMP is wanted, allows space/time optimizations.
XMP_OPEN_CACHETNAIL = 0x00000008 #< Cache thumbnail if possible,  GetThumbnail will be called.
XMP_OPEN_STRICTLY = 0x00000010 #< Be strict about locating XMP and reconciling with other forms. 
XMP_OPEN_USESMARTHANDLER = 0x00000020 #< Require the use of a smart handler (Text files, PDF and Illustrator are incompatible with this option).
XMP_OPEN_USEPACKETSCANNING = 0x00000040 #< Force packet scanning, don't use a smart handler.
XMP_OPEN_LIMITSCANNING = 0x00000080 #< Only packet scan files "known" to need scanning (Text files, PDF are incompatible with this option).
XMP_OPEN_INBACKGROUND = 0x10000000  #< Set if calling from background thread.

#
# Close options
#
XMP_CLOSE_NOOPTION      = 0x0000 #< No close option */
XMP_CLOSE_SAFEUPDATE    = 0x0001 #< Write into a temporary file and swap for crash safety.

#
# File formats
#
XMP_FT_PDF      = 0x50444620L  #  'PDF ' 
XMP_FT_PS       = 0x50532020L  #  'PS  ' general PostScript following DSC conventions. 
XMP_FT_EPS      = 0x45505320L  #  'EPS ' encapsulated PostScript. 
XMP_FT_JPEG     = 0x4A504547L  #  'JPEG' 
XMP_FT_JPEG2K   = 0x4A505820L  #  'JPX ' ISO 15444-1 
XMP_FT_TIFF     = 0x54494646L  #  'TIFF' 
XMP_FT_GIF      = 0x47494620L  #  'GIF ' 
XMP_FT_PNG      = 0x504E4720L  #  'PNG '   
XMP_FT_SWF      = 0x53574620L  #  'SWF ' 
XMP_FT_FLA      = 0x464C4120L  #  'FLA ' 
XMP_FT_FLV      = 0x464C5620L  #  'FLV ' 
XMP_FT_MOV      = 0x4D4F5620L  #  'MOV ' Quicktime 
XMP_FT_AVI      = 0x41564920L  #  'AVI ' 
XMP_FT_CIN      = 0x43494E20L  #  'CIN ' Cineon 
XMP_FT_WAV      = 0x57415620L  #  'WAV ' 
XMP_FT_MP3      = 0x4D503320L  #  'MP3 ' 
XMP_FT_SES      = 0x53455320L  #  'SES ' Audition session 
XMP_FT_CEL      = 0x43454C20L  #  'CEL ' Audition loop 
XMP_FT_MPEG     = 0x4D504547L  #  'MPEG' 
XMP_FT_MPEG2    = 0x4D503220L  #  'MP2 ' 
XMP_FT_MPEG4    = 0x4D503420L  #  'MP4 ' ISO 14494-12 and -14 
XMP_FT_WMAV     = 0x574D4156L  #  'WMAV' Windows Media Audio and Video 
XMP_FT_AIFF     = 0x41494646L  #  'AIFF' 
XMP_FT_HTML     = 0x48544D4CL  #  'HTML' 
XMP_FT_XML      = 0x584D4C20L  #  'XML ' 
XMP_FT_TEXT     = 0x74657874L  #  'text' 
#  Adobe application file formats. 
XMP_FT_PHOTOSHOP       = 0x50534420L  #  'PSD ' 
XMP_FT_ILLUSTRATOR     = 0x41492020L  #  'AI  ' 
XMP_FT_INDESIGN        = 0x494E4444L  #  'INDD' 
XMP_FT_AEPROJECT       = 0x41455020L  #  'AEP ' 
XMP_FT_AEPROJTEMPLATE  = 0x41455420L  #  'AET ' After Effects Project Template 
XMP_FT_AEFILTERPRESET  = 0x46465820L  #  'FFX ' 
XMP_FT_ENCOREPROJECT   = 0x4E434F52L  #  'NCOR' 
XMP_FT_PREMIEREPROJECT = 0x5052504AL  #  'PRPJ' 
XMP_FT_PREMIERETITLE   = 0x5052544CL  #  'PRTL' 
# Catch all
XMP_FT_UNKNOWN  = 0x20202020L

### XMP CORE
#
# Serialize Options
#		
XMP_SERIAL_OMITPACKETWRAPPER   = 0x0010L  # Do not include an XML packet wrapper.
XMP_SERIAL_READONLYPACKET      = 0x0020L  # Create a read-only XML packet wapper.
XMP_SERIAL_USECOMPACTFORMAT    = 0x0040L  # Use a highly compact RDF syntax and layout.
XMP_SERIAL_INCLUDETHUMBNAILPAD = 0x0100L  # Include typical space for a JPEG thumbnail in the padding if no xmp:Thumbnails property is present.
XMP_SERIAL_EXACTPACKETLENGTH   = 0x0200L  # The padding parameter provides the overall packet length.
XMP_SERIAL_WRITEALIASCOMMENTS  = 0x0400L  # Include XML comments for aliases.
XMP_SERIAL_OMITALLFORMATTING   = 0x0800L  # Omit all formatting whitespace.

#
# XMPIterator Options
#
XMP_ITER_CLASSMASK      = 0x00FFL   # The low 8 bits are an enum of what data structure to iterate. 
XMP_ITER_PROPERTIES     = 0x0000L   # Iterate the property tree of a TXMPMeta object. 
XMP_ITER_ALIASES        = 0x0001L   # Iterate the global alias table. - XMP Toolkit and Exempi don't implement this option yet
XMP_ITER_NAMESPACES     = 0x0002L   # Iterate the global namespace table. - XMP Toolkit and Exempi don't implement this option yet
XMP_ITER_JUSTCHILDREN   = 0x0100L   # Just do the immediate children of the root, default is subtree. 
XMP_ITER_JUSTLEAFNODES  = 0x0200L   # Just do the leaf nodes, default is all nodes in the subtree.
XMP_ITER_JUSTLEAFNAME   = 0x0400L   # Return just the leaf part of the path, default is the full path. 
XMP_ITER_INCLUDEALIASES = 0x0800L   # Include aliases, default is just actual properties. 
XMP_ITER_OMITQUALIFIERS = 0x1000L   # Omit all qualifiers. 
 
#
# XMPIterator Skip Options
#
XMP_ITER_SKIPSUBTREE   = 0x0001L  # Skip the subtree below the current node. 
XMP_ITER_SKIPSIBLINGS  = 0x0002L   # Skip the subtree below and remaining siblings of the current node.

#
# PropBits
#
XMP_PROP_VALUE_IS_URI     = 0x00000002L # The value is a URI, use rdf:resource attribute.  DISCOURAGED 
# Options relating to qualifiers attached to a property. 
XMP_PROP_HAS_QUALIFIERS   = 0x00000010L # The property has qualifiers,includes rdf:type and  xml:lang.
XMP_PROP_IS_QUALIFIER     = 0x00000020L # This is a qualifier, includes rdf:type and xml:lang. */
XMP_PROP_HAS_LANG         = 0x00000040L # Implies XMP_PropHasQualifiers,  property has xml:lang. 
XMP_PROP_HAS_TYPE         = 0x00000080L # Implies XMP_PropHasQualifiers,  property has rdf:type.

# Options relating to the data structure form. 
XMP_PROP_VALUE_IS_STRUCT = 0x00000100L  # The value is a structure with nested fields. 
XMP_PROP_VALUE_IS_ARRAY  = 0x00000200L  # The value is an array (RDF alt/bag/seq). 
XMP_PROP_ARRAY_IS_UNORDERED = XMP_PROP_VALUE_IS_ARRAY  # The item order does not matter.
XMP_PROP_ARRAY_IS_ORDERED = 0x00000400L # Implies XMP_PropValueIsArray,item order matters. 
XMP_PROP_ARRAY_IS_ALT    = 0x00000800L  # Implies XMP_PropArrayIsOrdered,items are alternates. 


# Additional struct and array options.
XMP_PROP_ARRAY_IS_ALTTEXT = 0x00001000L  # Implies kXMP_PropArrayIsAlternate,items are localized text. 
# kXMP_InsertBeforeItem  = 0x00004000L  ! Used by SetXyz functions. */
# kXMP_InsertAfterItem   = 0x00008000L  ! Used by SetXyz functions. */

# Other miscellaneous options
XMP_PROP_IS_ALIAS         = 0x00010000L #This property is an alias name for another property. 
XMP_PROP_HAS_ALIASES      = 0x00020000L #This property is the base value for a set of aliases. 
XMP_PROP_IS_INTERNAL      = 0x00040000L #This property is an "internal" property, owned by applications. 
XMP_PROP_IS_STABLE        = 0x00100000L #This property is not derived from the document content. 
XMP_PROP_IS_DERIVED       = 0x00200000L #This property is derived from the document content. 
# kXMPUtil_AllowCommas   = 0x10000000L  ! Used by TXMPUtils::CatenateArrayItems and ::SeparateArrayItems. 
# kXMP_DeleteExisting    = 0x20000000L  ! Used by TXMPMeta::SetXyz functions to delete any pre-existing property. 
XMP_IS_SCHEMA            = 0x80000000L  #Returned by iterators - #define to avoid warnings - Not defined by Exempi
XMP_PROP_IS_SCHEMA            = 0x80000000L  #Returned by iterators - #define to avoid warnings - Not defined by Exempi

# Multiple flag masks
XMP_PROP_ARRAY_FORM_MASK  = XMP_PROP_VALUE_IS_ARRAY	| XMP_PROP_ARRAY_IS_ORDERED | XMP_PROP_ARRAY_IS_ALT | XMP_PROP_ARRAY_IS_ALTTEXT
XMP_PROP_COMPOSITE_MASK   = XMP_PROP_VALUE_IS_STRUCT | XMP_PROP_ARRAY_FORM_MASK  #Is it simple or composite (array or struct)? 
XMP_IMPL_RESERVED_MASK    = 0x70000000L   # Reserved for transient use by the implementation. 

#####################
# Common Namespaces #
#####################
#
# XML namespace constants for standard XMP schema.
#
XMP_NS_XMP = "http://ns.adobe.com/xap/1.0/"
""" XMP Namespace """

XMP_NS_XMP_Rights = "http://ns.adobe.com/xap/1.0/rights/"
XMP_NS_XMP_MM = "http://ns.adobe.com/xap/1.0/mm/"
XMP_NS_XMP_BJ = "http://ns.adobe.com/xap/1.0/bj/"

XMP_NS_PDF = "http://ns.adobe.com/pdf/1.3/"
XMP_NS_Photoshop = "http://ns.adobe.com/photoshop/1.0/"
XMP_NS_PSAlbum = "http://ns.adobe.com/album/1.0/"
XMP_NS_EXIF = "http://ns.adobe.com/exif/1.0/"
XMP_NS_EXIF_Aux = "http://ns.adobe.com/exif/1.0/aux/"
XMP_NS_TIFF = "http://ns.adobe.com/tiff/1.0/"
XMP_NS_PNG = "http://ns.adobe.com/png/1.0/"
XMP_NS_SWF = "http://ns.adobe.com/swf/1.0/"
XMP_NS_JPEG = "http://ns.adobe.com/jpeg/1.0/"
XMP_NS_JP2K = "http://ns.adobe.com/jp2k/1.0/"
XMP_NS_CameraRaw = "http://ns.adobe.com/camera-raw-settings/1.0/"
XMP_NS_DM = "http://ns.adobe.com/xmp/1.0/DynamicMedia/"
XMP_NS_ASF = "http://ns.adobe.com/asf/1.0/"
XMP_NS_WAV = "http://ns.adobe.com/xmp/wav/1.0/"

XMP_NS_XMP_Note = "http://ns.adobe.com/xmp/note/"

XMP_NS_AdobeStockPhoto = "http://ns.adobe.com/StockPhoto/1.0/"
XMP_NS_CreatorAtom = "http://ns.adobe.com/creatorAtom/1.0/"

#
# XML namespace constants for qualifiers and structured property fields.
#
XMP_NS_XMP_IdentifierQual = "http://ns.adobe.com/xmp/Identifier/qual/1.0/"
XMP_NS_XMP_Dimensions = "http://ns.adobe.com/xap/1.0/sType/Dimensions#"
XMP_NS_XMP_Text = "http://ns.adobe.com/xap/1.0/t/"
XMP_NS_XMP_PagedFile = "http://ns.adobe.com/xap/1.0/t/pg/"
XMP_NS_XMP_Graphics = "http://ns.adobe.com/xap/1.0/g/"
XMP_NS_XMP_Image = "http://ns.adobe.com/xap/1.0/g/img/"
XMP_NS_XMP_Font = "http://ns.adobe.com/xap/1.0/sType/Font#"
XMP_NS_XMP_ResourceEvent = "http://ns.adobe.com/xap/1.0/sType/ResourceEvent#"
XMP_NS_XMP_ResourceRef = "http://ns.adobe.com/xap/1.0/sType/ResourceRef#"
XMP_NS_XMP_ST_Version = "http://ns.adobe.com/xap/1.0/sType/Version#"
XMP_NS_XMP_ST_Job = "http://ns.adobe.com/xap/1.0/sType/Job#"
XMP_NS_XMP_ManifestItem = "http://ns.adobe.com/xap/1.0/sType/ManifestItem#"

# Deprecated XML namespace constants
XMP_NS_XMP_T = "http://ns.adobe.com/xap/1.0/t/"
XMP_NS_XMP_T_PG = "http://ns.adobe.com/xap/1.0/t/pg/"
XMP_NS_XMP_G_IMG = "http://ns.adobe.com/xap/1.0/g/img/"

#
# XML namespace constants from outside Adobe.
#
XMP_NS_DC = "http://purl.org/dc/elements/1.1/"
XMP_NS_IPTCCore = "http://iptc.org/std/Iptc4xmpCore/1.0/xmlns/"
XMP_NS_DICOM = "http://ns.adobe.com/DICOM/"
XMP_NS_PDFA_Schema = "http://www.aiim.org/pdfa/ns/schema#"
XMP_NS_PDFA_Property = "http://www.aiim.org/pdfa/ns/property#"
XMP_NS_PDFA_Type = "http://www.aiim.org/pdfa/ns/type#"
XMP_NS_PDFA_Field = "http://www.aiim.org/pdfa/ns/field#"
XMP_NS_PDFA_ID = "http://www.aiim.org/pdfa/ns/id/"
XMP_NS_PDFA_Extension = "http://www.aiim.org/pdfa/ns/extension/"
XMP_NS_PDFX = "http://ns.adobe.com/pdfx/1.3/"
XMP_NS_PDFX_ID = "http://www.npes.org/pdfx/ns/id/"
XMP_NS_RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
XMP_NS_XML = "http://www.w3.org/XML/1998/namespace"

#
# Exempi added namespaces
#
XMP_NS_XMPMeta = "adobe:ns:meta/"
XMP_NS_Lightroom = "http://ns.adobe.com/lightroom/1.0/"
XMP_NS_CameraRawSavedSettings = "http://ns.adobe.com/camera-raw-saved-settings/1.0/"
XMP_NS_CC = "http://creativecommons.org/ns#"

#
# Python XMP Toolkit added namespaces
#
XMP_NS_AVM = "http://www.communicatingastronomy.org/avm/1.0/"

#
# Definition of serialization options names.
#
XMP_SERIAL_OPTIONS = {
	'omit_packet_wrapper' : XMP_SERIAL_OMITPACKETWRAPPER,
	'read_only_packet' : XMP_SERIAL_READONLYPACKET,
	'use_compact_format' : XMP_SERIAL_USECOMPACTFORMAT,
	'include_thumbnail_pad' : XMP_SERIAL_INCLUDETHUMBNAILPAD,
	'exact_packet_length' : XMP_SERIAL_EXACTPACKETLENGTH,
	'write_alias_comments' : XMP_SERIAL_WRITEALIASCOMMENTS,
	'omit_all_formatting' : XMP_SERIAL_OMITALLFORMATTING,
}


# Definition of property option names
XMP_PROP_OPTIONS = {
	'prop_value_is_uri' : XMP_PROP_VALUE_IS_URI,
	'prop_has_qualifiers' : XMP_PROP_HAS_QUALIFIERS,
	'prop_is_qualifier' : XMP_PROP_IS_QUALIFIER,
	'prop_has_lang' : XMP_PROP_HAS_LANG,
	'prop_has_type' : XMP_PROP_HAS_TYPE,
	'prop_value_is_struct' : XMP_PROP_VALUE_IS_STRUCT,
	'prop_value_is_array' : XMP_PROP_VALUE_IS_ARRAY,
	'prop_array_is_unordered' : XMP_PROP_ARRAY_IS_UNORDERED,
	'prop_array_is_ordered' : XMP_PROP_ARRAY_IS_ORDERED, 
	'prop_array_is_alt' : XMP_PROP_ARRAY_IS_ALT,
	'prop_array_is_alttext' : XMP_PROP_ARRAY_IS_ALTTEXT,
	'prop_is_alias' : XMP_PROP_IS_ALIAS,
	'prop_has_aliases' : XMP_PROP_HAS_ALIASES,
	'prop_is_internal' : XMP_PROP_IS_INTERNAL,
	'prop_is_stable' : XMP_PROP_IS_STABLE,
	'prop_is_deriver' : XMP_PROP_IS_DERIVED,
	'prop_is_schema' : XMP_PROP_IS_SCHEMA,			
}

# Definition of iterator's option names
XMP_ITERATOR_OPTIONS = {
	'iter_classmask': XMP_ITER_CLASSMASK,
	'iter_properties': XMP_ITER_PROPERTIES, 
	'iter_aliases': XMP_ITER_ALIASES,
	'iter_namespaces' : XMP_ITER_NAMESPACES,
	'iter_justchildren' : XMP_ITER_JUSTCHILDREN,
	'iter_justleafnodes' : XMP_ITER_JUSTLEAFNODES,	
	'iter_justleafname' : XMP_ITER_JUSTLEAFNAME,
	'iter_includealiases' : XMP_ITER_INCLUDEALIASES,
	'iter_omitqualifiers' : XMP_ITER_OMITQUALIFIERS								
}

# Definition of open options names
XMP_OPEN_OPTIONS = {
	'open_nooption' : XMP_OPEN_NOOPTION,
	'open_read' : XMP_OPEN_READ,
	'open_forupdate' : XMP_OPEN_FORUPDATE,
	'open_onlyxmp' : XMP_OPEN_ONLYXMP,
	'open_cachetnail' : XMP_OPEN_CACHETNAIL,
	'open_strictly' : XMP_OPEN_STRICTLY,
	'open_usesmarthandler' : XMP_OPEN_USESMARTHANDLER,
	'open_usepacketscanning' : XMP_OPEN_USEPACKETSCANNING,
	'open_limitscanning' : XMP_OPEN_LIMITSCANNING,
	'open_inbackground' : XMP_OPEN_INBACKGROUND,								
}

# Definition of XMPIterator.skip()'s option names
XMP_SKIP_OPTIONS = {
	'iter_skipsubtree' : XMP_ITER_SKIPSUBTREE, 
	'iter_skipsiblings' : XMP_ITER_SKIPSIBLINGS								
}

def has_option ( xmp_option, bitmask ):
	return bool( xmp_option & bitmask )

def options_mask( xmp_options, **kwargs ):
	"""
	Internal function for creating the options bit mask to parse into exempi C functions.
	
	Example::
	
	  opt = consts.options_mask( consts.XMP_SERIAL_OPTIONS, **kwargs )
	
	or::
	
	  opt = consts.options_mask( consts.XMP_SERIAL_OPTIONS, omit_packet_wrapper=True )	
	"""
	bitmask = 0x0L
	
	for const_name,const_value in kwargs.iteritems():
		if const_value and const_name in xmp_options:
			bitmask |= xmp_options[const_name]
			
	return bitmask
