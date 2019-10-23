# Shared core similarity functions

from typing import List
import os
from time import sleep
import logging

import pandas as pd

from ncats.translator.ontology.client.openapi_client.api.public_api import PublicApi
from ncats.translator.ontology.client.openapi_client.configuration import Configuration
from ncats.translator.ontology.client.openapi_client.api_client import ApiClient
from ncats.translator.ontology.client.openapi_client.exceptions import ApiException

from ncats.translator.ontology.client.openapi_client.model.computation_input import ComputationInput
from ncats.translator.ontology.client.openapi_client.model.computation_identifier import ComputationIdentifier
from ncats.translator.ontology.client.openapi_client.model.gene_entry import GeneEntry
from ncats.translator.ontology.client.openapi_client.model.results import Results


class GenericSimilarity(object):

    def __init__(self) -> None:
        self.ont = ''
        self.taxon = ''

        configuration = Configuration()

        # Defining host is optional and defaults to http://0.0.0.0:8082
        configuration.host = os.getenv('JACCARD_SIMILARITY_SERVER_HOST', 'http://0.0.0.0:8082')

        # Create an instance of the API class
        self.client = PublicApi(ApiClient(configuration))

    def compute_jaccard(self, input_genes: List[dict], lower_bound: float = 0.7) -> List[dict]:

        computation_input = ComputationInput(
            ontology=self.ont,
            taxon=self.taxon,
            lower_bound=lower_bound,
            input_genes=[
                GeneEntry(
                    input_id=entry['input_id'],
                    sim_input_curie=entry['sim_input_curie'],
                    input_symbol=entry['input_symbol']
                ) for entry in input_genes
            ]
        )

        computation_id: ComputationIdentifier
        try:
            # post a list of input genes and initiate a Jaccard similarity computation
            computation_id = self.client.compute_jaccard(computation_input=computation_input)
        except ApiException as e:
            logging.error("Exception when calling Jaccard Similarity PublicApi->compute_jaccard: %s\n" % e)
            return []

        results: Results
        status_code: str
        while True:

            try:
                # attempt to retrieve the results
                results, status_code, headers = self.client.get_results_with_http_info(computation_id.uuid)
            except ApiException as e:
                logging.error("Exception when calling Jaccard Similarity PublicApi->get_results: %s\n" % e)
                return []

            if status_code is 201:
                # wait a short while then check again for a result
                logging.debug("Jaccard Similarity PublicApi->get_results() http code 201: still processing?")
                sleep(1.0)
                continue
            else:
                break

        if status_code is not 200:
            logging.error("Jaccard Similarity server get_results() call HTTP error code: "+status_code)
            return []

        """
        # Single similarity entry
        'input_id': 'str',
        'input_symbol': 'str',
        'hit_symbol': 'str',
        'hit_id': 'str',
        'score': 'float',
        'shared_terms': 'list[str]',
        'shared_term_names': 'list[str]' 
        """
        similarities = [similarity.to_dict() for similarity in results.similarities]
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
