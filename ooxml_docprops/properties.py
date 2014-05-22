"""Representation of the Custom DocProperties Part of an OOXML Document.

Relevant parts of standards:
- ECMA-376 4th edition Part 1: Section 13.2 (Package Structure)
- ECMA-376 4th edition Part 1: Section 15.2.12.2 (Custom File Properties Part)
- ECMA-376 4th edition Part 1: Section 22.3 (Custom Properties)

http://www.ecma-international.org/publications/standards/Ecma-376.htm
"""

from config import CONTENT_TYPES_PATH
from config import CUSTOM_PROPERTY_CONTENT_TYPE
from config import CUSTOM_PROPERTY_DEFAULT_PATH
from config import CUSTOM_PROPERTY_FMTID
from config import NAMESPACES
from config import NSMAP
from config import NSMAP_CUSTOM_PROPERTIES
from datatypes import DataTypeConverter
from datatypes import DataTypeValidator
from lxml import etree
from package import OOXMLPackage
import config
import os
import re


class Part(object):
    """An XML part of the OOXML document.

    Represents one internal file of the OOXML document.
    """

    def __init__(self, path):
        self.filepath = path
        self.tree = etree.parse(open(self.filepath))

    def write_xml_file(self):
        xml = etree.tostring(self.tree, pretty_print=True,
                             xml_declaration=True, encoding='utf-8')
        with open(self.filepath, 'w') as f:
            f.write(xml)


class CustomPropertiesPart(Part):

    def __init__(self, docprops_path):
        super(CustomPropertiesPart, self).__init__(docprops_path)

        self.converter = DataTypeConverter()
        self.validator = DataTypeValidator()

    def set_property_value(self, name, value):
        property_node = self.get_property_node(name)
        value_type_node = property_node.getchildren()[0]
        self.validator.validate(value_type_node, value)
        value = self.converter.convert_value(value)
        value_type_node.text = value

        self.write_xml_file()

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
        nodes = self.tree.xpath(xpath, namespaces=NSMAP)
        names = [n.attrib['name'] for n in nodes]
        return names

    def get_max_pid(self):
        xpath = '/c:Properties/c:property'
        nodes = self.tree.xpath(xpath, namespaces=NSMAP)
        if nodes == []:
            # No properties yet. Property IDs must start at 2 (sic!),
            # so returning 1 will lead to a new PID of 2.
            return 1
        max_pid = max(int(n.attrib['pid']) for n in nodes)
        return max_pid

    def add_property(self, name, value):
        max_pid = self.get_max_pid()
        new_pid = str(max_pid + 1)
        root = self.tree.getroot()

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

        self.write_xml_file()

    def update(self, metadata):
        for (key, value) in metadata.items():
            self.update_property(key, value)
        return self

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
        nodes = self.tree.xpath(xpath, namespaces=NSMAP)
        try:
            prop = nodes[0]
        except IndexError:
            prop = None
        return prop


class EmptyPropertiesPart(object):

    def __init__(self, workdir):
        self.workdir = workdir

    def update(self, metadata):
        if not metadata:
            return

        self.add_properties_to_content_types()
        self.add_properties_to_relationships()
        properties_path = self._create_custom_props_file()
        return CustomPropertiesPart(properties_path).update(metadata)

    def add_properties_to_content_types(self):
        OOXMLContentTypes(self.workdir).create_custom_props_content_types()

    def add_properties_to_relationships(self):
        relationships = OOXMLRelationships(self.workdir)
        return relationships.create_custom_props_relationship()

    def _create_custom_props_file(self):
        custom_props_path = os.path.join(self.workdir,
                                         CUSTOM_PROPERTY_DEFAULT_PATH)
        assert not os.path.exists(custom_props_path)

        with open(custom_props_path, 'w') as f:
            root = etree.Element('Properties', nsmap=NSMAP_CUSTOM_PROPERTIES)
            xml = etree.tostring(etree.ElementTree(root), pretty_print=True,
                                 xml_declaration=True, encoding='utf-8')
            f.write(xml)

        return custom_props_path

    def get_property_names(self):
        return []


class OOXMLContentTypes(Part):

    def __init__(self, workdir):
        self.workdir = workdir
        super(OOXMLContentTypes, self).__init__(
            os.path.join(self.workdir, CONTENT_TYPES_PATH))
        self.part_name = os.path.join('/', CUSTOM_PROPERTY_DEFAULT_PATH)

    def has_custom_props_content_type(self):
        xpath = '/c:Types/c:Override[@PartName="{}"]'.format(self.part_name)
        return len(self.tree.xpath(xpath, namespaces=NSMAP)) > 0

    def create_custom_props_content_types(self):
        if self.has_custom_props_content_type():
            return

        root = self.tree.getroot()
        new_relationship = etree.SubElement(root, '{%s}Override' %
                                            NAMESPACES['CONTENT_TYPES'])
        new_relationship.attrib['ContentType'] = CUSTOM_PROPERTY_CONTENT_TYPE
        new_relationship.attrib['PartName'] = self.part_name

        self.write_xml_file()


class OOXMLRelationships(Part):

    def __init__(self, workdir):
        self.workdir = workdir
        super(OOXMLRelationships, self).__init__(
            os.path.join(self.workdir, '_rels', '.rels'))

    @property
    def relationships(self):
        return self.tree.xpath(
            '/r:Relationships/r:Relationship',
            namespaces=NSMAP
        )

    def get_by_type(self, type):
        for rel in self.relationships:
            if rel.attrib['Type'] == type:
                return rel
        return None

    def get_custom_props_path(self):
        custom_props_rel = self.get_by_type(NAMESPACES['CUSTOM_PROPS_REL'])
        if custom_props_rel is None:
            return None
        target = custom_props_rel.attrib['Target']
        return os.path.join(self.workdir, target)

    def create_custom_props_relationship(self):
        assert self.get_by_type(NAMESPACES['CUSTOM_PROPS_REL']) is None

        max_rid = self.get_max_rid()
        new_rid = "rId{}".format(max_rid + 1)
        root = self.tree.getroot()

        new_relationship = etree.SubElement(root, '{%s}Relationship' %
                                            NAMESPACES['RELATIONSHIPS'])
        new_relationship.attrib['Type'] = NAMESPACES['CUSTOM_PROPS_REL']
        new_relationship.attrib['Id'] = new_rid
        new_relationship.attrib['Target'] = CUSTOM_PROPERTY_DEFAULT_PATH

        self.write_xml_file()

    def get_max_rid(self):
        return max(int(re.match('rId(\d+)', n.attrib['Id']).group(1))
                   for n in self.relationships)


class OOXMLDocument(OOXMLPackage):

    def __enter__(self):
        super(OOXMLDocument, self).__enter__()

        self.relationships = OOXMLRelationships(self.workdir)
        docprops_path = self.relationships.get_custom_props_path()
        if docprops_path is None:
            self.properties = EmptyPropertiesPart(self.workdir)
        else:
            self.properties = CustomPropertiesPart(docprops_path)
        return self

    def update_properties(self, metadata):
        assert not self._read_only, 'you may not update readonly documents!'
        self.properties = self.properties.update(metadata)


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
