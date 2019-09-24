# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.model.identifier_mapping import IdentifierMapping  # noqa: E501
from openapi_server.model.inline_response201 import InlineResponse201  # noqa: E501
from openapi_server.test import BaseTestCase


class TestPublicController(BaseTestCase):
    """PublicController integration test stubs"""

    def test_identifier_list(self):
        """Test case for identifier_list

        post a list of identifiers
        """
        request_body = ['request_body_example']
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/identifier_list',
            method='POST',
            headers=headers,
            data=json.dumps(request_body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_identifier_keys(self):
        """Test case for list_identifier_keys

        list of valid key strings for identifier sources and targets
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/list_identifier_keys',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_translate(self):
        """Test case for translate

        Translates list of identifiers from source to target namespace 
        """
        query_string = [('list_identifier', 'list_identifier_example'),
                        ('target_namespace', 'target_namespace_example')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/translate',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_translate_one(self):
        """Test case for translate_one

        translates one identifier source to target namespace
        """
        query_string = [('source_identifier', 'source_identifier_example'),
                        ('target_namespace', 'target_namespace_example')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/translate_one',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
