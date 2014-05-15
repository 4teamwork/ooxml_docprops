"""Common configuration options and namespaces used throughout the package.
"""

DEBUG = False

CUSTOM_PROPERTY_FMTID = '{D5CDD505-2E9C-101B-9397-08002B2CF9AE}'

NAMESPACES = {
    'VTYPES':           'http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes',
    'CUSTOM_PROPS_REL': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/custom-properties',
    'RELATIONSHIPS':    'http://schemas.openxmlformats.org/package/2006/relationships',
    'CUSTOM_PROPS':     'http://schemas.openxmlformats.org/officeDocument/2006/custom-properties',
}


NSMAP = {'r': NAMESPACES['RELATIONSHIPS'],
         'c': NAMESPACES['CUSTOM_PROPS']}
