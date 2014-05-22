from ooxml_docprops.config import SUPPORTED_MIME_TYPES
from ooxml_docprops.properties import OOXMLDocument


def update_properties(document, metadata):
    """Update custom doc properties in the document specified by path
    `document` with properties from `metadata`. Modifies the document in place!
    """
    with OOXMLDocument(document) as doc:
        doc.update_properties(metadata)


def read_properties(document):
    """Read custom doc properties from the file `document`.
    """
    with OOXMLDocument(document, read_only=True) as doc:
        for name in doc.properties.get_property_names():
            value = doc.properties.get_property_value(name)
            yield (name, value)


def is_supported_mimetype(mime_type):
    return mime_type in SUPPORTED_MIME_TYPES
