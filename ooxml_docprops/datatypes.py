"""Definitions of ValueTypes used in OOXML and corresponding converters
and validators.
"""

from lxml.etree import QName


INT_VTYPES = ('i1', 'i2', 'i3', 'i4', 'i8', 'int')
STR_VTYPES = ('lpstr', 'lpwstr')


class ValidationError(Exception):
    """
    """


class DataTypeConverter(object):

    def convert_value(self, value):
        if isinstance(value, basestring):
            # TODO: Deal with non-ASCII characters / unicode
            return value
        elif isinstance(value, int):
            return str(value)
        elif isinstance(value, bool):
            return value and 'true' or 'false'
        else:
            raise Exception("Unsupported value type")

    def convert_node(self, vt_node):
        tag = QName(vt_node).localname
        value = vt_node.text
        if tag in STR_VTYPES:
            return value
        elif tag in INT_VTYPES:
            return int(value)
        elif tag == 'bool':
            return value.lower() == 'true'
        else:
            raise Exception("Unsupported value type: %s" % tag)

    def determine_value_type(self, value):
        if isinstance(value, int):
            return 'i4'
        elif isinstance(value, basestring):
            return 'lpwstr'
        elif isinstance(value, bool):
            return 'bool'
        else:
            raise Exception("Unsupported value type: %r" % value)


class DataTypeValidator(object):

    def validate(self, vt_node, value):
        tag = QName(vt_node).localname
        if tag in INT_VTYPES:
            required_type = int
        elif tag in STR_VTYPES:
            required_type = basestring
        elif tag == 'bool':
            required_type = bool
        else:
            raise Exception("Unsupported value type: %s" % tag)

        if not isinstance(value, required_type):
            raise ValidationError(
                "Value %r of type %s is invalid for node %s" % (
                    value, type(value), vt_node))
