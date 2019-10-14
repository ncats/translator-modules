# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from ncats.translator.ontology.server.openapi_server.model.computation_identifier import \
    ComputationIdentifier  # noqa: E501
from ncats.translator.ontology.server.openapi_server.model.computation_input import ComputationInput  # noqa: E501
from ncats.translator.ontology.server.openapi_server.model.results import Results  # noqa: E501
from ncats.translator.ontology.server.openapi_server.test import BaseTestCase


class TestPublicController(BaseTestCase):
    """PublicController integration test stubs"""

    def test_compute_jaccard(self):
        """Test case for compute_jaccard

        post a list of input genes and initiate a Jaccard similarity computation
        """
        computation_input = {
            "input_genes": [{
                "sim_input_curie": "P38398",
                "input_symbol": "BRCA1",
                "input_id": "HGNC:1100"
            }, {
                "sim_input_curie": "P38398",
                "input_symbol": "BRCA1",
                "input_id": "HGNC:1100"
            }],
            "taxon": "human",
            "ontology": "ontology"
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
        self.assertStatus(response, 201,
                          'Response body is : ' + response.data.decode('utf-8'))

    def test_get_results(self):
        """Test case for get_results

        Retrieves a list of similarity results when ready 
        """
        query_string = [('computation_id', '123e4567-e89b-12d3-a456-426655440000')]
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
