# -*- coding: utf-8 -*-
#
# Copyright (c) 2008-2009, European Space Agency & European Southern
# Observatory (ESA/ESO)
# Copyright (c) 2008-2009, CRS4 - Centre for Advanced Studies, Research and
# Development in Sardinia
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
#     * Neither the name of the European Space Agency, European Southern
#       Observatory, CRS4 nor the names of its contributors may be used to
#       endorse or promote products derived from this software without specific
#       prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY ESA/ESO AND CRS4 ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL ESA/ESO BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER # IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE

"""
A module for parsing, manipulating, and serializing XMP data. The core module
has no knowledge of files. The core API is provided by the :class:`XMPMeta` and
:class:`XMPIterator` classes.
"""

import re
import sys

from . import XMPError
from . import consts
from .consts import options_mask, has_option
from .consts import XMP_SERIAL_OPTIONS
from .consts import XMP_PROP_OPTIONS

from . import exempi as _cexempi

__all__ = ['XMPMeta','XMPIterator']


def _remove_bom(xstr):
    """Remove BOM (byte order marker) from a string."""
    # Python 2.7 cannot encode from ascii to utf-8 (or utf-8 to ascii) when an
    # XMP packet contains the XMP packet wrapper with the BOM in place.  Just
    # get rid of it if we find it.
    regex = re.compile(r"""\s*<\?xpacket\s*
                           begin=\"(?P<bom>.*)\"\s*
                           id=\"W5M0MpCehiHzreSzNTczkc9d\"\?>""",
                           re.UNICODE | re.VERBOSE)
    match = regex.match(xstr)
    if match is not None:
        # Ok we matched up to the BOM.  Get rid of it.
        bom_start, bom_end = match.span('bom')
        xstr = xstr[0:bom_start] + xstr[bom_end:]

    return xstr

def _remove_trailing_whitespace(xstr):
    """Remove trailing white space.
    
    There is a lot of white space between </x:xmpmeta> and <?xpacket end="w"?>,
    but we don't need that for presentation purposes.
    """
    regex = re.compile(r"""</x:xmpmeta>
                           (?P<whitespace>\s*)
                           <\?xpacket\s
                           end="w"\?>""", re.UNICODE | re.VERBOSE)
    match = regex.search(xstr)
    if match is not None:
        # Ok we matched up to the whitespace, get rid of it.
        ws_start, ws_end = match.span('whitespace')
        xstr = xstr[0:ws_start] + '\n' + xstr[ws_end:]

    return xstr

def _force_rdf_to_utf8(xstr):
    """Force RDF to unicode on 2.7, removing BOM in the process."""

    xstr = _remove_bom(xstr)
    return xstr.decode('utf-8')


