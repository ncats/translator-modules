from unittest import TestCase

from BioLink.model import HGNC

from translator_modules.core.data_transfer_model import Result, Identifier

from .test_attribute import mock_attribute
from .test_identifier import mock_identifier

mock_result_input_id  = mock_identifier()
mock_result_output_id = mock_identifier()
mock_result_score = '0.00001'

def mock_result():
    """
        input_id:  str   # should be a CURIE
        output_id: str   # should be a CURIE
        score: str = ''
        attributes: List[Attribute] = field(default_factory=list)
    """
    r = Result(mock_result_input_id, mock_result_output_id, mock_result_score)
    a = mock_attribute()
    r.attributes.append(a)
    return r


class TestResult(TestCase):

    def test_result_to_json(self):
        r = mock_result()
        print("\n\nResult JSON output: \n", r.to_json())
