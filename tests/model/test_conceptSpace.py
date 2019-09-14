from unittest import TestCase

from BioLink.model import Gene

from translator_modules.core.data_transfer_model import ConceptSpace

mock_concept_space_id_prefixes = 'HGNC'
mock_concept_space_category = Gene.class_name


def mock_concept_space():
    cs = ConceptSpace(
        category=mock_concept_space_category,
        id_prefixes=[mock_concept_space_id_prefixes]
    )
    return cs


class TestConceptSpace(TestCase):

    def test_concept_space_creation(self):

        cs = mock_concept_space()

        self.assertEqual(cs.id_prefixes[0], mock_concept_space_id_prefixes, 'ConceptSpace id_prefixes set')
        self.assertEqual(cs.category,  mock_concept_space_category,  'ConceptSpace category set')

    def test_concept_space_to_json(self):
        cs = mock_concept_space()
        print("\n\nConceptSpace JSON output: \n", cs.to_json())
