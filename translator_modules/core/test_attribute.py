from unittest import TestCase

from .model import Attribute


class TestAttribute(TestCase):

    def test_attribute_creation(self):
        name = 'some attribute name'
        value = 'some attribute value'

        a = Attribute(name, value)

        self.assertEqual(a.name, name, 'Attribute name set')
        self.assertEqual(a.value, value, 'Attribute value set')
        self.assertEqual(a.source, '', 'Attribute source is empty by default')

        a = Attribute(name, value, 'ncats')
        self.assertEqual(a.source, 'ncats', 'Optional Attribute source field is set to ncats')

    def test_attribute_to_json(self):

        name = 'tag'
        value = 'value'
        source = 'ncats'

        a = Attribute(name, value,source)

        print("\n\nAttribute JSON output: \n", a.to_json())
