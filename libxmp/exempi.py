"""
Wrapper functions for individual exempi library routines.
"""
import ctypes
import datetime
from ctypes.util import find_library
import os

from flufl.enum import IntEnum
import pytz

from . import XMPError

EXEMPI = ctypes.CDLL(find_library('exempi'))

class ErrorCodes(IntEnum):
    """
    Error codes defined by libexempi.  See "xmperrors.h"
    """
    unknown            =    0
    tbd                =   -1
    unavailable        =   -2
    bad_object         =   -3
    bad_param          =   -4
    bad_value          =   -5
    assert_failure     =   -6
    enforce_failure    =   -7
    unimplemented      =   -8
    internal_failure   =   -9
    deprecated         =  -10
    external_failure   =  -11
    user_abort         =  -12
    std_exception      =  -13
    unknown_exception  =  -14
    no_memory          =  -15
    bad_schema         = -101
    bad_xpath          = -102
    bad_options        = -103
    bad_index          = -104
    bad_iter_position  = -105
    bad_parse          = -106
    bad_serialize      = -107
    bad_file_format    = -108
    no_file_handler    = -109
    too_large_for_jpeg = -110
    bad_xml            = -201
    bad_rdf            = -202
    bad_xmp            = -203
    empty_iterator     = -204
    bad_unicode        = -205
    bad_tiff           = -206
    bad_jpeg           = -207
    bad_psd            = -208
    bad_psir           = -209
    bad_iptc           = -210
    bad_mpeg           = -211

ERROR_MESSAGE = { int(ErrorCodes.unknown):            "unknown error",
                  int(ErrorCodes.tbd):                "TBD",
                  int(ErrorCodes.unavailable):        "unavailable",
                  int(ErrorCodes.bad_object):         "bad object",
                  int(ErrorCodes.bad_param):          "bad parameter",
                  int(ErrorCodes.bad_value):          "bad value",
                  int(ErrorCodes.assert_failure):     "assert failure",
                  int(ErrorCodes.enforce_failure):    "enforce failure",
                  int(ErrorCodes.unimplemented):      "unimplemented",
                  int(ErrorCodes.internal_failure):   "internal failure",
                  int(ErrorCodes.deprecated):         "deprecated",
                  int(ErrorCodes.external_failure):   "external failure",
                  int(ErrorCodes.user_abort):         "user abort",
                  int(ErrorCodes.std_exception):      "std exception",
                  int(ErrorCodes.unknown_exception):  "unknown exception",
                  int(ErrorCodes.no_memory):          "no memory",
                  int(ErrorCodes.bad_schema):         "bad schema",
                  int(ErrorCodes.bad_xpath):          "bad XPath",
                  int(ErrorCodes.bad_options):        "bad options",
                  int(ErrorCodes.bad_index):          "bad index",
                  int(ErrorCodes.bad_iter_position):  "bad iter position",
                  int(ErrorCodes.bad_parse):          "bad parse",
                  int(ErrorCodes.bad_serialize):      "bad serialize",
                  int(ErrorCodes.bad_file_format):    "bad file format",
                  int(ErrorCodes.no_file_handler):    "no file handler",
                  int(ErrorCodes.too_large_for_jpeg): "too large for JPEG",
                  int(ErrorCodes.bad_xml):            "bad XML",
                  int(ErrorCodes.bad_rdf):            "bad RDF",
                  int(ErrorCodes.bad_xmp):            "bad XMP",
                  int(ErrorCodes.empty_iterator):     "empty iterator",
                  int(ErrorCodes.bad_unicode):        "bad unicode",
                  int(ErrorCodes.bad_tiff):           "bad TIFF",
                  int(ErrorCodes.bad_jpeg):           "bad JPEG",
                  int(ErrorCodes.bad_psd):            "bad PSD",
                  int(ErrorCodes.bad_psir):           "bad PSIR",
                  int(ErrorCodes.bad_iptc):           "bad IPTC",
                  int(ErrorCodes.bad_mpeg):           "bad MPEG" }

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
        Mask of options.

    Raises
    ------
    XMPError : if the corresponding library routine fails
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


