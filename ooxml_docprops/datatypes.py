"""Definitions of ValueTypes used in OOXML and corresponding converters
and validators.

Relevant parts of standards:
- ECMA-376 4th edition Part 1: Section 22.4 (Variant Types)
  http://www.ecma-international.org/publications/standards/Ecma-376.htm
"""

from datetime import date
from datetime import datetime
from datetime import time
from lxml.etree import QName
import iso8601


INT_VTYPES = ('i1', 'i2', 'i3', 'i4', 'i8', 'int')
STR_VTYPES = ('lpstr', 'lpwstr')


class ValidationError(Exception):
    """
    """


class DataTypeConverter(object):

    def convert_value(self, value):
        """Convert Python data types to the corresponding unicode
        representation to be set as the text of the value type node.
        """
        if isinstance(value, basestring):
            # Always pass unicode to lxml API
            if isinstance(value, str):
                value = value.decode('utf-8')
            return value
        elif isinstance(value, bool):
            return value and u'true' or u'false'
        elif isinstance(value, int):
            return str(value).encode('utf-8')
        elif isinstance(value, datetime):
            return value.isoformat()
        else:
            raise Exception("Unsupported value type")

    def convert_node(self, vt_node):
        """Convert a value type node to a native Python data type.
        """
        tag = QName(vt_node).localname
        value = vt_node.text
        if tag in STR_VTYPES:
            return value
        elif tag in INT_VTYPES:
            return int(value)
        elif tag == 'bool':
            return value.lower() == 'true'
        elif tag == 'filetime':
            # use None as default timezone to avoid converting naive to aware
            return iso8601.parse_date(value, default_timezone=None)
        else:
            raise Exception("Unsupported value type: %s" % tag)

    def determine_value_type(self, value):
        """Given a Python data type, determine the correct value type node
        type.
        """
        if isinstance(value, basestring):
            return 'lpwstr'
        elif isinstance(value, bool):
            return 'bool'
        elif isinstance(value, int):
            return 'i4'
        elif isinstance(value, datetime):
            return 'filetime'
        else:
            raise Exception("Unsupported value type: %r" % value)


class DataTypeValidator(object):

    def validate(self, vt_node, value):
        """Given a value type node and a native Python data type, check if
        the two types are compatible.
        """
        tag = QName(vt_node).localname
        if tag in STR_VTYPES:
            required_type = basestring
        elif tag == 'bool':
            required_type = bool
        elif tag in INT_VTYPES:
            required_type = int
        elif tag == 'filetime':
            required_type = datetime
        else:
            raise Exception("Unsupported value type: %s" % tag)

        if not isinstance(value, required_type):
            raise ValidationError(
                "Value %r of type %s is invalid for node %s" % (
                    value, type(value), vt_node))
