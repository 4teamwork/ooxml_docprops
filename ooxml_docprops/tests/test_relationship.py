from ooxml_docprops import config
from ooxml_docprops.properties import OOXMLDocument
from ooxml_docprops.tests.assets import TestAsset
from os.path import exists
from os.path import join
from unittest2 import TestCase


class TestRelationships(TestCase):

    def test_get_max_rid(self):
        with TestAsset('without_custom_properties.docx') as asset:
            with OOXMLDocument(asset.path) as doc:
                relationships = doc.relationships
                self.assertEqual(4, relationships.get_max_rid())

    def test_get_max_rid_after_custom_props_creation(self):
        with TestAsset('without_custom_properties.docx') as asset:
            with OOXMLDocument(asset.path) as doc:
                self.assertEqual(4, doc.relationships.get_max_rid())

                doc.relationships.create_custom_props_relationship()

                self.assertEqual(5, doc.relationships.get_max_rid())

    def test_create_custom_props_relationship(self):
        with TestAsset('without_custom_properties.docx') as asset:
            with OOXMLDocument(asset.path) as doc:

                custom_props_path = join(
                    doc.workdir, config.CUSTOM_PROPERTY_DEFAULT_PATH
                )
                self.assertFalse(exists(custom_props_path))

                relationships = doc.relationships
                relationships.create_custom_props_relationship()

                self.assertTrue(exists(custom_props_path))