class XMPMeta(object):
    """
    XMPMeta is the class providing the core services of the library
    """

    def __init__( self, **kwargs ):
        """
        :param xmp_str Optional.
        :param xmp_internal_ref Optional - used for internal purposes.
        """
        if '_xmp_internal_ref' in kwargs:
            self.xmpptr = kwargs['_xmp_internal_ref']
        else:
            self.xmpptr = _cexempi.new_empty()

            if 'xmp_str' in kwargs:
                self.parse_from_str( kwargs['xmp_str'] )

        self.iterator = None

    def __del__(self):
        """
        Ensures memory is deallocated when destroying object.
        """
        if self.xmpptr is not None:
            _cexempi.free(self.xmpptr)

        if self.iterator is not None:
            del self.iterator


    def __iter__(self):
        """
        Defines XMPIterator as an iterator for this class' instances
        """

        if self.iterator is None:
            self.iterator = XMPIterator(self)

        return self.iterator

    def __unicode__(self):
        """Return a unicode-friendly representation.
        """
        xstr = self.serialize_to_str()
        return xstr

    def __repr__(self):
        """We should strive to make this eval-able, but here it is difficult.
        """
        return str(self)

    def __str__(self):
        """ Prints a nice serialization of the XMPMeta object.

        Must be a bytes string in Python 2.
        """
        xstr = self.serialize_to_str()
        xstr = _remove_trailing_whitespace(xstr)
        if sys.hexversion < 0x03000000:
            # The BOM is not important, just remove it.
            xstr = _remove_bom(xstr)
            return xstr.encode('UTF-8', 'replace')
        else: 
            return xstr

    def __eq__(self, other):
        """ Checks if two XMPMeta objects are equal."""
        return self.xmpptr == other.xmpptr

    def __ne__(self, other):
        """ Checks if two XMPMeta object are not equal. """
        return self.xmpptr != other.xmpptr

    # -------------------------------------
    # Functions for getting property values
    # -------------------------------------
    def get_property(self, schema_ns, prop_name):
        """Retrieves property value.

        This is the simplest property accessor: use this to retrieve the values
        of top-level simple properties.

        :param str schema_ns: The namespace URI for the property; can be null or
            the empty string if the first component of the prop_name path
            contains a namespace prefix.
        :param str prop_name: The name of the property. Can be a general path
            expression, must not be null or the empty string. The first
            component can be a namespace prefix; if present without a schema_ns
            value, the prefix specifies the namespace.

        :returns: The property's value if the property exists.

        :raises: IOError if exempi library routine fails.

        .. todo:: Make get_property optionally return keywords describing
            property's options
        """
        value, _ = _cexempi.get_property(self.xmpptr, schema_ns, prop_name)
        return value


    def get_array_item(self, schema_ns, array_prop_name, index):
        """Get an item from an array property.

        Items are accessed by an integer index

        :param str schema_ns: The namespace URI for the property; can be null or
            the empty string if the first component of the prop_name path
            contains a namespace prefix.
        :param str array_prop_name: The name of the array property. Can be a
            general path expression, must not be null or the empty string. The
            first component can be a namespace prefix; if present without a
            schema_ns value, the prefix specifies the namespace.
        :param int index:  The 1-based index of the item.

        :raises: IOError if exempi library routine fails.

        .. todo:: Make get_array_item optionally return keywords describing
            array item's options
        """
        prop, _ = _cexempi.get_array_item(self.xmpptr, schema_ns,
                                          array_prop_name, index)
        return prop


    # -------------------------------------
    # Functions for setting property values
    # -------------------------------------
    def set_property(self, schema_ns, prop_name, prop_value, **kwargs ):
        """Creates or sets a property value.

        The method takes optional keyword aguments that describe the property.
        You can use these functions to create empty arrays and structs by
        setting appropriate option flags.  When you assign a value, all levels
        of a struct that are implicit in the assignment are created if
        necessary; append_array_item() implicitly creates the named array if
        necessary.

        :param str schema_ns: The namespace URI; see get_property().
        :param str prop_name: The name of the property. Can be a general path
            expression, must not be null or the empty string; see
            get_property() for namespace prefix usage.
        :param str prop_value: The new item value.
        :param **kwargs: Optional keyword arguments describing the options;
            must much an already existing option from consts.XMP_PROP_OPTIONS

        :raises: IOError if exempi library routine fails.
        """
        options = options_mask(XMP_PROP_OPTIONS, **kwargs) if kwargs else 0
        _cexempi.set_property(self.xmpptr, schema_ns, prop_name, prop_value,
                              options)

    def set_array_item(self, schema_ns, array_name, item_index, item_value,
                       **kwargs):
        """Creates or sets the value of an item within an array.

        Items are accessed by an integer index, where the first item has index
        1.  This function creates the item if necessary, but the array itself
        must already exist: use append_array_item() to create arrays.  A new
        item is automatically appended if the index is the array size plus 1;
        to insert a new item before or after an existing item, use kwargs.

        :param str schema_ns:  The namespace URI; see get_property().
        :param str array_name: The name of the array property. Can be a
            general path expression, must not be null or the empty string. The
            first component can be a namespace prefix; if present without a
            schema_ns value, the prefix specifies the namespace.
        :param int item_index: The 1-based index of the desired item.
        :param item_value:     The new item value.
        :param **kwargs:       Optional keywork arguments describing the array
            type and insertion location for a new item.  The type, if
            specified, must match the existing array type,
            prop_array_is_ordered, prop_array_is_alternate, or
            prop_array_is_alt_text. Default (no keyword parameters) matches the
            existing array type.

        :raises: IOError if exempi library routine fails.
        """
        options = options_mask(XMP_PROP_OPTIONS, **kwargs) if kwargs else 0
        _cexempi.set_array_item(self.xmpptr, schema_ns, array_name, item_index,
                                item_value, options)


    def append_array_item(self, schema_ns, array_name, item_value,
                          array_options=None, **kwargs ):
        """Adds an item to an array, creating the array if necessary.

        This function simplifies construction of an array by not requiring that
        you pre-create an empty array. The array that is assigned is created
        automatically if it does not yet exist. If the array exists, it must
        have the form specified by the options.  Each call appends a new item to
        the array.

        :param str schema_ns:   The namespace URI; see get_property().
        :param str array_name:  The name of the array property. Can be a
            general path expression, must not be null or the empty string. The
            first component can be a namespace prefix; if present without a
            schema_ns value, the prefix specifies the namespace.
        :param str item_value:  The new item value.
        :param dict array_options:  An optional dictionary of keywords from
            XMP_PROP_OPTIONS describing the array type to create.
        :param **kwargs:        Optional keyword arguments describing the item
            type to create.
        """
        if array_options is not None:
            array_options = options_mask(XMP_PROP_OPTIONS, **array_options)
        else:
            array_options = 0
        options = options_mask(XMP_PROP_OPTIONS, **kwargs) if kwargs else 0
        _cexempi.append_array_item(self.xmpptr, schema_ns, array_name,
                                   array_options, item_value, options)


    # -----------------------------------------------
    # Functions accessing properties as binary values
    # -----------------------------------------------
    def get_property_bool(self, schema, name):
        """Retrieve a boolean property.

        :param str schema_ns:   The namespace URI; see get_property().
        :param str array_name:  The name of the array property. Can be a
            general path expression, must not be null or the empty string. The
            first component can be a namespace prefix; if present without a
            schema_ns value, the prefix specifies the namespace.

        :raises: IOError if operation fails.

        :returns: The boolean property value.

        .. todo:: Make get_property_bool optionally return keywords describing
            property's options
        """
        value, _ = _cexempi.get_property_bool(self.xmpptr, schema, name)
        return value


    def get_property_int(self, schema_ns, name):
        """Retrieve an integer property.

        :param str schema_ns:   The namespace URI; see get_property().
        :param str prop_name:  The name of the property. Can be a general path
            expression, must not be null or the empty string. The
            first component can be a namespace prefix; if present without a
            schema_ns value, the prefix specifies the namespace.

        :raises: IOError if operation fails.

        :returns: The integer property value.

        .. todo:: Make get_property_int optionally return keywords describing
            property's options
        """
        value, _ = _cexempi.get_property_int32(self.xmpptr, schema_ns, name)
        return value

    def get_property_long(self, schema_ns, prop_name):
        """Retrieve a long (int64) property.

        :param str schema_ns:   The namespace URI; see get_property().
        :param str prop_name:  The name of the property. Can be a general path
            expression, must not be null or the empty string. The
            first component can be a namespace prefix; if present without a
            schema_ns value, the prefix specifies the namespace.

        :raises: IOError if operation fails.

        :returns: The 64-bit integer property value.

        .. todo:: Make get_property_int optionally return keywords describing
            property's options
        """
        value, _ = _cexempi.get_property_int64(self.xmpptr,
                                               schema_ns, prop_name)
        return value


    def get_property_float(self, schema_ns, prop_name):
        """Return a property value as floating point.

        :param str schema_ns:   The namespace URI; see get_property().
        :param str prop_name:  The name of the property. Can be a general path
            expression, must not be null or the empty string. The
            first component can be a namespace prefix; if present without a
            schema_ns value, the prefix specifies the namespace.

        :raises: IOError if operation fails.

        :returns: The floating point property value.

        .. todo:: Make get_property_float optionally return keywords describing
            property's options
        """
        val, _ = _cexempi.get_property_float(self.xmpptr, schema_ns, prop_name)
        return val


    def get_property_datetime(self, schema_ns, prop_name ):
        """Retrieve a datetime property.

        :param str schema_ns:   The namespace URI; see get_property().
        :param str prop_name:  The name of the property. Can be a general path
            expression, must not be null or the empty string. The
            first component can be a namespace prefix; if present without a
            schema_ns value, the prefix specifies the namespace.

        :returns: datetime.datetime instance.

        :raises: IOError if operation fails.
        """
        prop, _ = _cexempi.get_property_date(self.xmpptr, schema_ns, prop_name)
        return prop


    def get_localized_text(self, schema_ns, alt_text_name, generic_lang,
                           specific_lang):
        """Returns information about a selected item in an alt-text array.

        :param str schema_ns:   The namespace URI; see get_property().
        :param str alt_text_name:  The name of the alt-text array. May be a
            general path expression, must not be None or the empty string.  Has
            the same namespace prefix usage as propName in GetProperty.
        :param str generic_lang:  The name of the generic language as an RFC
            3066 primary subtag. May be None or the empty string if no generic
            language is wanted.
        :param str specific_lang: The name of the specific language as an RFC
            3066 tag. Must not be null or the empty string.

        :raises: IOError if operation fails.

        :return: The property's value.
        """
        value, _, _ = _cexempi.get_localized_text(self.xmpptr, schema_ns,
                                                  alt_text_name, generic_lang,
                                                  specific_lang)
        return value


    def set_property_bool(self, schema_ns, prop_name, prop_value, **kwargs ):
        """Set a boolean property.

        :param str schema_ns: The namespace URI; see get_property().
        :param str prop_name: The name of the property. Can be a general path
            expression, must not be null or the empty string; see
            get_property() for namespace prefix usage.
        :param bool prop_value: The new item value.
        :param **kwargs: Optional keyword arguments describing the options;
            must much an already existing option from consts.XMP_PROP_OPTIONS

        :raises: IOError if exempi library routine fails.
        """
        options = options_mask(XMP_PROP_OPTIONS, **kwargs) if kwargs else 0
        _cexempi.set_property_bool(self.xmpptr, schema_ns, prop_name,
                                   bool(prop_value), options)

    def set_property_int(self, schema_ns, prop_name, prop_value, **kwargs ):
        """Set an integer property.

        :param str schema_ns: The namespace URI; see get_property().
        :param str prop_name: The name of the property. Can be a general path
            expression, must not be null or the empty string; see
            get_property() for namespace prefix usage.
        :param int prop_value: The new item value.
        :param **kwargs: Optional keyword arguments describing the options;
            must much an already existing option from consts.XMP_PROP_OPTIONS

        :raises: IOError if exempi library routine fails.
        """
        options = options_mask(XMP_PROP_OPTIONS, **kwargs) if kwargs else 0
        _cexempi.set_property_int32(self.xmpptr, schema_ns, prop_name,
                                    int(prop_value), options)

    def set_property_long(self, schema_ns, prop_name, prop_value, **kwargs ):
        """Set a long integer (int64) property.

        :param str schema_ns: The namespace URI; see get_property().
        :param str prop_name: The name of the property. Can be a general path
            expression, must not be null or the empty string; see
            get_property() for namespace prefix usage.
        :param long prop_value: The new item value.
        :param **kwargs: Optional keyword arguments describing the options;
            must much an already existing option from consts.XMP_PROP_OPTIONS

        :raises: IOError if exempi library routine fails.
        """
        options = options_mask(XMP_PROP_OPTIONS, **kwargs) if kwargs else 0
        _cexempi.set_property_int64(self.xmpptr, schema_ns, prop_name,
                                    prop_value, options)

    def set_property_float(self, schema_ns, prop_name, prop_value, **kwargs ):
        """Set a floating point property.

        :param str schema_ns: The namespace URI; see get_property().
        :param str prop_name: The name of the property. Can be a general path
            expression, must not be null or the empty string; see
            get_property() for namespace prefix usage.
        :param float prop_value: The new item value.
        :param **kwargs: Optional keyword arguments describing the options;
            must much an already existing option from consts.XMP_PROP_OPTIONS

        :raises: IOError if exempi library routine fails.
        """
        options = options_mask(XMP_PROP_OPTIONS, **kwargs) if kwargs else 0
        _cexempi.set_property_float(self.xmpptr, schema_ns, prop_name,
                                    float(prop_value), options)


    def set_property_datetime(self, schema_ns, prop_name, prop_value, **kwargs):
        """Set a datetime property.

        :param str schema_ns: The namespace URI; see get_property().
        :param str prop_name: The name of the property. Can be a general path
            expression, must not be null or the empty string; see
            get_property() for namespace prefix usage.
        :param datetime.datetime prop_value: The new datetime value.

        :raises: IOError if exempi library routine fails.
        """
        options = options_mask(XMP_PROP_OPTIONS, **kwargs) if kwargs else 0
        _cexempi.set_property_date(self.xmpptr, schema_ns, prop_name,
                                   prop_value, options)


    def set_localized_text(self, schema_ns, alt_text_name, generic_lang,
                           specific_lang, prop_value, **kwargs):
        """Creates or sets a localized text value.

        :param str schema_ns:     The namespace URI; see get_property().
        :param str alt_text_name: The name of the property. Can be a general
            path expression, must not be null or the empty string. The first
            component can be a namespace prefix.
        :param str generic_lang:  A valid generic language tag from RFC 3066
            specification (i.e. en for English).  Passing "x" for a generic
            language is allowed, but considered poor practice.  An empty string
            may be specified.
        :param str specific_lang: A specific language tag from RFC 3066
            specification (i.e en-US for US English).
        :param str prop_value:    Item value
        :param **kwargs:          Optional keyword arguments describing the
            options; must much an already existing option from
            consts.XMP_PROP_OPTIONS

        :raises: IOError if exempi library routine fails.
        """
        options = options_mask(XMP_PROP_OPTIONS, **kwargs) if kwargs else 0
        _cexempi.set_localized_text(self.xmpptr, schema_ns, alt_text_name,
                                    generic_lang, specific_lang, prop_value,
                                    options)


    # ------------------------------------------------
    # Functions for deleting and detecting properties.
    # ------------------------------------------------
    def delete_localized_text(self, schema_ns, alt_text_name, generic_lang,
                              specific_lang):
        """Remove a localized property.

        :param str schema_ns:   The namespace URI; see get_property().
        :param str alt_text_name:  The name of the alt-text array. May be a
            general path expression, must not be None or the empty string.  Has
            the same namespace prefix usage as propName in GetProperty.
        :param str generic_lang:  The name of the generic language as an RFC
            3066 primary subtag. May be null or the empty string if no generic
            language is wanted.
        :param str specific_lang: The name of the specific language as an RFC
            3066 tag. Must not be null or the empty string.

        :raises: XMPError if operation fails.
        """
        _cexempi.delete_localized_text(self.xmpptr, schema_ns, alt_text_name,
                                       generic_lang, specific_lang)


    def delete_property(self, schema_ns, prop_name ):
        """Delete a property from XMP packet.

        Deletes an XMP subtree rooted at a given property.  It is not an error
        if the property does not exist.

        :param str schema_ns: The namespace URI; see get_property().
        :param str prop_name: The name of the property; see get_property().
        """
        _cexempi.delete_property(self.xmpptr, schema_ns, prop_name)

    def does_property_exist(self, schema_ns, prop_name ):
        """Queries for existence of a property.

        :param str schema_ns: The namespace URI; see get_property().
        :param str prop_name: The name of the property; see get_property().

        :returns: True if the property exists, False otherwise.
        """
        return _cexempi.has_property(self.xmpptr, schema_ns, prop_name)


    def does_array_item_exist(self, schema_ns, array_name, item ):
        """Reports whether an item exists in an array.

        :param str schema_ns: The namespace URI; see get_property().
        :param str array_name: The name of the array; see get_property().
        :param str item:  The name of the item.

        :return: True if item is in array, False otherwise
        :rtype: bool
        """
        index = 0
        found = False
        while True:
            try:
                the_prop, _ = _cexempi.get_array_item(self.xmpptr, schema_ns,
                                                      array_name, index+1)
                index += 1
            except XMPError:
                # We've gone through the entire list. It does not exist.
                break
            if the_prop == item:
                found = True
                break

        return found

    # -------------------------------------
    # Functions for parsing and serializing
    # -------------------------------------
    # These functions support parsing serialized RDF into an XMP object, and
    # serializing an XMP object into RDF.  Serialization is always as UTF-8.
    def parse_from_str(self, xmp_packet_str, xmpmeta_wrap=False,
                       input_encoding=None ):
        """Parses RDF from a string into a XMP object.

        The input for parsing may be any valid Unicode encoding. ISO Latin-1 is
        also recognized, but its use is strongly discouraged.

        Note RDF string must contain an outermost <x:xmpmeta> object.

        :param str xmp_packet_str: String to parse.
        :param bool xmpmeta_wrap: Optional - If True, the string will be wrapped
            in an <x:xmpmeta> element.
        :param str input_encoding: Optional - If `xmp_packet_str` is a 8-bit
            string, it will by default be assumed to be UTF-8 encoded.
        :raises: IOError if operation fails.
        """
        if sys.hexversion < 0x03000000 and isinstance(xmp_packet_str, str):
            xmp_packet_str = _force_rdf_to_utf8(xmp_packet_str)
        if xmpmeta_wrap:
            fmt = u"<x:xmpmeta xmlns:x='adobe:ns:meta/'>{0}</x:xmpmeta>"
            xmp_packet_str = fmt.format(xmp_packet_str)

        _cexempi.parse(self.xmpptr, xmp_packet_str)


    def serialize_and_format(self, padding=0, newlinechr='\n', tabchr = '\t',
                             indent=0, **kwargs ):
        """Serializes an XMPMeta object into a string as RDF.

        Note, normally it is sufficient to use either `serialize_to_str` or
        `serialize_to_unicode` unless you need high degree of control over the
        serialization.

        The specified parameters must be logically consistent, an exception is
        raised if not. You cannot specify both `omit_packet_wrapper` along with
        `read_only_packet`, `include_thumbnail_pad`, or `exact_packet_length`.

        :param int padding: The number of bytes of padding, useful for modifying
            embedded XMP in place.
        :param str newlinechr: The new line character to use.
        :param str tabchr: The indentation character to use.
        :param int indent: The initial indentation level.
        :param bool omit_packet_wrapper: Do not include an XML packet wrapper.
        :param bool read_only_packet: Create a read-only XML packet wapper.
        :param bool use_compact_format: Use a highly compact RDF syntax and
            layout.
        :param bool include_thumbnail_pad: Include typical space for a JPEG
            thumbnail in the padding if no xmp:Thumbnails property is present.
        :param bool exact_packet_length: The padding parameter provides the
            overall packet length.
        :param bool write_alias_comments: Include XML comments for aliases.
        :param bool omit_all_formatting: Omit all formatting whitespace.
        :return: XMPMeta object serialized into a string as RDF.
        :rtype: utf-8 string.
        """
        options = options_mask( XMP_SERIAL_OPTIONS, **kwargs )
        return _cexempi.serialize_and_format(self.xmpptr, options, padding,
                                             newlinechr, tabchr, indent)



    def serialize_to_unicode( self, **kwargs ):
        """
        Serializes an XMPMeta object into a Unicode string as RDF and format.
        Note, this is wrapper around `serialize_to_str`.

        The specified parameters must be logically consistent, an exception
        is raised if not. You cannot specify both `omit_packet_wrapper` along
        with `read_only_packet`, `include_thumbnail_pad`, or
        `exact_packet_length`.

        :param int padding: The number of bytes of padding, useful for
            modifying embedded XMP in place.
        :param bool omit_packet_wrapper: Do not include an XML packet wrapper.
        :param bool read_only_packet: Create a read-only XML packet wapper.
        :param bool use_compact_format: Use a highly compact RDF syntax and
            layout.
        :param bool  include_thumbnail_pad: Include typical space for a JPEG
            thumbnail in the padding if no xmp:Thumbnails property is present.
        :param bool exact_packet_length: The padding parameter provides the
            overall packet length.
        :param bool write_alias_comments: Include XML comments for aliases.
        :param bool omit_all_formatting: Omit all formatting whitespace.
        :return: XMPMeta object serialized into a string as RDF.
        :rtype: `unicode` string.
        """
        obj =  self.serialize_to_str( **kwargs )
        return obj


    def serialize_to_str(self, padding = 0, **kwargs):
        """Serialize into a string (8-bit, UTF-8 encoded) as RDF and format.

        :param int padding: The number of bytes of padding, useful for
            modifying embedded XMP in place.
        :param bool omit_packet_wrapper: Do not include an XML packet wrapper.
        :param bool read_only_packet: Create a read-only XML packet wapper.
        :param bool use_compact_format: Use a highly compact RDF syntax and
            layout.
        :param bool include_thumbnail_pad: Include typical space for a JPEG
            thumbnail in the padding if no xmp:Thumbnails property is present.
        :param int exact_packet_length: The padding parameter provides the
            overall packet length.
        :param bool write_alias_comments: Include XML comments for aliases.
        :param bool omit_all_formatting: Omit all formatting whitespace.
        :returns: `str` 8-bit string in UTF-8 encoding (ready to be written to
            a file).
        """
        options = options_mask(XMP_SERIAL_OPTIONS, **kwargs)
        xstr = _cexempi.serialize(self.xmpptr, options, padding)
        return xstr


    # -------------------------------------
    # Misceallaneous functions
    # -------------------------------------
    def clone( self ):
        """
        Create a new XMP packet from this one.

        :returns:  Copy of XMP packet.
        :rtype: XMPMeta
        """
        newptr = _cexempi.copy( self.xmpptr )

        return (XMPMeta( _xmp_internal_ref = newptr ) if newptr else None)


    def count_array_items( self, schema_ns, array_name ):
        """
        count_array_items returns the number of a given array's items
        """
        count = 0
        while True:
            try:
                _, _ = _cexempi.get_array_item(self.xmpptr, schema_ns,
                                                      array_name, count+1)
                count += 1
            except XMPError:
                # We've gone through the entire list. It does not exist.
                break

        return count

    # -------------------------------------
    # Namespace Functions
    # -------------------------------------
    @staticmethod
    def get_prefix_for_namespace(namespace):
        """
        Check if a namespace is registered.

        Parameters:
        :param str namespace: the namespace to check.
        :returns: the associated prefix if registered
        :raises: IOError if exempi library routine fails.
        """
        return _cexempi.namespace_prefix(namespace)

    @staticmethod
    def get_namespace_for_prefix(prefix):
        """Checks if a prefix is registered.

        :param str prefix: The prefix to check.
        :returns: The associated namespace if registered.
        :raises: IOError if exempi library routine fails.
        """
        return _cexempi.prefix_namespace_uri(prefix)

    @staticmethod
    def register_namespace( namespace_uri, suggested_prefix ):
        """ Register a new namespace.

        :param str namespace_uri: the new namespace's URI
        :param str suggested prefix: the suggested prefix: note that is NOT
            guaranteed it'll be the actual namespace's prefix
        :returns: the actual registered prefix for the namespace
        """
        return _cexempi.register_namespace(namespace_uri, suggested_prefix)



