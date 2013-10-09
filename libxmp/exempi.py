"""
Wrapper functions for individual exempi library routines.
"""
import ctypes
from ctypes.util import find_library
import sys

from flufl.enum import IntEnum

# Handle for the library.
EXEMPI = ctypes.CDLL(find_library('exempi'))

class OpenFileOptions(IntEnum):
    """Option bits for xmp_files_open."""
    # No open option.
    no_option           = 0x00000000

    # Open for read-only access
    read                = 0x00000001

    # open for reading and writing
    for_update          = 0x00000002

    # only the XMP is wanted, allows space/time optimizations
    only_xmp            = 0x00000004

    # Cache thumbnail if possible, GetThumbnail will be called.
    cache_tnail         = 0x00000008

    # Be strict about locating XMP and reconciling with other forms.
    strictly            = 0x00000010

    # Require the use of a smart handler.
    use_smart_handler   = 0x00000020

    # Force packet scanning, don't use a smart handler.
    use_packet_scanning = 0x00000040

    # Only packet scan files known to need scanning.
    limit_scanning      = 0x00000080

    # Attempt to repair a file opened for update, default is to not open (raise
    # an exception).
    repair_file         = 0x00000100

    # Set if calling from background thread.
    # TODO:  is this ok from a python perspective?
    in_background       = 0x10000000


class CloseFileOptions(IntEnum):
    """ Option bits for xmp_files_close library routine."""
    # no close option
    no_option = 0x0000

    # Write into a temporary file and swap for crash safety.
    safe_update = 0x0001


class FileType(IntEnum):
    """Public file formats."""
    pdf             = 0x50444620
    ps              = 0x50532020
    eps             = 0x45505320

    jpeg            = 0x4A504547
    jpeg2k          = 0x4A505820
    tiff            = 0x54494646
    gif             = 0x47494620
    png             = 0x504E4720

    swf             = 0x53574620
    fla             = 0x464C4120
    flv             = 0x464C5620

    mov             = 0x4D4F5620  # Quicktime
    avi             = 0x41564920
    cin             = 0x43494E20  # Cineon
    wav             = 0x57415620
    mp3             = 0x4D503320
    ses             = 0x53455320  # Audition session
    cel             = 0x43454C20  # Audition loop
    mpeg            = 0x4D504547
    mpeg2           = 0x4D503220
    mpeg4           = 0x4D503420  # ISO 14494-12 and -14
    wmav            = 0x574D4156  # Windows Media Audio and Video
    aiff            = 0x41494646

    html            = 0x48544D4C
    xml             = 0x584D4C20
    text            = 0x74657874

    # Adobe application file formats.
    photoshop       = 0x50534420  # PSD
    illustrator     = 0x41492020  # AI
    indesign        = 0x494E4444  # INDD
    aeproject       = 0x41455020  # AEP
    aeprojtemplate  = 0x41455420  # AET, After Effects Project Template
    aefilterpreset  = 0x46465820  # FFX
    encoreproject   = 0x4E434F52  # NCOR
    premierproject  = 0x5052504A  # PRPJ
    premiertitle    = 0x5052544C  # PRTL

    unknown         = 0x20202020


class FileFormatOptions(IntEnum):
    """TODO"""
    can_inject_xmp        = 0x00000001
    can_expand            = 0x00000002
    can_rewrite           = 0x00000004
    prefers_in_place      = 0x00000008
    can_reconcile         = 0x00000010
    allows_only_xmp       = 0x00000020
    returns_raw_packet    = 0x00000040
    handler_owns_file     = 0x00000100
    allow_safe_update     = 0x00000200
    needs_readonly_packet = 0x00000400
    use_sidecar_xmp       = 0x00000800
    folder_based_format   = 0x00001000


class IterOptions(IntEnum):
    """Flags for modifying iteration."""
    # The low 8 bits are an enum of what data structure to iterate.
    class_mask      = 0x00FF

    # Iterate the property tree of a TXMPMeta object.
    properties      = 0x0000

    # Iterate the global alias table.
    aliases         = 0x0001

    # Iterate the global namespace table.
    namespaces      = 0x0002
    # Just do the immediate children * of the root, default is subtree.
    just_children   = 0x0100

    # Just do the leaf nodes, default * is all nodes in the subtree.
    just_leaf_nodes = 0x0200

    # Return just the leaf part of the * path, default is the full path.
    just_leaf_names = 0x0400

    # Include aliases, default is just * actual properties.
    include_aliases = 0x0800

    # Omit all qualifiers.
    omit_qualifiers = 0x1000


# Namespaces
# TODO verify that these are right.
NS_CC = "http://creativecommons.org/ns#"
NS_XMP = "http://ns.adobe.com/xap/1.0/"
NS_XMP_META = "adobe:ns:meta/"
NS_XAP = NS_XMP
NS_XMP_Rights = "http://ns.adobe.com/xap/1.0/rights/"
NS_XMP_MM = "http://ns.adobe.com/xap/1.0/mm/"
NS_XMP_BJ = "http://ns.adobe.com/xap/1.0/bj/"

