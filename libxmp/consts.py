### XMP FILES 

#
# Open options
#
XMP_OPEN_NOOPTION = 0x00000000 #< No open option
XMP_OPEN_READ = 0x00000001 #< Open for read-only access.
XMP_OPEN_FORUPDATE = 0x00000002 #< Open for reading and writing.
XMP_OPEN_ONLYXMP = 0x00000004 #< Only the XMP is wanted, allows space/time optimizations.
XMP_OPEN_CACHETNAIL = 0x00000008 #< Cache thumbnail if possible,  GetThumbnail will be called.
XMP_OPEN_STRICTLY = 0x00000010 #< Be strict about locating XMP and reconciling with other forms. 
XMP_OPEN_USESMARTHANDLER = 0x00000020 #< Require the use of a smart handler.
XMP_OPEN_USEPACKETSCANNING = 0x00000040 #< Force packet scanning, don't use a smart handler.
XMP_OPEN_LIMITSCANNING = 0x00000080 #< Only packet scan files "known" to need scanning.
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
XMP_ITER_SKIPSUBTREE   = 0x0001L,  # Skip the subtree below the current node. 
XMP_ITER_SKIPSIBLINGS  = 0x0002L   # Skip the subtree below and remaining siblings of the current node. 

