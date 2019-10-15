from uuid import uuid4

from typing import Dict, Tuple, Any

from ncats.translator.ontology.server.openapi_server.exceptions import OntologyServerException
from ncats.translator.ontology.server.openapi_server.model.computation_identifier import ComputationIdentifier
from ncats.translator.ontology.server.openapi_server.model.computation_input import ComputationInput
from ncats.translator.ontology.server.openapi_server.model.results import Results
from ncats.translator.ontology.server.openapi_server import util

from ncats.translator.ontology.server.ontology import GenericSimilarity

"""
Handler delegation functions to inject and connect into 
Jaccard Computation Service OpenAPI controller stubs:

from .controller_impl import (
    handle_compute_jaccard,
    handle_get_jaccard_results,
)
"""
_ontology = {}

_result_cache = {}


def handle_compute_jaccard(computation_input: ComputationInput) -> Tuple[ComputationIdentifier, int]:
    """post a list of input genes and initiate a Jaccard similarity computation

    Post a list of input genes and initiate a Jaccard similarity computation  # noqa: E501

    :param computation_input: List of input genes upon which to compute Jaccard similarity
    :type computation_input: dict | bytes

    :rtype: ComputationIdentifier
    """
    if computation_input:

        # Initiate a Jaccard Similarity computation here

        ontology = computation_input.ontology
        if ontology not in ['go', 'hp', 'mp']:
            raise OntologyServerException("compute_jaccard() ERROR: ontology '"+ontology+"' not recognized.")

        taxon = computation_input.taxon
        if taxon not in ['human', 'mouse']:
            raise OntologyServerException("compute_jaccard() ERROR: taxon '"+taxon+"' not recognized.")

        input_genes = computation_input.input_genes
        if not input_genes:
            raise OntologyServerException("compute_jaccard() ERROR: invalid or empty input_genes set.")

        lower_bound = computation_input.lower_bound
        if not lower_bound:
            lower_bound = 0.7

        if ontology not in _ontology:
            _ontology[ontology] = {}

        if taxon not in _ontology[ontology]:
            _ontology[ontology][taxon] = GenericSimilarity(ontology, taxon)

        similarity_engine = _ontology[ontology][taxon]

        uuid = str(uuid4())

        _result_cache[uuid] = similarity_engine.compute_jaccard_async(input_genes, lower_bound)

        compute_id = ComputationIdentifier(uuid=uuid)

        return compute_id, 201

    else:
        raise RuntimeError("handle_identifier_list() ERROR: Empty request body?")


def handle_get_jaccard_results(computation_id: str) -> Tuple[Any,int]:
    """Retrieves a list of similarity results when ready

    Retrieves a list of similarity results when obtained by a Jaccard similarity of a posted list of input genes  # noqa: E501

    :param computation_id: Computational Identifier UUID returned from a submitted Jaccard similarity computation request upon a posted list of input genes
    :type computation_id: str

    :rtype: Results
    """
    if computation_id in _result_cache:
        result_future = _result_cache[computation_id]
        if result_future:
            # Need to check if the result is ready to return then return it
            return Results()
        else:
            return "The requested computation processing without error, but results are not yet available.", 102
    else:
        return "Not found", 404