NS_PDF = "http://ns.adobe.com/pdf/1.3/"
NS_PHOTOSHOP = "http://ns.adobe.com/photoshop/1.0/"
NS_PSAlbum = "http://ns.adobe.com/album/1.0/"
NS_EXIF = "http://ns.adobe.com/exif/1.0/"
NS_EXIF_Aux = "http://ns.adobe.com/exif/1.0/aux/"
NS_TIFF = "http://ns.adobe.com/tiff/1.0/"
NS_PNG = "http://ns.adobe.com/png/1.0/"
NS_SWF = "http://ns.adobe.com/swf/1.0/"
NS_JPEG = "http://ns.adobe.com/jpeg/1.0/"
NS_JP2K = "http://ns.adobe.com/jp2k/1.0/"
NS_CAMERA_RAW_SETTINGS = "http://ns.adobe.com/camera-raw-settings/1.0/"
NS_DM = "http://ns.adobe.com/xmp/1.0/DynamicMedia/"
NS_Script = "http://ns.adobe.com/xmp/1.0/Script/"
NS_ASF = "http://ns.adobe.com/asf/1.0/"
NS_WAV = "http://ns.adobe.com/xmp/wav/1.0/"
NS_BWF = "http://ns.adobe.com/bwf/bext/1.0/"
NS_XMP_Note = "http://ns.adobe.com/xmp/note/"
NS_AdobeStockPhoto = "http://ns.adobe.com/StockPhoto/1.0/"
NS_CreatorAtom = "http://ns.adobe.com/creatorAtom/1.0/"
NS_DC = "http://purl.org/dc/elements/1.1/"
NS_IPTCCore = "http://iptc.org/std/Iptc4xmpCore/1.0/xmlns/"
NS_DICOM = "http://ns.adobe.com/DICOM/"

NS_PDFA_Schema = "http://www.aiim.org/pdfa/ns/schema#"
NS_PDFA_Property = "http://www.aiim.org/pdfa/ns/property#"
NS_PDFA_Type = "http://www.aiim.org/pdfa/ns/type#"
NS_PDFA_Field = "http://www.aiim.org/pdfa/ns/field#"
NS_PDFA_ID = "http://www.aiim.org/pdfa/ns/id/"
NS_PDFA_Extension = "http://www.aiim.org/pdfa/ns/extension/"

NS_PDFX = "http://ns.adobe.com/pdfx/1.3/"
NS_PDFX_ID = "http://www.npes.org/pdfx/ns/id/"

NS_RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
NS_XML = "http://www.w3.org/XML/1998/namespace"


class XmpPropsBits(object):
    """Options relating to the XML string form of the property value."""
    # the value is a URI, use rdf:resource attribute.  DISCOURAGED
    value_is_uri = 0x0002

    # has qualifiers, includes rdf:type and xml:lang
    has_qualifier = 0x0010

    # is a qualifier, includes rdf:type and xml:lang
    is_qualifier = 0x0020

    # has xml:lang
    has_lang = 0x0040

    # has rdf:type
    has_type = 0x0080

    # The value is a structure.
    value_is_struct = 0x0100

    # The value is an array
    value_is_array = 0x0200

    # the item order does not matter
    array_is_unordered = 0x0200

    # item order matters
    array_is_ordered = 0x0400

    # items are alternates
    array_is_alt = 0x0800

    # items are localized text
    array_is_alttext = 0x1000

    # used by array functions
    array_insert_before = 0x4000
    array_insert_after = 0x8000

    # is an alias name for another property
    is_alias = 0x10000

    # is the base value for a set of aliases
    has_aliases = 0x20000

    # this property is an "internal" property, owned by applications
    is_internal = 0x40000

    # this property is not derived from the document content
    is_stable = 0x100000

    # this property is derived from the document content
    is_derived = 0x200000

    array_form_mask = value_is_array | array_is_ordered | array_is_alt \
                    | array_is_alttext
    composite_mask = value_is_struct | array_form_mask

    # reserved for transient use by the implementation
    reserved_mask = 0x70000000


class XmpDateTime(ctypes.Structure):
    """Corresponds to XmpDateTime type in exempi headers.
    """
    _fields_ = [
        ("year",        ctypes.c_int32),
        ("month",       ctypes.c_int32),
        ("day",         ctypes.c_int32),
        ("hour",        ctypes.c_int32),
        ("minute",      ctypes.c_int32),
        ("second",      ctypes.c_int32),
        ("tzSign",      ctypes.c_int32),
        ("tzHour",      ctypes.c_int32),
        ("tzMinute",    ctypes.c_int32),
        ("nanoSecond",  ctypes.c_int32)]


class TimeSign(IntEnum):
    """Values used for tzSign field."""
    west = -1
    utc = 0
    east = 1


class Serialize(IntEnum):
    """Options for xmp_serialize."""

    # Omit the XML packet wrapper.
    omit_packet_wrapper = 0x0010

    # Default is a writeable packet.
    read_only_packet = 0x0020

    # Use a compact form of RDF
    use_compact_format = 0x0040

    # Include a padding allowance for a thumbnail image.
    include_thumbnail_pad = 0x0100

    # The padding parameter is the overall packet length.
    exact_packet_length = 0x0200

    # Show aliases as XML comments.
    write_alias_comments = 0x0400

    # Omit all formatting whitespace.
    omit_all_formatting = 0x0800

    # Don't use this directly.
    _little_endian_bit = 0x0001

    encoding_mask = 0x0007
    encode_utf8 = 0x0000
    encode_utf16_big = 0x0002
    encode_utf16_little = encode_utf16_big | _little_endian_bit
    encode_utf32_big = 0x0004
    encode_utf16_little = encode_utf32_big | _little_endian_bit


def append_array_item(xmp, schema, name, array_options, value, option_bits):
    """Append a value to the XMP property array in the XMP packet.

    Wrapper for xmp_append_property_item library routine.

    Parameters
    ----------
    xmp : pointer
        The XMP packet.
    schema : str
        The schema of the property.
    name : str
        The name of the property.
    array_options : unsigned int
        The option bits of the parent array.
    value : str
        The value of the item to be appended.
    option_bits : unsigned int
        Option bits of the value itself.
    """
    EXEMPI.xmp_append_array_item.restype = check_error
    EXEMPI.xmp_append_array_item.argtypes = [ctypes.c_void_p,
                                             ctypes.c_char_p,
                                             ctypes.c_char_p,
                                             ctypes.c_uint32,
                                             ctypes.c_char_p,
                                             ctypes.c_uint32]

    EXEMPI.xmp_append_array_item(xmp,
                                 schema.encode(),
                                 name.encode(),
                                 array_options,
                                 value.encode(),
                                 option_bits)


