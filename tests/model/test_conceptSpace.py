from unittest import TestCase

from BioLink.model import Gene

from translator_modules.core.data_transfer_model import ConceptSpace

mock_concept_space_mappings = 'HGNC'
mock_concept_space_category = Gene.class_name


def mock_concept_space():
    cs = ConceptSpace(
        category=mock_concept_space_category,
        mappings=[mock_concept_space_mappings]
    )
    return cs


class TestConceptSpace(TestCase):

    def test_concept_space_creation(self):

        cs = mock_concept_space()

        self.assertEqual(cs.mappings[0], mock_concept_space_mappings, 'ConceptSpace mappings set')
        self.assertEqual(cs.category,  mock_concept_space_category,  'ConceptSpace category set')

    def test_concept_space_to_json(self):
        cs = mock_concept_space()
        print("\n\nConceptSpace JSON output: \n", cs.to_json())
