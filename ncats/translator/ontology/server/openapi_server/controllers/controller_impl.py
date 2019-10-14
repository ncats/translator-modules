
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
    pass


def handle_get_jaccard_results(computation_id: str) -> Results:
    pass