def files_can_put_xmp(xfptr, xmp):
    """Wrapper for xmp_files_can_put_xmp library routine.

    Parameters
    ----------
    xfptr : file pointer
        File pointer
    xmp : pointer
        The XMP packet.

    Returns
    -------
    tf : bool
       True if the XMP packet can be written to the file.
    """
    EXEMPI.xmp_files_can_put_xmp.restype = ctypes.c_bool
    EXEMPI.xmp_files_can_put_xmp.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    tf = EXEMPI.xmp_files_can_put_xmp(xfptr, xmp)
    return tf == 1


def files_check_file_format(filename):
    """Check the file format of a file.

    Wrapper for xmp_check_file_format library routine.

    Parameters
    ----------
    filename : str
        Path to file.
    """
    EXEMPI.xmp_files_check_file_format.restype = FileType
    EXEMPI.xmp_files_check_file_format.argtypes = [ctypes.c_char_p]
    fmt = EXEMPI.xmp_files_check_file_format(filename.encode())
    return fmt


def delete_localized_text(xmp, schema, name, generic_lang, specific_lang):
    """Remove a property.

    Wrapper for xmp_delete_localized_text library routine.

    Parameters
    ----------
    xmp : pointer
        The XMP packet.
    schema : str
        The schema of the property.
    name : str
        The name of the property.
    generic_lang : str
        The generic language you may want.  Can be None.
    specific_lang : str
        The specific language.
    """
    EXEMPI.xmp_delete_localized_text.restype = check_error
    EXEMPI.xmp_delete_localized_text.argtypes = [ctypes.c_void_p,
                                                 ctypes.c_char_p,
                                                 ctypes.c_char_p,
                                                 ctypes.c_char_p,
                                                 ctypes.c_char_p]

    EXEMPI.xmp_delete_localized_text(xmp,
                                     schema.encode(),
                                     name.encode(),
                                     generic_lang.encode(),
                                     specific_lang.encode())


def delete_property(xmp, schema, name):
    """Delete a property from the XMP packet.

    Wrapper for xmp_delete_property library routine.

    Parameters
    ----------
    xmp : pointer
        The XMP packet.
    schema : str
        The schema of the property.
    name : str
        The name of the property.
    """
    EXEMPI.xmp_delete_property.restype = check_error
    EXEMPI.xmp_delete_property.argtypes = [ctypes.c_void_p,
                                           ctypes.c_char_p,
                                           ctypes.c_char_p]
    EXEMPI.xmp_delete_property(xmp, schema.encode(), name.encode())


def files_close(xfptr, options):
    """Close an XMP file, flush the changes.

    Wrapper for xmp_files_close library routine.

    Parameters
    ----------
    xfptr : file pointer
        File pointer
    options : CloseFileOptions
        the options for closing
    """
    EXEMPI.xmp_files_close.restype = check_error
    EXEMPI.xmp_files_close.argtypes = [ctypes.c_void_p, ctypes.c_int32]
    EXEMPI.xmp_files_close(xfptr, options)


def files_free(xfptr):
    """Free an XMP file pointer.

    Wrapper for xmp_files_free library routine.

    Parameters
    ----------
    xfptr : file pointer
        File pointer

    """
    EXEMPI.xmp_files_free.restype = check_error
    EXEMPI.xmp_files_free.argtypes = [ctypes.c_void_p]
    EXEMPI.xmp_files_free(xfptr)


def files_get_file_info(xfptr):
    """Get the file info from the open file.

    Wrapper for xmp_files_get_file_info library routine.

    Parameters
    ----------
    xfptr : file pointer
        File pointer

    Returns
    -------
    file_path : XmpStringPtr
        the file path object to store the path in. Pass NULL if not needed.
    options : XmpOpenFileOptions
        the options for open.
    file_format : XmpFileType
        the detected file format.
    handler_flags : XmpFileFormatOptions
        the format options like from files_get_format_info.
    """
    EXEMPI.xmp_files_get_file_info.restype = check_error
    EXEMPI.xmp_files_get_file_info.argtypes = [ctypes.c_void_p,
                                               ctypes.c_void_p,
                                               ctypes.POINTER(ctypes.c_int32),
                                               ctypes.POINTER(ctypes.c_int32),
                                               ctypes.POINTER(ctypes.c_int32)]
    file_path = string_new()
    options = ctypes.c_int32(0)
    file_format = ctypes.c_int32(0)
    handler_flags = ctypes.c_int32(0)

    EXEMPI.xmp_files_get_file_info(xfptr,
                                   file_path,
                                   ctypes.byref(options),
                                   ctypes.byref(file_format),
                                   ctypes.byref(handler_flags))

    options = OpenFileOptions[options.value]
    file_format = FileType[file_format.value]
    return file_path, options, file_format, handler_flags.value


def files_get_new_xmp(xfptr):
    """Wrapper for xmp_files_get_new_xmp library routine.

    Parameters
    ----------
    xfptr : file pointer
        File pointer

    Returns
    -------
    xmp_ptr : ctypes pointer
        XMP pointer
    """
    EXEMPI.xmp_files_get_new_xmp.restype = ctypes.c_void_p
    EXEMPI.xmp_files_get_new_xmp.argtypes = [ctypes.c_void_p]
    xmp_ptr = EXEMPI.xmp_files_get_new_xmp(xfptr)
    return xmp_ptr


