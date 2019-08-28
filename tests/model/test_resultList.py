from unittest import TestCase

from BioLink.model import Disease, Gene, GeneToDiseaseAssociation, PhenotypicFeature

from tests.model.test_concept import mock_concept
from translator_modules.core.data_transfer_model import ResultList, ConceptSpace

from .test_attribute import mock_attribute
from .test_result import mock_result

r = mock_result()
a = mock_attribute()


def default_mock_result_list():

    rl = ResultList('default mock result list')
    rl.attributes.append(a)
    rl.concepts.append(mock_concept())
    rl.results.append(r)

    return rl


def overridden_mock_result_list(
        domain=ConceptSpace('MONDO', Disease.class_name),
        relationship=GeneToDiseaseAssociation.class_name,
        range=ConceptSpace('HGNC', Gene.class_name)
):

    rl = ResultList(
        'overridden mock result list',
        source='ncats',
        domain=domain,
        relationship=relationship,
        range=range
    )
    rl.attributes.append(a)
    rl.concepts.append(mock_concept())
    rl.results.append(r)

    return rl


class TestResultList(TestCase):

    mock_predicate = "has_phenotype"

    def test_result_list_to_json(self):

        rl = default_mock_result_list()

        print("\n\nDefault ResultList JSON output: \n", rl.to_json())

        rl = overridden_mock_result_list()

        print("\n\nOverridden ResultList JSON output: \n", rl.to_json())

        rl = overridden_mock_result_list(
            domain=ConceptSpace('UBERON',Disease.class_name),
            relationship=TestResultList.mock_predicate,
            range=ConceptSpace('UPHENO', PhenotypicFeature.class_name)
        )

        self.assertEqual(rl.relationship, TestResultList.mock_predicate, "Set relationship to predicate")
        print("\n\nOverridden ResultList JSON output with changed parameters: \n", rl.to_json())
