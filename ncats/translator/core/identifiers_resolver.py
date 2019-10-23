#!/usr/bin/env python

import os
import csv
import json
import logging

from typing import Iterable, List
from ncats.translator.core import handle_input_or_input_location

from ncats.translator.identifiers import SYMBOL
from ncats.translator.identifiers.client.openapi_client.api.public_api import PublicApi
from ncats.translator.identifiers.client.openapi_client.configuration import Configuration
from ncats.translator.identifiers.client.openapi_client.api_client import ApiClient
from ncats.translator.identifiers.client.openapi_client.exceptions import ApiException

import fire

DEBUG = False


class Resolver:
    """
    This class handles identifier conversions. Note that, for now, the 'identifier_map' catalog and the 'input_ids'
    need to have matching identifier formatting, in particular, with respect to xmlns (curie) prefixes.
    """
    _the_resolver = None

    @classmethod
    def get_the_resolver(cls):
        if not cls._the_resolver:
            cls._the_resolver = Resolver()
        return cls._the_resolver

    def __init__(self):
        """
        This is a constructor to connect a client to an actual server Resolver
        """
        # proxy directly to server class, for now
        self.input_identifiers = None

        configuration = Configuration()

        # Defining host is optional and defaults to http://0.0.0.0:8081
        configuration.host = os.getenv('IDENTIFIERS_RESOLUTION_SERVER_HOST', 'http://0.0.0.0:8081')

        # Create an instance of the API class
        self.client = PublicApi(ApiClient(configuration))

    def list_identifier_keys(self) -> List[str]:
        """list of valid key strings for identifier sources and targets  # noqa: E501

        Returns list of valid key strings for source and target parameters in other API calls   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_identifier_keys(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: list[str]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        identifier_keys: list[str]
        try:
            identifier_keys = self.client.self.client.list_identifier_keys()
        except ApiException as e:
            logging.error("Exception when calling Jaccard Similarity PublicApi->compute_jaccard: %s\n" % e)
            return []

        return identifier_keys

    def load_identifiers(self, identifiers, source=None):

        if DEBUG:
            print("load identifiers")
        """
        Load a file of identifiers into
        :param identifiers: csv, tab-delimited text, json, or direct iterable collection of identifiers to translate \
        note that the 'source' field should match that previously provided to the Resolver constructor
        :return:
        """
        input_str, extension = handle_input_or_input_location(identifiers)

        self.input_identifiers: list
        # NB: push this out to the handle_input_or_input_location function?

        if extension == "csv":
            self._read_identifiers_in_flatfile(identifiers, source=source)

        elif extension == "txt":
            self._read_identifiers_in_flatfile(identifiers, delimiter='\t', source=source)

        elif extension == "json":

            if not source:
                raise RuntimeError("Resolver.load_identifiers ERROR: json file 'domain' tag unspecified?")

            with open(identifiers) as id_file:
                input_json = json.loads(id_file)
                # assume records format
                self.input_identifiers = [record[source] for record in input_json]

        elif extension is None:
            if type(identifiers) is Iterable:
                self.input_identifiers = [entry for entry in identifiers]

        return self

    def _read_identifiers_in_flatfile(self, identifiers, delimiter=',', source=None):
        if DEBUG:
            print("identifiers.client._read_identifiers_in_flatfile()")

        if not source:
            raise RuntimeError("Resolver._read_identifiers_in_flatfile ERROR: json file 'source' tag unspecified?")

        with open(identifiers) as id_file:
            input_reader = csv.DictReader(id_file, delimiter=delimiter)
            self.input_identifiers = [row[source] for row in input_reader]

    def translate_one(self, source, target):
        return self.client.translate_one(source, target)

    def translate(self, target=None):
        self.client.input_identifiers = self.input_identifiers
        return self.client.translate(target)


def gene_symbol(identifier, symbol):
    if not symbol:
        identifier, symbol = Resolver.get_the_resolver().translate_one(source=identifier, target=SYMBOL)
    return symbol


def main():
    fire.Fire(Resolver)


if __name__ == '__main__':
    main()