def copy(xmp):
    """Create a new XMP packet from an existing instance.

    Wrapper for xmp_copy library routine.

    Parameters
    ----------
    xmp : XmpPtr instance.
        The XMP packet object.

    Returns
    -------
    newxmp : XmpPtr instance.
        A copy of the XMP packet object.
    """
    EXEMPI.xmp_copy.restype = ctypes.c_void_p
    EXEMPI.xmp_copy.argtypes = [ctypes.c_void_p]
    newxmp = EXEMPI.xmp_copy(xmp)
    return newxmp


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
    value = EXEMPI.xmp_files_can_put_xmp(xfptr, xmp)
    return value == 1


def files_check_file_format(filename):
    """Check the file format of a file.

    Wrapper for xmp_check_file_format library routine.

    Parameters
    ----------
    filename : str
        Path to file.
    """
    if not os.path.exists(filename):
        raise IOError("{0} does not exist.".format(filename))
    EXEMPI.xmp_files_check_file_format.restype = ctypes.c_int32
    EXEMPI.xmp_files_check_file_format.argtypes = [ctypes.c_char_p]
    return EXEMPI.xmp_files_check_file_format(filename.encode())


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

    Raises
    ------
    XMPError : if the corresponding library routine fails

    .. versionadded:: 2.0.0
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

    Raises
    ------
    XMPError : if the corresponding library routine fails
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

    Raises
    ------
    XMPError : if the corresponding library routine fails
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

    Raises
    ------
    XMPError : if the corresponding library routine fails

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
    file_path : str
        the file path object to store the path in.
    options : XmpOpenFileOptions
        the options for open.
    file_format : XmpFileType
        the detected file format.
    handler_flags : XmpFileFormatOptions
        the format options like from files_get_format_info.

    Raises
    ------
    XMPError : if the corresponding library routine fails
    """
    EXEMPI.xmp_files_get_file_info.restype = check_error
    EXEMPI.xmp_files_get_file_info.argtypes = [ctypes.c_void_p,
                                               ctypes.c_void_p,
                                               ctypes.POINTER(ctypes.c_int32),
                                               ctypes.POINTER(ctypes.c_int32),
                                               ctypes.POINTER(ctypes.c_int32)]
    _file_path = _string_new()
    options = ctypes.c_int32(0)
    file_format = ctypes.c_int32(0)
    handler_flags = ctypes.c_int32(0)

    EXEMPI.xmp_files_get_file_info(xfptr,
                                   _file_path,
                                   ctypes.byref(options),
                                   ctypes.byref(file_format),
                                   ctypes.byref(handler_flags))

    file_path = string_cstr(_file_path)
    _string_free(_file_path)

    options = OpenFileOptions[options.value]
    return file_path, options, file_format.value, handler_flags.value


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

    Raises
    ------
    XMPError : if the corresponding library routine fails
    """
    EXEMPI.xmp_files_get_xmp.restype = check_error
    EXEMPI.xmp_files_get_xmp.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

    xmp = new_empty()
    EXEMPI.xmp_files_get_xmp(xfptr, xmp)
    return xmp


def files_open(xfptr, filename, options):
    """Wrapper for xmp_files_open library routine.

    Parameters
    ----------
    xfptr : object
        XMP file object (with no associated file)
    filename : str
        File to be opened.
    options : XmpFileOpenOptions
        How the file is to be opened.

    Raises
    ------
    XMPError : if the corresponding library routine fails
    """
    if not os.path.exists(filename) and options & OpenFileOptions.read:
        raise IOError("{0} does not exist.".format(filename))
    EXEMPI.xmp_files_open.restype = check_error
    EXEMPI.xmp_files_open.argtypes = [ctypes.c_void_p,
                                      ctypes.c_char_p,
                                      ctypes.c_int32]
    EXEMPI.xmp_files_open(xfptr, filename.encode('utf-8'), options)


