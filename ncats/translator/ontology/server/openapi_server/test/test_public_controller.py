# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from ncats.translator.ontology.server.openapi_server.test import BaseTestCase


class TestPublicController(BaseTestCase):
    """PublicController integration test stubs"""

    def test_compute_jaccard(self):
        """Test case for compute_jaccard

        post a list of input genes and initiate a Jaccard similarity computation
        """
        computation_input = {
            "input_genes": [{
                "sim_input_curie": "UniProtKB:Q8NB91",
                "input_symbol": "FANCB",
                "input_id": "HGNC:3583"
            }],
            "taxon": "human",
            "ontology": "go",
            "lower_bound": 0.05
        }
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/compute_jaccard',
            method='POST',
            headers=headers,
            data=json.dumps(computation_input),
            content_type='application/json')

        response_body = response.data.decode('utf-8')

        self.assertStatus(response, 201, 'Response body is : ' + response_body)

        # convert response body string to a  proper Python object
        response_body = json.loads(response_body)

    # Merging the two tests since a proper test of
    # 'get_results' requires a valid compute_jaccard endpoint call
    # @unittest.skip("Need to validate core jaccard_similarity test first?")
    # def test_get_results(self):
        """Test case for get_results

        Retrieves a list of similarity results when ready 
        """
        query_string = [('computation_id', response_body['uuid'])]

        headers = {
            'Accept': 'application/json',
        }
        
        response = self.client.open(
            '/results',
            method='GET',
            headers=headers,
            query_string=query_string)

        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
