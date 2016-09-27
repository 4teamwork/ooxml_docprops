from datetime import datetime
from ooxml_docprops.properties import OOXMLDocument
from ooxml_docprops.tests.assets import TestAsset
from unittest2 import TestCase


class TestDocProperties(TestCase):

    def test_can_write_string_properties(self):
        with TestAsset('without_custom_properties.docx') as asset:
            with OOXMLDocument(asset.path) as doc:
                doc.update_properties({'hans': 'Peter'})
                self.assertEqual('Peter', doc.properties.get_property_value('hans'))

    def test_can_write_int_properties(self):
        with TestAsset('without_custom_properties.docx') as asset:
            with OOXMLDocument(asset.path) as doc:
                doc.update_properties({'zahl': 1})
                self.assertEqual(1, doc.properties.get_property_value('zahl'))

    def test_can_write_bool_properties(self):
        with TestAsset('without_custom_properties.docx') as asset:
            with OOXMLDocument(asset.path) as doc:
                doc.update_properties({'ischeswahr': True})
                self.assertEqual(True, doc.properties.get_property_value('ischeswahr'))

    def test_can_write_datetime_properties(self):
        dt = datetime.now()
        with TestAsset('without_custom_properties.docx') as asset:
            with OOXMLDocument(asset.path) as doc:
                doc.update_properties({'denn': dt})
                self.assertEqual(dt, doc.properties.get_property_value('denn'))
