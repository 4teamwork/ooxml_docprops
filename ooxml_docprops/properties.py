"""Representation of the Custom DocProperties Part of an OOXML Document.

Relevant parts of standards:
- ECMA-376 4th edition Part 1: Section 13.2 (Package Structure)
- ECMA-376 4th edition Part 1: Section 15.2.12.2 (Custom File Properties Part)
- ECMA-376 4th edition Part 1: Section 22.3 (Custom Properties)

http://www.ecma-international.org/publications/standards/Ecma-376.htm
"""

from config import CUSTOM_PROPERTY_FMTID
from config import NAMESPACES
from config import NSMAP
from datatypes import DataTypeConverter
from datatypes import DataTypeValidator
from lxml import etree
from package import OOXMLPackage
import config
import os


class CustomPropertiesPart(object):
    def __init__(self, docprops_path):
        self.filepath = docprops_path
        self._properties_tree = etree.parse(open(docprops_path))
        self.converter = DataTypeConverter()
        self.validator = DataTypeValidator()

    def write_back(self):
        xml = etree.tostring(self._properties_tree, pretty_print=True,
                             xml_declaration=True, encoding='utf-8')
        with open(self.filepath, 'w') as f:
            f.write(xml)

    def set_property_value(self, name, value):
        property_node = self.get_property_node(name)
        value_type_node = property_node.getchildren()[0]
        self.validator.validate(value_type_node, value)
        value = self.converter.convert_value(value)
        value_type_node.text = value
        self.write_back()

    def get_property_value(self, name):
        property_node = self.get_property_node(name)
        value_type_node = property_node.getchildren()[0]
        value = self.converter.convert_node(value_type_node)
        return value

    def has_property(self, name):
        prop = self.get_property_node(name)
        return prop is not None

    def get_property_names(self):
        xpath = '/c:Properties/c:property'
        nodes = self._properties_tree.xpath(xpath, namespaces=NSMAP)
        names = [n.attrib['name'] for n in nodes]
        return names

    def get_max_pid(self):
        xpath = '/c:Properties/c:property'
        nodes = self._properties_tree.xpath(xpath, namespaces=NSMAP)
        if nodes == []:
            # No properties yet. Property IDs must start at 2 (sic!),
            # so returning 1 will lead to a new PID of 2.
            return 1
        max_pid = max(int(n.attrib['pid']) for n in nodes)
        return max_pid

    def add_property(self, name, value):
        max_pid = self.get_max_pid()
        new_pid = str(max_pid + 1)
        root = self._properties_tree.getroot()

        new_property = etree.SubElement(root, '{%s}property' %
            NAMESPACES['CUSTOM_PROPS'])
        new_property.attrib['fmtid'] = CUSTOM_PROPERTY_FMTID
        new_property.attrib['pid'] = new_pid
        new_property.attrib['name'] = name

        value_type = self.converter.determine_value_type(value)
        vt = etree.SubElement(new_property, '{%s}%s' % (
            NAMESPACES['VTYPES'], value_type))
        self.validator.validate(vt, value)
        value = self.converter.convert_value(value)
        vt.text = value
        self.write_back()

    def update_property(self, name, value):
        if self.has_property(name):
            self.set_property_value(name, value)
        else:
            self.add_property(name, value)

        if config.DEBUG:
            value = self.get_property_value(name)
            print "Reading out property '%s' again:" % name
            print "    %s = %s" % (name, value)

    def get_property_node(self, name):
        xpath = '/c:Properties/c:property[@name="%s"]' % name
        nodes = self._properties_tree.xpath(xpath, namespaces=NSMAP)
        try:
            prop = nodes[0]
        except IndexError:
            prop = None
        return prop


class OOXMLDocument(OOXMLPackage):

    def __enter__(self):
        OOXMLPackage.__enter__(self)
        self.properties = CustomPropertiesPart(self.get_docprops_path())
        return self

    def get_relationships(self):
        rels_path = os.path.join(self.workdir, '_rels', '.rels')
        with open(rels_path) as rels_xml_file:
            rels_xml = etree.parse(rels_xml_file)
        relationships = rels_xml.xpath('/r:Relationships/r:Relationship',
                                       namespaces=NSMAP)
        return relationships

    def get_docprops_path(self):
        relationships = self.get_relationships()

        custom_props_rel = None
        for rel in relationships:
            if rel.attrib['Type'] == NAMESPACES['CUSTOM_PROPS_REL']:
                custom_props_rel = rel

        if custom_props_rel is None:
            raise Exception("No rel for custom props found")

        target = custom_props_rel.attrib['Target']
        docprops_path = os.path.join(self.workdir, target)
        return docprops_path

    def update_properties(self, metadata):
        for (key, value) in metadata.items():
            self.properties.update_property(key, value)


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