def files_new():
    """Wrapper for xmp_files_new library routine.

    Returns
    -------
    xfptr : ctypes pointer
        File pointer.
    """
    EXEMPI.xmp_files_new.restype = ctypes.c_void_p
    xfptr = EXEMPI.xmp_files_new()

    return xfptr


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
    if not os.path.exists(filename) and options & OpenFileOptions.read:
        raise IOError("{0} does not exist.".format(filename))
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

    Raises
    ------
    XMPError : if the corresponding library routine fails
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
    item : str
        The value of the property.
    property_bits : unsigned int
        The property bits

    Raises
    ------
    XMPError : if the corresponding library routine fails
    """
    EXEMPI.xmp_get_array_item.restype = check_error
    EXEMPI.xmp_get_array_item.argtypes = [ctypes.c_void_p,
                                          ctypes.c_char_p,
                                          ctypes.c_char_p,
                                          ctypes.c_int32,
                                          ctypes.c_void_p,
                                          ctypes.POINTER(ctypes.c_uint32)]
    _item = _string_new()
    property_bits = ctypes.c_uint32(0)

    EXEMPI.xmp_get_array_item(xmp,
                              schema.encode(),
                              name.encode(),
                              ctypes.c_int32(index),
                              _item,
                              ctypes.byref(property_bits))

    item = string_cstr(_item)
    _string_free(_item)

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
    item : str
        The localized text.
    prop_bits : unsigned int
        option bit mask
    actual_lang : str
        The actual language of the item.

    Raises
    ------
    XMPError : if the corresponding library routine fails
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

    _item = _string_new()
    prop_bits = ctypes.c_uint32(0)
    _actual_lang = _string_new()

    EXEMPI.xmp_get_localized_text(xmp,
                                  schema.encode(),
                                  name.encode(),
                                  generic_lang,
                                  specific_lang.encode(),
                                  _actual_lang, _item,
                                  ctypes.byref(prop_bits))

    item = string_cstr(_item)
    _string_free(_item)

    actual_lang = string_cstr(_actual_lang)
    _string_free(_actual_lang)

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
    prop : str
        Property value as a string.
    prop_bits : unsigned int
        option bit mask

    Raises
    ------
    XMPError : if the corresponding library routine fails
    """
    # Use a function callback instead of returning a boolean value.
    EXEMPI.xmp_get_property.restype = check_error
    EXEMPI.xmp_get_property.argtypes = [ctypes.c_void_p,
                                        ctypes.c_char_p,
                                        ctypes.c_char_p,
                                        ctypes.c_void_p,
                                        ctypes.POINTER(ctypes.c_uint32)]

    _value = _string_new()
    prop_bits = ctypes.c_uint32(0)

    EXEMPI.xmp_get_property(xmp,
                            ctypes.c_char_p(schema.encode()),
                            ctypes.c_char_p(name.encode()),
                            _value, ctypes.byref(prop_bits))

    value = string_cstr(_value)
    _string_free(_value)
    
    return value, prop_bits.value


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

    Raises
    ------
    XMPError : if the corresponding library routine fails
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

    Raises
    ------
    XMPError : if the corresponding library routine fails
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

    date1 = datetime.datetime(xmp_date_time.year,
                              xmp_date_time.month,
                              xmp_date_time.day,
                              xmp_date_time.hour,
                              xmp_date_time.minute,
                              xmp_date_time.second)
    utc = pytz.timezone('utc')
    utc_date = utc.localize(date1)
    delta = datetime.timedelta(hours=xmp_date_time.tzHour,
                               minutes=xmp_date_time.tzMinute,
                               microseconds=xmp_date_time.nanoSecond * 1000)

    if xmp_date_time.tzSign < 0:
        the_date = utc_date - delta
    else:
        the_date = utc_date + delta

    return the_date, prop_bits.value


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

    Raises
    ------
    XMPError : if the corresponding library routine fails
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

    Raises
    ------
    XMPError : if the corresponding library routine fails
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
    # EXEMPI has trouble parsing some floats such as "+1.0", so let python
    # do it instead.
    value, prop_bits = get_property(xmp, schema, name)
    value = float(value)
    return value, prop_bits


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
    """Wrapper for xmp_init library routine.

    Raises
    ------
    XMPError : if the corresponding library routine fails
    """
    EXEMPI.xmp_init.restype = check_error
    EXEMPI.xmp_init()