class XMPIterator(object):
    """Provides means to iterate over a schema and properties.

    XMPIterator provides a uniform means to iterate over the schema and
    properties within an XMP object.  It is implemented according to Python's
    iterator protocol and it is the iterator for XMPMeta class.

    :param obj xmp_obj:   an XMPMeta instance
    :param str schema_ns: Optional namespace URI to restrict the iteration.
    :param str prop_name: Optional property name to restrict the iteration.
    :param **kwargs:      Optional keyword arguments from XMP_ITERATOR_OPTIONS
    :returns: an iterator for the given xmp_obj
    """
    def __init__( self, xmp_obj, schema_ns=None, prop_name=None, **kwargs ):
        if kwargs:
            self.options = options_mask(consts.XMP_ITERATOR_OPTIONS, **kwargs)
        else:
            self.options = 0

        self.xmpiteratorptr = _cexempi.iterator_new(xmp_obj.xmpptr, schema_ns,
                                                    prop_name, self.options)
        self.schema = schema_ns
        self.prop_name = prop_name

    def __del__(self):
        _cexempi.iterator_free(self.xmpiteratorptr)

    def __iter__(self):
        return self

    def next(self):
        """
        Implements iterator protocol for 2.X

        .. todo:: Suppress this in sphinx docs

        :raises: StopIteration
        """
        return self.__next__()

    def __next__(self):
        """
        Implements iterator protocol for 3.X

        :raises: StopIteration
        """
        schema, name, value, options = _cexempi.iterator_next(self.xmpiteratorptr)

        #decode option bits into a human-readable format (that is, a dict)
        opts = { 'VALUE_IS_URI'     : False,
                 'IS_QUALIFIER'     : False,
                 'HAS_QUALIFIERS'   : False,
                 'HAS_LANG'         : False,
                 'HAS_TYPE'         : False,
                 'VALUE_IS_STRUCT'  : False,
                 'VALUE_IS_ARRAY'   : False,
                 'ARRAY_IS_ORDERED' : False,
                 'ARRAY_IS_ALT'     : False,
                 'ARRAY_IS_ALTTEXT' : False,
                 'IS_ALIAS'         : False,
                 'HAS_ALIASES'      : False,
                 'IS_INTERNAL'      : False,
                 'IS_STABLE'        : False,
                 'IS_DERIVED'       : False,
                 'IS_SCHEMA'        : False, }

        for opt in opts:
            if has_option(options.value, getattr(consts, 'XMP_PROP_' + opt)):
                opts[opt] = True

        return(schema, name, value, opts)

    def skip(self, **kwargs ):
        """Skips some portion of the remaining iterations.

        :param **kwargs: Optional keyword parameters from XMP_SKIP_OPTIONS to
            control the iteration
        :returns: None
        :rtype: NoneType
        """
        if kwargs:
            options = options_mask(consts.XMP_SKIP_OPTIONS, **kwargs)
        else:
            options = 0
        _cexempi.iterator_skip(self.xmpiteratorptr, options)
