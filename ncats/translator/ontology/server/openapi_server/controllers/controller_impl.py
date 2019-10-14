from uuid import uuid4

from ncats.translator.ontology.server.openapi_server.model.computation_identifier import ComputationIdentifier
from ncats.translator.ontology.server.openapi_server.model.computation_input import ComputationInput
from ncats.translator.ontology.server.openapi_server.model.results import Results
from ncats.translator.ontology.server.openapi_server import util

"""
Handler delegation functions to inject and connect into 
Jaccard Computation Service OpenAPI controller stubs:

from .controller_impl import (
    handle_compute_jaccard,
    handle_get_jaccard_results,
)
"""


def handle_compute_jaccard(computation_input: ComputationInput) -> ComputationIdentifier:
    """post a list of input genes and initiate a Jaccard similarity computation

    Post a list of input genes and initiate a Jaccard similarity computation  # noqa: E501

    :param computation_input: List of input genes upon which to compute Jaccard similarity
    :type computation_input: dict | bytes

    :rtype: ComputationIdentifier
    """
    if computation_input:

        uuid = str(uuid4())

        compute_id = ComputationIdentifier(uuid=uuid)

        return compute_id

    else:
        raise RuntimeError("handle_identifier_list() ERROR: Empty request body?")


def handle_get_jaccard_results(computation_id: str) -> Results:
    """Retrieves a list of similarity results when ready

    Retrieves a list of similarity results when obtained by a Jaccard similarity of a posted list of input genes  # noqa: E501

    :param computation_id: Computational Identifier UUID returned from a submitted Jaccard similarity computation request upon a posted list of input genes
    :type computation_id: str

    :rtype: Results
    """
    pass
