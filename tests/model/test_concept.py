from unittest import TestCase

from core.data_transfer_model import Concept
from .test_attribute import mock_attribute
from .test_identifier import mock_identifier, mock_identifier_xmlns, mock_identifier_object_id


def mock_concept(identifier=mock_identifier()):
    a = mock_attribute()
    c = Concept(identifier)
    c.identifiers.append(identifier)
    c.attributes.append(a)
    return c


class TestConcept(TestCase):

    def test_concept_creation(self):

        c = mock_concept()

        self.assertEqual(c.primary_id.xmlns,     mock_identifier_xmlns, 'Concept primary_id xmlns set')
        self.assertEqual(c.primary_id.object_id, mock_identifier_object_id, 'Concept primary_id object_id set')

    def test_concept_to_json(self):
        c = mock_concept()
        print("\n\nConcept JSON output: \n", c.to_json())