def files_get_xmp(xfptr):
    """Wrapper for xmp_files_get_xmp library routine.

    Parameters
    ----------
    xfptr : file pointer
        File pointer

    Returns
    -------
    xmp_ptr : ctypes pointer
        XMP pointer
    """
    EXEMPI.xmp_files_get_xmp.restype = check_error
    EXEMPI.xmp_files_get_xmp.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

    xmp = new_empty()
    EXEMPI.xmp_files_get_xmp(xfptr, xmp)
    return xmp


def files_open_new(filename, options):
    """Wrapper for xmp_files_open_new library routine.

    Parameters
    ----------
    filename : str
        File to be opened.
    options : XmpFileOpenOptions
        How the file is to be opened.

    Returns
    -------
    xfptr : ctypes pointer
        File pointer.
    """
    EXEMPI.xmp_files_open_new.restype = ctypes.c_void_p
    EXEMPI.xmp_files_open_new.argtypes = [ctypes.c_void_p, ctypes.c_int32]
    xfptr = EXEMPI.xmp_files_open_new(filename.encode(), options)
    return xfptr


def files_put_xmp(xfptr, xmp):
    """Wrapper for xmp_files_put_xmp library routine.

    Parameters
    ----------
    xfptr : ctypes pointer
        File pointer.
    xmp : pointer
        The XMP packet.
    """
    EXEMPI.xmp_files_put_xmp.restype = check_error
    EXEMPI.xmp_files_put_xmp.argtypes = [ctypes.c_void_p, ctypes.c_int32]
    EXEMPI.xmp_files_put_xmp(xfptr, xmp)


def get_array_item(xmp, schema, name, index):
    """Get an item from an array property.

    Wrapper for xmp_get_array_item library routine.

    Parameters
    ----------
    xmp : pointer
        The XMP packet.
    schema : str
        The schema of the property.
    name : str
        The name of the property.
    index : int
        1-based index of the property.

    Returns
    -------
    item : exempi XmpStringPtr
        The value of the property.
    property_bits : unsigned int
        The property bits
    """
    EXEMPI.xmp_get_array_item.restype = check_error
    EXEMPI.xmp_get_array_item.argtypes = [ctypes.c_void_p,
                                          ctypes.c_char_p,
                                          ctypes.c_char_p,
                                          ctypes.c_int32,
                                          ctypes.c_void_p,
                                          ctypes.POINTER(ctypes.c_uint32)]
    item = string_new()
    property_bits = ctypes.c_uint32(0)

    EXEMPI.xmp_get_array_item(xmp,
                              schema.encode(),
                              name.encode(),
                              ctypes.c_int32(index),
                              item,
                              ctypes.byref(property_bits))
    return item, property_bits.value

def get_localized_text(xmp, schema, name, generic_lang, specific_lang):
    """Get a localised text from a localisable property.

    Wrapper for xmp_get_localized_text library routine.

    Parameters
    ----------
    xmp : pointer
        The XMP packet.
    schema : str
        The schema of the property.
    name : str
        The name of the property.
    generic_lang : str
        The generic language you may want.  Can be None.
    specific_lang : str
        The specific language.

    Returns
    -------
    item : xmp string pointer
        Opaque pointer to an XMP string.
    prop_bits : unsigned int
        option bit mask
    actual_lang : str
        The actual language of the item.
    """
    EXEMPI.xmp_get_localized_text.restype = check_error
    EXEMPI.xmp_get_localized_text.argtypes = [ctypes.c_void_p,
                                              ctypes.c_char_p,
                                              ctypes.c_char_p,
                                              ctypes.c_char_p,
                                              ctypes.c_char_p,
                                              ctypes.c_void_p,
                                              ctypes.c_void_p,
                                              ctypes.POINTER(ctypes.c_uint32)]

    if generic_lang is not None:
        generic_lang = generic_lang.encode()

    item = string_new()
    prop_bits = ctypes.c_uint32(0)
    actual_lang = string_new()

    EXEMPI.xmp_get_localized_text(xmp,
                                  schema.encode(),
                                  name.encode(),
                                  generic_lang,
                                  specific_lang.encode(),
                                  actual_lang, item,
                                  ctypes.byref(prop_bits))

    return item, prop_bits.value, actual_lang


def get_property(xmp, schema, name):
    """Wrapper for xmp_get_property library routine.

    Parameters
    ----------
    xmp : pointer
        The XMP packet.
    schema : str
        The schema of the property.
    name : str
        The name of the property.

    Returns
    -------
    prop : xmp string pointer
        Opaque pointer to an XMP string.  It is your responsibility to dispose
        of this string when you are finished with it.
    prop_bits : unsigned int
        option bit mask
    """
    # Use a function callback instead of returning a boolean value.
    EXEMPI.xmp_get_property.restype = check_error
    EXEMPI.xmp_get_property.argtypes = [ctypes.c_void_p,
                                        ctypes.c_char_p,
                                        ctypes.c_char_p,
                                        ctypes.c_void_p,
                                        ctypes.POINTER(ctypes.c_uint32)]

    newstr = string_new()
    prop_bits = ctypes.c_uint32(0)

    EXEMPI.xmp_get_property(xmp,
                            ctypes.c_char_p(schema.encode()),
                            ctypes.c_char_p(name.encode()),
                            newstr, ctypes.byref(prop_bits))
    return newstr, prop_bits.value


