from unittest import TestCase

from BioLink.model import Disease, Gene, GeneToDiseaseAssociation, PhenotypicFeature

from tests.model.test_concept import mock_concept
from tests.model.test_identifier import mock_identifier_2
from translator_modules.core.data_transfer_model import ResultList, ConceptSpace
from .test_attribute import mock_attribute
from .test_result import mock_result

_r = mock_result()
_a = mock_attribute()

mock_predicate = "has_phenotype"


def default_mock_result_list():

    rl = ResultList()
    rl.attributes.append(_a)
    rl.concepts.append(mock_concept())
    rl.concepts.append(mock_concept(identifier=mock_identifier_2()))
    rl.results.append(_r)

    return rl


def overridden_mock_result_list(
        association=GeneToDiseaseAssociation.class_name,
        domain=ConceptSpace(
            category=Disease.class_name,
            mappings=['MONDO']
        ),
        relationship='related_to',
        range=ConceptSpace(
            category=Gene.class_name,
            mappings=['HGNC']
        )
):

    rl = ResultList(
        source='ncats',
        association=association,
        domain=domain,
        relationship=relationship,
        range=range
    )
    rl.attributes.append(_a)
    rl.concepts.append(mock_concept())
    rl.concepts.append(mock_concept(identifier=mock_identifier_2()))
    rl.results.append(_r)

    return rl


_json_test_file = "result_list_test.json"

_mock_uberon_concept_space = ConceptSpace(
    category=Disease.class_name,
    mappings=['UBERON']
)

_mock_upheno_concept_space = ConceptSpace(
    category=PhenotypicFeature.class_name,
    mappings=['UPHENO']
)

_mock_hgnc_concept_space = ConceptSpace(
    category=Gene.class_name,
    mappings=['HGNC']
)

_mock_mondo_concept_space = ConceptSpace(
    category=Disease.class_name,
    mappings=['MONDO']
)


class TestResultList(TestCase):

    def test_default_result_list_to_json(self):
        rl = default_mock_result_list()
        print("\n\nDefault ResultList JSON output: \n", rl.to_json())

    def test_overridden_result_list_to_json(self):
        rl = overridden_mock_result_list()
        print("\n\nOverridden ResultList JSON output: \n", rl.to_json())

    def test_customized_result_list_to_json(self):
        rl = overridden_mock_result_list(
            domain=_mock_uberon_concept_space,
            relationship=mock_predicate,
            range=_mock_upheno_concept_space
        )
        self.assertEqual(rl.relationship, mock_predicate, "Set relationship to predicate")
        print("\n\nOverridden ResultList JSON output with changed parameters: \n", rl.to_json())

    def test_defective_result_list_creation(self):
        print("\nTest creation of ResultList with missing Domain value:")
        try:
            rl = overridden_mock_result_list(
                domain=None,
                relationship=mock_predicate,
                range=_mock_upheno_concept_space
            )
            print("\nI should not see this JSON output: \n", rl.to_json())
        except RuntimeError as re:
            print("\nPASSED: Proper ResultList exception thrown for missing Domain value\n", re)

        print("\nTest creation of ResultList with a Domain value which is not a ConceptSpace:")
        try:
            rl = overridden_mock_result_list(
                domain="Not a ConceptSpace!",
                relationship=mock_predicate,
                range=_mock_upheno_concept_space
            )
            print("\nI should not see this JSON output: \n", rl.to_json())
        except RuntimeError as re:
            print("\nPASSED: Proper ResultList exception thrown for incorrect Domain data type\n", re)

        print("\nTest creation of ResultList with missing Range value:")
        try:
            rl = overridden_mock_result_list(
                domain=_mock_uberon_concept_space,
                relationship=mock_predicate,
                range=None
            )
            print("\nI should not see this JSON output: \n", rl.to_json())
        except RuntimeError as re:
            print("\nPASSED! Proper ResultList exception thrown for missing Range value\n", re)

        print("\nTest creation of ResultList with invalid Range value:")
        try:
            rl = overridden_mock_result_list(
                domain=_mock_uberon_concept_space,
                relationship=mock_predicate,
                range="Not a ConceptSpace!"
            )
            print("\nI should not see this JSON output: \n", rl.to_json())
        except RuntimeError as re:
            print("\nPASSED! Proper ResultList exception thrown for incorrect Range data type\n", re)

    def test_result_list_json_loading(self):
        rl_out = overridden_mock_result_list(
            domain=_mock_hgnc_concept_space,
            relationship=mock_predicate,
            range=_mock_mondo_concept_space
        )
        rl_json = rl_out.to_json()
        rl_in = ResultList.load(rl_json)
        print("\n\nReloaded ResultList JSON: \n", rl_in.to_json())

        print("\n\nDataFrame conversion?\n")
        df = rl_in.export_data_frame()
        print("\n"+df.to_json())
