from unittest import TestCase

from io.ncats.translator.core.data_transfer_model import Attribute

mock_attribute_name = 'some attribute name'
mock_value = 'some attribute value'
mock_source = 'ncats'


def mock_attribute():
    return Attribute(mock_attribute_name, mock_value, mock_source)


class TestAttribute(TestCase):

    def test_attribute_creation(self):

        name = 'some attribute name'
        value = 'some attribute value'

        a = Attribute(name, value)

        self.assertEqual(a.name, name, 'Attribute name set')
        self.assertEqual(a.value, value, 'Attribute value set')
        self.assertEqual(a.source, '', 'Attribute source is empty by default')

        a = mock_attribute()
        self.assertEqual(a.source, 'ncats', 'Optional Attribute source field is set to ncats')

    def test_attribute_to_json(self):
        a = mock_attribute()
        print("\n\nAttribute JSON output: \n", a.to_json())