def get_property_bool(xmp, schema, name):
    """Wrapper for xmp_get_property_bool library routine.

    Parameters
    ----------
    xmp : pointer
        The XMP packet.
    schema : str
        The schema of the property.
    name : str
        The name of the property.

    Returns
    -------
    value : bool
        The value requested.
    prop_bits : unsigned int
        option bit mask
    """
    # Use a function callback instead of returning a boolean value.
    EXEMPI.xmp_get_property_bool.restype = check_error
    EXEMPI.xmp_get_property_bool.argtypes = [ctypes.c_void_p,
                                             ctypes.c_char_p,
                                             ctypes.c_char_p,
                                             ctypes.POINTER(ctypes.c_bool),
                                             ctypes.POINTER(ctypes.c_uint32)]

    bool_value = ctypes.c_bool(0)
    prop_bits = ctypes.c_uint32(0)

    EXEMPI.xmp_get_property_bool(xmp,
                                 schema.encode(),
                                 name.encode(),
                                 ctypes.byref(bool_value),
                                 ctypes.byref(prop_bits))
    return bool_value.value, prop_bits.value


def get_property_date(xmp, schema, name):
    """Wrapper for xmp_get_property_date library routine.

    Parameters
    ----------
    xmp : pointer
        The XMP packet.
    schema : str
        The schema of the property.
    name : str
        The name of the property.

    Returns
    -------
    date : XmpTimeSign
        Date structure.
    prop_bits : unsigned int
        option bit mask
    """
    # Use a function callback instead of returning a boolean value.
    EXEMPI.xmp_get_property_date.restype = check_error
    EXEMPI.xmp_get_property_date.argtypes = [ctypes.c_void_p,
                                             ctypes.c_char_p,
                                             ctypes.c_char_p,
                                             ctypes.POINTER(XmpDateTime),
                                             ctypes.POINTER(ctypes.c_uint32)]

    xmp_date_time = XmpDateTime()
    prop_bits = ctypes.c_uint32(0)

    EXEMPI.xmp_get_property_date(xmp,
                                 schema.encode(),
                                 name.encode(),
                                 ctypes.byref(xmp_date_time),
                                 ctypes.byref(prop_bits))
    return xmp_date_time, prop_bits.value


def get_property_int32(xmp, schema, name):
    """Wrapper for xmp_get_property_int32 library routine.

    Parameters
    ----------
    xmp : pointer
        The XMP packet.
    schema : str
        The schema of the property.
    name : str
        The name of the property.

    Returns
    -------
    value : int
        The int32 value requested.
    prop_bits : unsigned int
        option bit mask
    """
    # Use a function callback instead of returning a boolean value.
    EXEMPI.xmp_get_property_int32.restype = check_error
    EXEMPI.xmp_get_property_int32.argtypes = [ctypes.c_void_p,
                                             ctypes.c_char_p,
                                             ctypes.c_char_p,
                                             ctypes.POINTER(ctypes.c_int32),
                                             ctypes.POINTER(ctypes.c_uint32)]

    ivalue = ctypes.c_int32(0)
    prop_bits = ctypes.c_uint32(0)

    EXEMPI.xmp_get_property_int32(xmp,
                                  schema.encode(),
                                  name.encode(),
                                  ctypes.byref(ivalue),
                                  ctypes.byref(prop_bits))
    return ivalue.value, prop_bits.value


def get_property_int64(xmp, schema, name):
    """Wrapper for xmp_get_property_int64 library routine.

    Parameters
    ----------
    xmp : pointer
        The XMP packet.
    schema : str
        The schema of the property.
    name : str
        The name of the property.

    Returns
    -------
    value : int
        The int64 value requested.
    prop_bits : unsigned int
        option bit mask
    """
    # Use a function callback instead of returning a boolean value.
    EXEMPI.xmp_get_property_int64.restype = check_error
    EXEMPI.xmp_get_property_int64.argtypes = [ctypes.c_void_p,
                                             ctypes.c_char_p,
                                             ctypes.c_char_p,
                                             ctypes.POINTER(ctypes.c_int64),
                                             ctypes.POINTER(ctypes.c_uint32)]

    ivalue = ctypes.c_int64(0)
    prop_bits = ctypes.c_uint32(0)

    EXEMPI.xmp_get_property_int64(xmp,
                                  schema.encode(),
                                  name.encode(),
                                  ctypes.byref(ivalue),
                                  ctypes.byref(prop_bits))
    return ivalue.value, prop_bits.value


def get_property_float(xmp, schema, name):
    """Wrapper for xmp_get_property_float library routine.

    Parameters
    ----------
    xmp : pointer
        The XMP packet.
    schema : str
        The schema of the property.
    name : str
        The name of the property.

    Returns
    -------
    value : float
        The value requested.
    prop_bits : unsigned int
        option bit mask
    """
    # Use a function callback instead of returning a boolean value.
    EXEMPI.xmp_get_property_float.restype = check_error
    EXEMPI.xmp_get_property_float.argtypes = [ctypes.c_void_p,
                                              ctypes.c_char_p,
                                              ctypes.c_char_p,
                                              ctypes.POINTER(ctypes.c_double),
                                              ctypes.POINTER(ctypes.c_uint32)]

    double_value = ctypes.c_double(0)
    prop_bits = ctypes.c_uint32(0)

    EXEMPI.xmp_get_property_float(xmp,
                                  schema.encode(),
                                  name.encode(),
                                  ctypes.byref(double_value),
                                  ctypes.byref(prop_bits))
    return double_value.value, prop_bits.value


def free(xmp):
    """Wrapper for xmp_free library routine."""
    EXEMPI.xmp_free.argtypes = [ctypes.c_void_p]
    EXEMPI.xmp_free.restype = None
    EXEMPI.xmp_free(xmp)


def get_error():
    """Wrapper for xmp_get_error library routine."""
    EXEMPI.xmp_get_error.restype = ctypes.c_int32
    code = EXEMPI.xmp_get_error()
    return code


