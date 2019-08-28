from unittest import TestCase

from BioLink.model import MONDO

from translator_modules.core.data_transfer_model import Identifier

mock_identifier_xmlns = MONDO
mock_identifier_object_id = '1'


def stub_identifier():
    return Identifier(mock_identifier_xmlns, mock_identifier_object_id)

class TestIdentifier(TestCase):

    def test_identifier_creation(self):

        i = stub_identifier()

        self.assertEqual(i.xmlns, mock_identifier_xmlns, 'Identifier xmlns set')
        self.assertEqual(i.object_id, mock_identifier_object_id, 'Identifier object_id set')

    def test_identifier_to_json(self):
        i = stub_identifier()
        print("\n\nIdentifier JSON output: \n", i.to_json())

    def test_curie(self):
        i = stub_identifier()

        self.assertEqual(i.curie(), "Namespace:1", "Identifier CURIE is properly constructed")