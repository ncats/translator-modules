from unittest import TestCase

from translator_modules.core.model import ResultList
from translator_modules.core.test_result import stub_result
from translator_modules.core.test_attribute import stub_attribute


def stub_result_list():

    r = stub_result()
    a = stub_attribute()

    rl = ResultList(
        'fake result list',
        source='ncats',
        # input_category='input biolink category',
        # output_category='output biolink category',
        relationship='biolink predicate relationship'
    )
    rl.attributes.append(a)
    rl.results.append(r)

    return rl


class TestResultList(TestCase):

    def test_result_list_to_json(self):

        rl = stub_result_list()

        print("\n\nResultList JSON output: \n", rl.to_json())
