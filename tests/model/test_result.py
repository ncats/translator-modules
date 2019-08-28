from unittest import TestCase

from BioLink.model import HGNC

from translator_modules.core.data_transfer_model import Result, Identifier

from .test_attribute import stub_attribute
from .test_identifier import stub_identifier


def stub_result():

    i = stub_identifier()
    a = stub_attribute()

    r = Result(Identifier(HGNC, "1234"), score='100')
    r.identifiers.append(i)
    r.attributes.append(a)

    return r

class TestResult(TestCase):

    def test_result_to_json(self):
        r = stub_result()
        print("\n\nResult JSON output: \n", r.to_json())
