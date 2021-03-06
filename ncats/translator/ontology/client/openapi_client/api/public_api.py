# coding: utf-8

"""
    NCATS Translator Modules Ontology Jaccard Similarity Server

    NCATS Translator Modules Ontology Jaccard Similarity Server  # noqa: E501

    The version of the OpenAPI document: 0.0.1
    Contact: richard@starinformatics.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from ncats.translator.ontology.client.openapi_client.api_client import ApiClient
from ncats.translator.ontology.client.openapi_client.exceptions import (
    ApiTypeError,
    ApiValueError
)


class PublicApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def compute_jaccard(self, **kwargs):  # noqa: E501
        """post a list of input genes and initiate a Jaccard similarity computation  # noqa: E501

        Post a list of input genes and initiate a Jaccard similarity computation   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.compute_jaccard(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param ComputationInput computation_input: List of input genes upon which to compute Jaccard similarity 
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ComputationIdentifier
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.compute_jaccard_with_http_info(**kwargs)  # noqa: E501

    def compute_jaccard_with_http_info(self, **kwargs):  # noqa: E501
        """post a list of input genes and initiate a Jaccard similarity computation  # noqa: E501

        Post a list of input genes and initiate a Jaccard similarity computation   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.compute_jaccard_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param ComputationInput computation_input: List of input genes upon which to compute Jaccard similarity 
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(ComputationIdentifier, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['computation_input']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method compute_jaccard" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'computation_input' in local_var_params:
            body_params = local_var_params['computation_input']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/compute_jaccard', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ComputationIdentifier',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_results(self, computation_id, **kwargs):  # noqa: E501
        """Retrieves a list of similarity results when ready   # noqa: E501

        Retrieves a list of similarity results when obtained by a Jaccard similarity of a posted list of input genes   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_results(computation_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str computation_id: Computational Identifier UUID returned from a submitted Jaccard similarity computation request upon a posted list of input genes  (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Results
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.get_results_with_http_info(computation_id, **kwargs)  # noqa: E501

    def get_results_with_http_info(self, computation_id, **kwargs):  # noqa: E501
        """Retrieves a list of similarity results when ready   # noqa: E501

        Retrieves a list of similarity results when obtained by a Jaccard similarity of a posted list of input genes   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_results_with_http_info(computation_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str computation_id: Computational Identifier UUID returned from a submitted Jaccard similarity computation request upon a posted list of input genes  (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Results, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['computation_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_results" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'computation_id' is set
        if ('computation_id' not in local_var_params or
                local_var_params['computation_id'] is None):
            raise ApiValueError("Missing the required parameter `computation_id` when calling `get_results`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'computation_id' in local_var_params:
            query_params.append(('computation_id', local_var_params['computation_id']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/results', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Results',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
