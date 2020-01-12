# coding: utf-8

"""
    OpenAPI for NCATS Biomedical Translator Reasoners

    OpenAPI for NCATS Biomedical Translator Reasoners  # noqa: E501

    The version of the OpenAPI document: 0.9.2
    Contact: edeutsch@systemsbiology.org
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import ara_client
from ara_client.api.query_api import QueryApi  # noqa: E501
from ara_client.rest import ApiException


class TestQueryApi(unittest.TestCase):
    """QueryApi unit test stubs"""

    def setUp(self):
        self.api = ara_client.api.query_api.QueryApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_query(self):
        """Test case for query

        Query reasoner via one of several inputs  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