def has_property(xmp, schema, name):
    """Wrapper for xmp_has_property library routine.

    Parameters
    ----------
    xmp : pointer
        The XMP packet.
    schema : str
        The schema of the property.
    name : str
        The name of the property.
    """
    EXEMPI.xmp_has_property.restype = ctypes.c_bool
    EXEMPI.xmp_has_property.argtypes = [ctypes.c_void_p,
                                        ctypes.c_char_p,
                                        ctypes.c_char_p]
    ret = EXEMPI.xmp_has_property(xmp,
                                  schema.encode(),
                                  name.encode())
    if ret == 1:
        return True
    else:
        return False


def init():
    """Wrapper for xmp_init library routine."""
    EXEMPI.xmp_init.restype = check_error
    ret = EXEMPI.xmp_init()
    return ret


def iterator_free(iterator):
    """Wrapper for xmp_iterator_free library routine.

    Parameters
    ----------
    iterator : XmpIteratorPtr
        iterator for use with iterator_next
    """

    EXEMPI.xmp_iterator_free.argtypes = [ctypes.c_void_p]
    EXEMPI.xmp_iterator_free.restype = check_error
    EXEMPI.xmp_iterator_free(iterator)


def iterator_next(iterator):
    """Iterate to the next value.

    Wrapper for xmp_iterator_next library routine.

    Parameters
    ----------
    iterator : XmpIteratorPtr
        iterator for use with iterator_next

    Returns
    -------
    schema, propname, value : XmpStringPtr
        The schema, name, and value of the property.  These values should be
        properly disposed of with the string_free function.
    options : unsigned integer
        The options for the property.

    Raises
    ------
    StopIteration : when the library determines that the iteration is finished.
    """

    EXEMPI.xmp_iterator_next.argtypes = [ctypes.c_void_p,
                                         ctypes.c_void_p,
                                         ctypes.c_void_p,
                                         ctypes.c_void_p,
                                         ctypes.POINTER(ctypes.c_uint32)]
    EXEMPI.xmp_iterator_next.restype = ctypes.c_bool

    schema = string_new()
    propname = string_new()
    propvalue = string_new()
    options = ctypes.c_uint32(0)

    success = EXEMPI.xmp_iterator_next(iterator, schema, propname, propvalue,
                                   ctypes.byref(options))

    if not success:
        raise StopIteration()

    return schema, propname, propvalue, options


def iterator_new(xmp, schema, propname, options):
    """Wrapper for xmp_iterator_new library routine.

    Parameters
    ----------
    xmp : pointer
        The XMP packet.
    schema, propname : str
        The schema and name of the property.
    options : unsigned integer
        The options for the property.

    Returns
    -------
    iterator : XmpIteratorPtr
        iterator for use with iterator_next
    """

    EXEMPI.xmp_iterator_new.argtypes = [ctypes.c_void_p,
                                        ctypes.c_char_p,
                                        ctypes.c_char_p,
                                        ctypes.c_int32]
    EXEMPI.xmp_iterator_new.restype = ctypes.c_void_p

    if schema is not None:
        schema = schema.encode()

    if propname is not None:
        propname = propname.encode()

    iterator = EXEMPI.xmp_iterator_new(xmp, schema, propname, options)
    return iterator


def namespace_prefix(namespace):
    """Retuns a prefix associated with a namespace.

    Wrapper for xmp_namespace_prefix library routine.

    Parameters
    ----------
    namespace : str
        The namespace associated if registered.  May pass None.

    Returns
    -------
    prefix : xmp pointer
        The prefix to check.
    """
    EXEMPI.xmp_namespace_prefix.restype = check_error
    EXEMPI.xmp_namespace_prefix.argtypes = [ctypes.c_char_p, ctypes.c_void_p]
    prefix = string_new()
    EXEMPI.xmp_namespace_prefix(namespace.encode(), prefix)
    return prefix


def new_empty():
    """Create a new XMP packet.

    Wrapper for xmp_new_empty library routine.

    Returns
    -------
    item : xmp string pointer
        Opaque pointer to an XMP string.  It is your responsibility to properly
        dispose of the string.
    """
    EXEMPI.xmp_new_empty.restype = ctypes.c_void_p
    xmp = EXEMPI.xmp_new_empty()
    return xmp


def parse(xmp, strbuffer):
    """Parse the XML and load it.

    Wrapper for xmp_parse library routine.

    Parameters
    ----------
    xmp : pointer
        The XMP packet.
    strbuffer : str
        A string of XML to parse.
    """
    # Use a function callback instead of returning a boolean value.
    EXEMPI.xmp_parse.restype = check_error
    EXEMPI.xmp_parse.argtypes = [ctypes.c_void_p,
                                 ctypes.c_char_p,
                                 ctypes.c_size_t]
    strbuffer_charray = strbuffer.encode()
    EXEMPI.xmp_parse(xmp, strbuffer_charray, len(strbuffer_charray))


def prefix_namespace_uri(prefix):
    """Retrieve namespace associated with a prefix.

    Wrapper for xmp_namespace_prefix library routine.

    Parameters
    ----------
    prefix : xmp pointer
        The prefix to check.

    Returns
    -------
    namespace : str
        The namespace associated if registered.  May pass None.
    """
    EXEMPI.xmp_prefix_namespace_uri.restype = check_error
    EXEMPI.xmp_prefix_namespace_uri.argtypes = [ctypes.c_char_p]

    namespace = string_new()
    EXEMPI.xmp_prefix_namespace_uri(prefix.encode(), namespace)
    return namespace


def register_namespace(namespace_uri, prefix):
    """Register a new namespace.

    Wrapper for xmp_register_namespace library routine.

    Parameters
    ----------
    namespace_uri : str
        the namespace URI to register
    prefix : str
        the suggested prefix

    Returns
    -------
    registered_prefix : xmp pointer
        # TODO harmonize these descriptions.
        The really registered prefix.
    """
    # TODO Needs a raises part.
    EXEMPI.xmp_register_namespace.restype = check_error
    EXEMPI.xmp_register_namespace.argtypes = [ctypes.c_char_p,
                                              ctypes.c_char_p,
                                              ctypes.c_void_p]

    registered_prefix = string_new()
    EXEMPI.xmp_register_namespace(namespace_uri.encode(),
                                  prefix.encode(),
                                  registered_prefix)

    return registered_prefix

