"""Common configuration options and namespaces used throughout the package.
"""
import os

DEBUG = False

CUSTOM_PROPERTY_FMTID = '{D5CDD505-2E9C-101B-9397-08002B2CF9AE}'
CUSTOM_PROPERTY_DEFAULT_PATH = os.path.join('docProps', 'custom.xml')

NAMESPACES = {
    'VTYPES':           'http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes',
    'CUSTOM_PROPS_REL': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/custom-properties',
    'RELATIONSHIPS':    'http://schemas.openxmlformats.org/package/2006/relationships',
    'CUSTOM_PROPS':     'http://schemas.openxmlformats.org/officeDocument/2006/custom-properties',
}

# this is used to hack around the required namespace prefix for xpath
NSMAP = {
    'r': NAMESPACES['RELATIONSHIPS'],
    'c': NAMESPACES['CUSTOM_PROPS'],
}

NSMAP_CUSTOM_PROPERTIES = {
    None: NAMESPACES['CUSTOM_PROPS'],  # None means default namespace
    'vt': NAMESPACES['VTYPES'],
}