def iterator_free(iterator):
    """Wrapper for xmp_iterator_free library routine.

    Parameters
    ----------
    iterator : XmpIteratorPtr
        iterator for use with iterator_next

    Raises
    ------
    XMPError : if the corresponding library routine fails
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
    schema, propname, value : str
        The schema, name, and value of the property as strings.
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

    _schema = _string_new()
    _propname = _string_new()
    _propvalue = _string_new()
    options = ctypes.c_uint32(0)

    success = EXEMPI.xmp_iterator_next(iterator, _schema, _propname, _propvalue,
                                   ctypes.byref(options))

    if not success:
        _string_free(_schema)
        _string_free(_propname)
        _string_free(_propvalue)
        raise StopIteration()

    schema = string_cstr(_schema)
    _string_free(_schema)

    propname = string_cstr(_propname)
    _string_free(_propname)

    propvalue = string_cstr(_propvalue)
    _string_free(_propvalue)

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


def iterator_skip(iterator, options):
    """Wrapper for xmp_iterator_skip library routine.

    Parameters
    ----------
    iterator : XmpIteratorPtr
        iterator for use with iterator_next
    options : int
        Mask of options.

    Raises
    ------
    XMPError : if the corresponding library routine fails
    """
    EXEMPI.xmp_iterator_skip.argtypes = [ctypes.c_void_p,
                                         ctypes.c_int32]
    EXEMPI.xmp_iterator_skip.restype = ctypes.c_bool
    success = EXEMPI.xmp_iterator_skip(iterator, options)
    check_error(success)


def namespace_prefix(namespace):
    """Returns a prefix associated with a namespace.

    Wrapper for xmp_namespace_prefix library routine.

    Parameters
    ----------
    namespace : str
        The namespace associated if registered.  May pass None.
        TODO:  check this

    Returns
    -------
    prefix : str
        The prefix associated with the namespace.

    Raises
    ------
    XMPError : if the corresponding library routine fails
    """
    EXEMPI.xmp_namespace_prefix.restype = check_error
    EXEMPI.xmp_namespace_prefix.argtypes = [ctypes.c_char_p, ctypes.c_void_p]
    _prefix = _string_new()
    EXEMPI.xmp_namespace_prefix(namespace.encode(), _prefix)

    prefix = string_cstr(_prefix)
    _string_free(_prefix)

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

    Raises
    ------
    XMPError : if the corresponding library routine fails
    """
    # Use a function callback instead of returning a boolean value.
    EXEMPI.xmp_parse.restype = check_error
    EXEMPI.xmp_parse.argtypes = [ctypes.c_void_p,
                                 ctypes.c_char_p,
                                 ctypes.c_size_t]
    strbuffer = strbuffer.encode('utf-8')
    EXEMPI.xmp_parse(xmp, strbuffer, len(strbuffer))


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
        The namespace associated if registered.

    Raises
    ------
    XMPError : if the corresponding library routine fails
    """
    EXEMPI.xmp_prefix_namespace_uri.restype = check_error
    EXEMPI.xmp_prefix_namespace_uri.argtypes = [ctypes.c_char_p,
                                                ctypes.c_void_p]

    _namespace = _string_new()
    EXEMPI.xmp_prefix_namespace_uri(prefix.encode(), _namespace)

    namespace = string_cstr(_namespace)
    _string_free(_namespace)

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
    registered_prefix : str
        The really registered prefix.

    Raises
    ------
    XMPError : if the corresponding library routine fails
    """
    EXEMPI.xmp_register_namespace.restype = check_error
    EXEMPI.xmp_register_namespace.argtypes = [ctypes.c_char_p,
                                              ctypes.c_char_p,
                                              ctypes.c_void_p]

    _registered_prefix = _string_new()

    EXEMPI.xmp_register_namespace(namespace_uri.encode(),
                                  prefix.encode(),
                                  _registered_prefix)

    registered_prefix = string_cstr(_registered_prefix)
    _string_free(_registered_prefix)

    return registered_prefix