def serialize_and_format(xmp, options, padding, newline, tab, indent):
    """Serialize the XMP Packet with formatting.

    Wrapper for xmp_serialize_and_format library routine.

    Parameters
    ----------
    xmp : pointer
        The XMP packet.
    options : unsigned integer
        Options on how to write the XMP.
    padding : int
        Number of bytes of padding, useful for modifying embedded XMP in place.
    newline, tab : str
        Characters to specify the newline and tabbing.
    indent : int
        The initial indentation level.
    """
    EXEMPI.xmp_serialize_and_format.restype = check_error
    EXEMPI.xmp_serialize_and_format.argtypes = [ctypes.c_void_p,
                                                ctypes.c_void_p,
                                                ctypes.c_uint32,
                                                ctypes.c_uint32,
                                                ctypes.c_char_p,
                                                ctypes.c_char_p,
                                                ctypes.c_int32]
    item = string_new()
    EXEMPI.xmp_serialize_and_format(xmp, item, options, padding,
                                    newline.encode(), tab.encode(), indent)
    return item


def set_array_item(xmp, schema, name, index, value, option_bits):
    """Wrapper for xmp_set_array_item library routine.

    Parameters
    ----------
    xmp : pointer
        The XMP packet.
    schema : str
        The schema of the property.
    name : str
        The name of the property.
    index : int
        1-based index of the property.
    value : str
        The value of the property.
    """
    EXEMPI.xmp_set_array_item.restype = check_error
    EXEMPI.xmp_set_array_item.argtypes = [ctypes.c_void_p,
                                          ctypes.c_char_p,
                                          ctypes.c_char_p,
                                          ctypes.c_int32,
                                          ctypes.c_char_p,
                                          ctypes.c_uint32]
    EXEMPI.xmp_set_array_item(xmp,
                              schema.encode(),
                              name.encode(),
                              ctypes.c_int32(index),
                              value.encode(),
                              option_bits)


def set_localized_text(xmp, schema, name, generic_lang, specific_lang, value,
                       mask=0):
    """Set a localized text from a localizable property.

    Wrapper for xmp_set_localized_txt library routine.

    Parameters
    ----------
    xmp : pointer
        The XMP packet.
    schema : str
        The schema of the property.
    name : str
        The name of the property.
    specific_lang : str
        The specific language.
    generic_lang : str
        The generic language you may want as a fall back.
    value : xmp string pointer
        Opaque pointer to an XMP string.
    mask : unsigned int
        option bit mask
    """
    EXEMPI.xmp_set_localized_text.restype = check_error
    EXEMPI.xmp_set_localized_text.argtypes = [ctypes.c_void_p,
                                              ctypes.c_char_p,
                                              ctypes.c_char_p,
                                              ctypes.c_char_p,
                                              ctypes.c_char_p,
                                              ctypes.c_char_p,
                                              ctypes.c_uint32]

    if generic_lang is not None:
        generic_lang = generic_lang.encode()

    mask = ctypes.c_uint32(mask)
    EXEMPI.xmp_set_localized_text(xmp,
                                  schema.encode(),
                                  name.encode(),
                                  generic_lang,
                                  specific_lang.encode(),
                                  value.encode(),
                                  mask)

def set_property(xmp, schema, name, value, option_bits=0):
    """Set an XMP property in the XMP packet.

    Wrapper for xmp_set_property library routine.

    Parameters
    ----------
    xmp : pointer
        The XMP packet.
    schema : str
        The schema of the property.
    name : str
        The name of the property.
    value : str
        The name of the property.
    option_bits : unsigned int
        #TODO
    """
    # Use a function callback instead of returning a boolean value.
    EXEMPI.xmp_set_property.restype = check_error
    EXEMPI.xmp_set_property.argtypes = [ctypes.c_void_p,
                                        ctypes.c_char_p,
                                        ctypes.c_char_p,
                                        ctypes.c_char_p,
                                        ctypes.c_uint32]

    EXEMPI.xmp_set_property(xmp,
                            schema.encode(),
                            name.encode(),
                            value.encode(),
                            ctypes.c_uint32(option_bits))


def set_property_bool(xmp, schema, name, value, option_bits=0):
    """Set a bool XMP property in the XMP packet.

    Wrapper for xmp_set_property_bool library routine.

    Parameters
    ----------
    xmp : pointer
        The XMP packet.
    schema : str
        The schema of the property.
    name : str
        The name of the property.
    value : bool
        The boolean value
    option_bits : unsigned int
        #TODO
    """
    # Use a function callback instead of returning a boolean value.
    EXEMPI.xmp_set_property_bool.restype = check_error
    EXEMPI.xmp_set_property_bool.argtypes = [ctypes.c_void_p,
                                             ctypes.c_char_p,
                                             ctypes.c_char_p,
                                             ctypes.c_bool,
                                             ctypes.c_uint32]

    bvalue = ctypes.c_bool(value)
    EXEMPI.xmp_set_property_bool(xmp,
                                 schema.encode(),
                                 name.encode(),
                                 bvalue,
                                 ctypes.c_uint32(option_bits))


