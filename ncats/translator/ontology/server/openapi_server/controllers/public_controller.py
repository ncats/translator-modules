import connexion
import six

from openapi_server.model.computation_identifier import ComputationIdentifier  # noqa: E501
from openapi_server.model.computation_input import ComputationInput  # noqa: E501
from openapi_server.model.results import Results  # noqa: E501
from openapi_server import util

from .controller_impl import (
    handle_compute_jaccard,
    handle_get_jaccard_results,
)

def compute_jaccard(computation_input=None):  # noqa: E501
    """post a list of input genes and initiate a Jaccard similarity computation

    Post a list of input genes and initiate a Jaccard similarity computation  # noqa: E501

    :param computation_input: List of input genes upon which to compute Jaccard similarity 
    :type computation_input: dict | bytes

    :rtype: ComputationIdentifier
    """
    if connexion.request.is_json:
        computation_input = ComputationInput.from_dict(connexion.request.get_json())  # noqa: E501
    return handle_compute_jaccard(computation_input)


def get_results(computation_id):  # noqa: E501
    """Retrieves a list of similarity results when ready 

    Retrieves a list of similarity results when obtained by a Jaccard similarity of a posted list of input genes  # noqa: E501

    :param computation_id: Computational Identifier UUID returned from a submitted Jaccard similarity computation request upon a posted list of input genes 
    :type computation_id: str

    :rtype: Results
    """
    return handle_get_jaccard_results(computation_id)
