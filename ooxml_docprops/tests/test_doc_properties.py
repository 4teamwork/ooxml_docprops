from ooxml_docprops.properties import OOXMLDocument
from ooxml_docprops.tests.assets import TestAsset
from unittest2 import TestCase


class TestDocProperties(TestCase):

    def test_documents_without_properties_can_be_processed(self):
        with TestAsset('without_custom_properties.docx') as asset:
            with OOXMLDocument(asset.path) as doc:
                self.assertItemsEqual([], doc.properties.get_property_names())

    def test_properties_can_be_added_to_documents_without_properties(self):
        with TestAsset('without_custom_properties.docx') as asset:
            with OOXMLDocument(asset.path) as doc:
                self.assertListEqual([], doc.properties.get_property_names())

                doc.update_properties({'Hans': 'Peter'})

                self.assertItemsEqual(['Hans'],
                                      doc.properties.get_property_names())

    def test_properties_can_be_added_to_documents_with_properties(self):
        with TestAsset('with_custom_properties.docx') as asset:
            with OOXMLDocument(asset.path) as doc:
                self.assertListEqual(['Test'],
                                     doc.properties.get_property_names())

                doc.update_properties({'Hans': 'Peter'})

                self.assertItemsEqual(['Hans', 'Test'],
                                      doc.properties.get_property_names())

    def test_properties_can_be_updated_for_documents_with_properties(self):
        with TestAsset('with_custom_properties.docx') as asset:
            with OOXMLDocument(asset.path) as doc:
                self.assertEqual('Peter',
                                 doc.properties.get_property_value('Test'))

                doc.update_properties({'Test': 'Hanspeter'})

                self.assertEqual('Hanspeter',
                                 doc.properties.get_property_value('Test'))