def set_property_date(xmp, schema, name, xmp_date, option_bits=0):
    """Set a date XMP property in the XMP packet.

    Wrapper for xmp_set_property_date library routine.

    Parameters
    ----------
    xmp : pointer
        The XMP packet.
    schema : str
        The schema of the property.
    name : str
        The name of the property.
    xmp_date : XmpDateTime
        The date and time
    option_bits : unsigned int
        #TODO
    """
    # Use a function callback instead of returning a boolean value.
    EXEMPI.xmp_set_property_date.restype = check_error
    EXEMPI.xmp_set_property_date.argtypes = [ctypes.c_void_p,
                                              ctypes.c_char_p,
                                              ctypes.c_char_p,
                                              ctypes.POINTER(XmpDateTime),
                                              ctypes.c_uint32]

    EXEMPI.xmp_set_property_date(xmp,
                                 ctypes.c_char_p(schema.encode()),
                                 ctypes.c_char_p(name.encode()),
                                 ctypes.byref(xmp_date),
                                 ctypes.c_uint32(option_bits))


def set_property_int32(xmp, schema, name, value, option_bits=0):
    """Set an int32 XMP property in the XMP packet.

    Wrapper for xmp_set_property_int32 library routine.

    Parameters
    ----------
    xmp : pointer
        The XMP packet.
    schema : str
        The schema of the property.
    name : str
        The name of the property.
    value : int64
        The int32 value
    option_bits : unsigned int
        #TODO
    """
    # Use a function callback instead of returning a boolean value.
    EXEMPI.xmp_set_property_int32.restype = check_error
    EXEMPI.xmp_set_property_int32.argtypes = [ctypes.c_void_p,
                                              ctypes.c_char_p,
                                              ctypes.c_char_p,
                                              ctypes.c_int32,
                                              ctypes.c_uint32]

    ivalue = ctypes.c_int32(value)
    EXEMPI.xmp_set_property_int32(xmp,
                                  schema.encode(),
                                  name.encode(),
                                  ivalue,
                                  ctypes.c_uint32(option_bits))


def set_property_int64(xmp, schema, name, value, option_bits=0):
    """Set an int64 XMP property in the XMP packet.

    Wrapper for xmp_set_property_int32 library routine.

    Parameters
    ----------
    xmp : pointer
        The XMP packet.
    schema : str
        The schema of the property.
    name : str
        The name of the property.
    value : int
        The int64 value
    option_bits : unsigned int
        #TODO
    """
    # Use a function callback instead of returning a boolean value.
    EXEMPI.xmp_set_property_int64.restype = check_error
    EXEMPI.xmp_set_property_int64.argtypes = [ctypes.c_void_p,
                                              ctypes.c_char_p,
                                              ctypes.c_char_p,
                                              ctypes.c_int64,
                                              ctypes.c_uint32]

    ivalue = ctypes.c_int64(value)
    EXEMPI.xmp_set_property_int64(xmp,
                                  schema.encode(),
                                  name.encode(),
                                  ivalue,
                                  ctypes.c_uint32(option_bits))


def set_property_float(xmp, schema, name, value, option_bits=0):
    """Set a float XMP property in the XMP packet.

    Wrapper for xmp_set_property_float library routine.

    Parameters
    ----------
    xmp : pointer
        The XMP packet.
    schema : str
        The schema of the property.
    name : str
        The name of the property.
    value : float
        The float value
    option_bits : unsigned int
        #TODO
    """
    # Use a function callback instead of returning a boolean value.
    EXEMPI.xmp_set_property_float.restype = check_error
    EXEMPI.xmp_set_property_float.argtypes = [ctypes.c_void_p,
                                              ctypes.c_char_p,
                                              ctypes.c_char_p,
                                              ctypes.c_double,
                                              ctypes.c_uint32]

    dvalue = ctypes.c_double(value)
    EXEMPI.xmp_set_property_float(xmp,
                                  schema.encode(),
                                  name.encode(),
                                  dvalue,
                                  ctypes.c_uint32(option_bits))


def string_cstr(xmpstr):
    """Wrapper for xmp_string_cstr library routine.

    Parameters
    ----------
    xmpstr : Opaque pointer (XmpStringPtr)
        Exempi string type.

    Returns
    -------
    pystr : str
        Python string
    """
    EXEMPI.xmp_string_cstr.restype = ctypes.c_char_p
    EXEMPI.xmp_string_cstr.argtypes = [ctypes.c_void_p]
    cstr = EXEMPI.xmp_string_cstr(xmpstr)
    if sys.hexversion < 0x03000000:
        return str(cstr)
    else:
        return cstr.decode('utf-8')


def string_free(xmp_string):
    """Free an XmpStringPtr.

    Wrapper for xmp_string_free library routine.

    Parameters
    ----------
    xmp_string : exempi XmpStringPtr
        The string to free.
    """
    EXEMPI.xmp_string_free.argtypes = [ctypes.c_void_p]
    EXEMPI.xmp_string_free(xmp_string)


def string_new():
    """Wrapper for xmp_string_new library routine.

    Returns
    -------
    ptr : pointer
        Opaque pointer to a string.
    """
    # This is an opaque type that we should not peek into!
    EXEMPI.xmp_string_new.restype = ctypes.c_void_p
    return EXEMPI.xmp_string_new()


def terminate():
    """Wrapper for xmp_terminate library routine"""
    EXEMPI.xmp_terminate.restype = ctypes.c_void_p
    EXEMPI.xmp_terminate()


def check_error(status):
    """Set a generic function as the restype attribute of all exempi
    functions that return a boolean value.  This way we do not have to check
    for error status in each wrapping function and an exception will always be
    appropriately raised.
    """
    error_code = EXEMPI.xmp_get_error()
    if status != 1:
        msg = "Exempi function failure (error code={0})."
        msg = msg.format(error_code)
        raise IOError(msg)


# The following correspond to macros in xmp.h
def is_prop_simple(opt):
    return ((opt & XmpPropsBits.composite_mask) == 0)


def is_prop_struct(opt):
    return ((opt & XmpPropsBits.value_is_struct) == 0)
