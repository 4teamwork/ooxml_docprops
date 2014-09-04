from ooxml_docprops.properties import OOXMLDocument
from ooxml_docprops.tests.assets import TestAsset
from unittest2 import TestCase


class TestDocProperties(TestCase):

    def test_has_any_property_with_properties(self):
        with TestAsset('with_custom_properties.docx') as asset:
            with OOXMLDocument(asset.path) as doc:
                doc.update_properties({'Hans': 'Peter'})

                self.assertTrue(doc.has_any_property(['Hans']))
                self.assertTrue(doc.has_any_property(['Hans', 'Foo']))
                self.assertFalse(doc.has_any_property(['Bar', 'Foo']))
                self.assertFalse(doc.has_any_property([]))

    def test_has_any_property_without_properties(self):
        with TestAsset('without_custom_properties.docx') as asset:
            with OOXMLDocument(asset.path) as doc:
                self.assertListEqual([], doc.properties.get_property_names())

                self.assertFalse(doc.has_any_property(['Hans']))
                self.assertFalse(doc.has_any_property(['Hans', 'Foo']))
                self.assertFalse(doc.has_any_property([]))