def serialize(xmp, options, padding):
    """Serialize the XMP Packet.

    Wrapper for xmp_serialize library routine.

    Parameters
    ----------
    xmp : pointer
        The XMP packet.
    options : unsigned integer
        Options on how to write the XMP.
    padding : int
        Number of bytes of padding, useful for modifying embedded XMP in place.

    Returns
    -------
    item : str
        The formatted XMP.

    Raises
    ------
    XMPError : if the corresponding library routine fails
    """
    EXEMPI.xmp_serialize.restype = check_error
    EXEMPI.xmp_serialize.argtypes = [ctypes.c_void_p,
                                     ctypes.c_void_p,
                                     ctypes.c_uint32,
                                     ctypes.c_uint32]
    _item = _string_new()
    EXEMPI.xmp_serialize(xmp, _item, options, padding)

    item = string_cstr(_item)
    _string_free(_item)

    return item


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

    Returns
    -------
    item : str
        The formatted XMP.

    Raises
    ------
    XMPError : if the corresponding library routine fails
    """
    EXEMPI.xmp_serialize_and_format.restype = check_error
    EXEMPI.xmp_serialize_and_format.argtypes = [ctypes.c_void_p,
                                                ctypes.c_void_p,
                                                ctypes.c_uint32,
                                                ctypes.c_uint32,
                                                ctypes.c_char_p,
                                                ctypes.c_char_p,
                                                ctypes.c_int32]
    _item = _string_new()
    EXEMPI.xmp_serialize_and_format(xmp, _item, options, padding,
                                    newline.encode(), tab.encode(), indent)

    item = string_cstr(_item)
    _string_free(_item)

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

    Raises
    ------
    XMPError : if the corresponding library routine fails
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

    Raises
    ------
    XMPError : if the corresponding library routine fails
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
        Mask of options.

    Raises
    ------
    XMPError : if the corresponding library routine fails
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
        Mask of options.

    Raises
    ------
    XMPError : if the corresponding library routine fails
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


def set_property_date(xmp, schema, name, the_date, option_bits=0):
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
    the_date : datetime.datetime
        The date and time
    option_bits : unsigned int
        Mask of options.

    Raises
    ------
    XMPError : if the corresponding library routine fails
    """
    # Use a function callback instead of returning a boolean value.
    EXEMPI.xmp_set_property_date.restype = check_error
    EXEMPI.xmp_set_property_date.argtypes = [ctypes.c_void_p,
                                              ctypes.c_char_p,
                                              ctypes.c_char_p,
                                              ctypes.POINTER(XmpDateTime),
                                              ctypes.c_uint32]

    if the_date.tzinfo is not None:
        the_date = the_date.astimezone(pytz.utc)

    xmp_date = XmpDateTime()
    xmp_date.year = the_date.year
    xmp_date.month = the_date.month
    xmp_date.day = the_date.day
    xmp_date.hour = the_date.hour
    xmp_date.minute = the_date.minute
    xmp_date.second = the_date.second
    xmp_date.tzSign = 0
    xmp_date.tzHour = 0
    xmp_date.tzMinute = 0
    xmp_date.nanoSecond = 0

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
        Mask of options.

    Raises
    ------
    XMPError : if the corresponding library routine fails
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
        Mask of options.

    Raises
    ------
    XMPError : if the corresponding library routine fails
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
        Mask of options.

    Raises
    ------
    XMPError : if the corresponding library routine fails
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
    pystr : UTF-8 str
        Python string
    """
    EXEMPI.xmp_string_cstr.restype = ctypes.c_char_p
    EXEMPI.xmp_string_cstr.argtypes = [ctypes.c_void_p]
    cstr = EXEMPI.xmp_string_cstr(xmpstr)
    return cstr.decode('utf-8')


def _string_free(xmp_string):
    """Free an XmpStringPtr.

    Wrapper for xmp_string_free library routine.  You should not need to call
    this function.

    Parameters
    ----------
    xmp_string : exempi XmpStringPtr
        The resource to free.
    """
    EXEMPI.xmp_string_free.argtypes = [ctypes.c_void_p]
    EXEMPI.xmp_string_free(xmp_string)


def _string_new():
    """Wrapper for xmp_string_new library routine.  You should not need to call
    this function.

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


def check_error(success):
    """Set a generic function as the restype attribute of all exempi
    functions that return a boolean value.  This way we do not have to check
    for error status in each wrapping function and an exception will always be
    appropriately raised.
    """
    if not success:
        error_msg = ERROR_MESSAGE[EXEMPI.xmp_get_error()]
        msg = 'Exempi function failure ("{0}").'.format(error_msg)
        raise XMPError(msg)
