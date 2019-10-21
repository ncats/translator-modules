# Shared core similarity functions

from typing import List, Tuple

import pandas as pd

from ncats.translator.ontology.client.openapi_client.api.public_api import PublicApi
from ncats.translator.ontology.client.openapi_client.configuration import Configuration
from ncats.translator.ontology.client.openapi_client.api_client import ApiClient
from ncats.translator.ontology.client.openapi_client.model.computation_input import ComputationInput
from ncats.translator.ontology.client.openapi_client.model.computation_identifier import ComputationIdentifier
from ncats.translator.ontology.client.openapi_client.exceptions import ApiException


class GenericSimilarity(object):

    def __init__(self) -> None:
        self.ont = ''
        self.taxon = ''

        configuration = Configuration()

        # Defining host is optional and defaults to http://0.0.0.0:8082
        configuration.host = "http://0.0.0.0:8082"

        # Create an instance of the API class
        self.client = PublicApi(ApiClient(configuration))

    def compute_jaccard(self, input_genes: List[dict], lower_bound: float = 0.7) -> List[dict]:

        computation_input = ComputationInput(
            ontology=self.ont,
            taxon=self.taxon,
            lower_bound=lower_bound,
            input_genes=""
        )

        computation_id: ComputationIdentifier
        try:
            # post a list of input genes and initiate a Jaccard similarity computation
            computation_id = self.client.compute_jaccard(computation_input=computation_input)
        except ApiException as e:
            print("Exception when calling PublicApi->compute_jaccard: %s\n" % e)
            return []

        try:
            # attempt to retrieve the results
            computation_id = self.client.get_results(computation_id.uuid)
            computation_id
        except ApiException as e:
            print("Exception when calling PublicApi->get_results: %s\n" % e)
            return []

        similarities = []

        return similarities

    @staticmethod
    def sort_results(results) -> pd.DataFrame:

        results = pd.DataFrame(results)

        if not results.empty:
            # CX: Some users need to know the scores that input genes have for each other.
            #     replacing code to remove GeneA input = GeneA output results
            results = \
                results[~(results.hit_id == results.input_id)]. \
                sort_values('score', ascending=False)

        return results
