from unittest import TestCase

from .model import Identifier


class TestIdentifier(TestCase):

    def test_identifier_creation(self):

        xmlns = 'Namespace'
        object_id = '1'

        i = Identifier(xmlns, object_id)

        self.assertEqual(i.xmlns, xmlns, 'Identifier xmlns set')
        self.assertEqual(i.object_id, object_id, 'Identifier object_id set')

    def test_identifier_to_json(self):
        xmlns = 'Namespace'
        object_id = '1'

        i = Identifier(xmlns, object_id)

        print("\n\nIdentifier JSON output: \n", i.to_json())

    def test_curie(self):

        xmlns = 'Namespace'
        object_id = '1'

        i = Identifier(xmlns, object_id)

        self.assertEqual(i.curie(), "Namespace:1", "Identifier CURIE properly constructed")