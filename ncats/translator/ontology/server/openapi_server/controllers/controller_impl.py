import asyncio
from asyncio import CancelledError, InvalidStateError
from uuid import uuid4

from typing import Dict, Tuple, Any

from ncats.translator.ontology.server.openapi_server.exceptions import (
    OntologyServerException,
    JaccardSimilarityPending,
    JaccardSimilarityResultNotFound,
    JaccardSimilarityComputationError
)

from ncats.translator.ontology.server.openapi_server.model.computation_identifier import ComputationIdentifier
from ncats.translator.ontology.server.openapi_server.model.computation_input import ComputationInput
from ncats.translator.ontology.server.openapi_server.model.results import Results
from ncats.translator.ontology.server.openapi_server import util

from ncats.translator.ontology.server.ontology import GenericSimilarity
from openapi_server.model import Similarity

"""
Handler delegation functions to inject and connect into 
Jaccard Computation Service OpenAPI controller stubs:

from .controller_impl import (
    handle_compute_jaccard,
    handle_get_jaccard_results,
)
"""


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

        taxon = computation_input.taxon

        input_genes = computation_input.input_genes
        if not input_genes:
            raise OntologyServerException("compute_jaccard() ERROR: invalid or empty input_genes set.")

        lower_bound = computation_input.lower_bound
        if not lower_bound:
            lower_bound = 0.7

        uuid = str(uuid4())

        similarity_engine = GenericSimilarity.get_similarity_engine(ontology, taxon)

        similarity_engine.compute_jaccard_async(input_genes, lower_bound)

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
    try:
        """
        # Similarity result data is returned in 
        an array of dictionary objects with the following keys:

        'input_id'
        'input_symbol'
        'hit_symbol'
        'hit_id'
        'score'
        'shared_terms'
        'shared_term_names'
        """

        result = GenericSimilarity.get_jaccard_similarity_result(computation_id)

        #  wrap the computation identifier again to echo it
        computation_id = ComputationIdentifier(computation_id)

        similarities = [
            Similarity(
                input_id=entry['input_id'],
                input_symbol=entry['input_symbol'],
                hit_symbol=entry['hit_symbol'],
                hit_id=entry['hit_id'],
                score=entry['score'],
                shared_terms=[x for x in entry['shared_terms']],
                shared_term_names=[x for x in entry['shared_term_names']]
            ) for entry in result
        ]

        results = Results(
            computation_id=computation_id,
            similarities=similarities
        )

        return results, 200

    except JaccardSimilarityPending:
        return "The requested computation processing without error, but results are not yet available.", 102

    except JaccardSimilarityResultNotFound:
        return "Computation cancelled or not found - no result available", 404

    except JaccardSimilarityComputationError:
        return "Invalid computation state", 500

