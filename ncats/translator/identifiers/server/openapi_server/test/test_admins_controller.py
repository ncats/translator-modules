# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json

from ncats.translator.identifiers.server.openapi_server.test import BaseTestCase


class TestAdminsController(BaseTestCase):
    """AdminsController integration test stubs"""

    @unittest.skip("Admin interfaces not yet implemented")
    def test_load_identifier_map(self):
        """Test case for load_identifier_map

        Identifier Resolver map initial creation
        """
        identifier_map = {
  "records" : [ [ "HGNC:24086", "A1CF", "APOBEC1 complementation factor", "NM_014576", "ENSG00000148584", "29974" ], [ "HGNC:24086", "A1CF", "APOBEC1 complementation factor", "NM_014576", "ENSG00000148584", "29974" ] ],
  "keys" : [ "HGNC_ID", "Approved_Symbol", "Approved_Name", "Refseq_ID", "Ensembl_Gene_ID", "NCBI_Gene_ID" ],
  "map_identifier" : {
    "uuid" : "123e4567-e89b-12d3-a456-426655440000"
  }
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/identifier_map',
            method='POST',
            headers=headers,
            data=json.dumps(identifier_map),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    @unittest.skip("Admin interfaces not yet implemented")
    def test_update_identifier_map(self):
        """Test case for update_identifier_map

        Identifier Resolver map update
        """
        identifier_map = {
  "records" : [ [ "HGNC:24086", "A1CF", "APOBEC1 complementation factor", "NM_014576", "ENSG00000148584", "29974" ], [ "HGNC:24086", "A1CF", "APOBEC1 complementation factor", "NM_014576", "ENSG00000148584", "29974" ] ],
  "keys" : [ "HGNC_ID", "Approved_Symbol", "Approved_Name", "Refseq_ID", "Ensembl_Gene_ID", "NCBI_Gene_ID" ],
  "map_identifier" : {
    "uuid" : "123e4567-e89b-12d3-a456-426655440000"
  }
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/identifier_map',
            method='PUT',
            headers=headers,
            data=json.dumps(identifier_map),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
