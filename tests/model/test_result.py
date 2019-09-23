from unittest import TestCase

from tests.model.test_identifier \
    import mock_identifier_xmlns, mock_identifier_object_id, mock_identifier_version, \
    mock_identifier_xmlns_2, mock_identifier_object_id_2, mock_identifier_version_2

from io.ncats.translator.core.data_transfer_model import Result
from .test_attribute import mock_attribute

mock_result_input_id = mock_identifier_xmlns+":"+mock_identifier_object_id+'.'+mock_identifier_version
mock_result_output_id = mock_identifier_xmlns_2+":"+mock_identifier_object_id_2+'.'+mock_identifier_version_2
mock_result_score = '0.00001'


def mock_result(
        input_id=mock_result_input_id,
        output_id=mock_result_output_id
):
    """
        input_id:  str   # should be a CURIE
        output_id: str   # should be a CURIE
        score: str = ''
        attributes: List[Attribute] = field(default_factory=list)
    """
    r = Result(input_id, output_id, mock_result_score)
    a = mock_attribute()
    r.attributes.append(a)
    return r


class TestResult(TestCase):

    def test_result_to_json(self):
        r = mock_result()
        print("\n\nResult JSON output: \n", r.to_json())
