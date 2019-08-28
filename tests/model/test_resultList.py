from unittest import TestCase

from BioLink.model import Disease, Gene, GeneToDiseaseAssociation, BiologicalEntity, PhenotypicFeature

from translator_modules.core.data_transfer_model import ResultList
from .test_result import stub_result
from .test_attribute import stub_attribute

r = stub_result()
a = stub_attribute()


def default_mock_result_list():

    rl = ResultList(
        'fake result list',
        source='ncats'
    )
    rl.attributes.append(a)
    rl.results.append(r)

    return rl


def overridden_mock_result_list(
        input_category=Disease.class_name,
        output_category=Gene.class_name,
        relationship=GeneToDiseaseAssociation.class_name
):

    rl = ResultList(
        'fake result list',
        source='ncats',
        input_category=input_category,
        output_category=output_category,
        relationship=relationship
    )
    rl.attributes.append(a)
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
            input_category=BiologicalEntity.class_name,
            output_category=PhenotypicFeature.class_name,
            relationship=TestResultList.mock_predicate
        )

        self.assertEqual(rl.relationship, TestResultList.mock_predicate, "Set relationship to predicate")
        print("\n\nOverridden ResultList JSON output with changed parameters: \n", rl.to_json())
