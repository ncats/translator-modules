#!/usr/bin/env python

import os
import csv
import json
import logging

from typing import Iterable, List, Dict
from ncats.translator.core import handle_input_or_input_location

from ncats.translator.identifiers import SYMBOL
from ncats.translator.identifiers.client.openapi_client.api.public_api import PublicApi
from ncats.translator.identifiers.client.openapi_client.configuration import Configuration
from ncats.translator.identifiers.client.openapi_client.api_client import ApiClient
from ncats.translator.identifiers.client.openapi_client.exceptions import ApiException

from ncats.translator.identifiers.client.openapi_client.model.identifier_mapping import IdentifierMapping

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
        The optional environment variable IDENTIFIERS_RESOLUTION_SERVER_HOST may be set
        to point the client to another server location. This can be used, for example,
        within Dockerfiles to point to an internal microservice container running the resolver.
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

        Returns list of valid key strings for source and target parameters in other Resolver calls
        :return: list[str]
        """
        identifier_keys: list[str]
        try:
            identifier_keys = self.client.list_identifier_keys()
        except ApiException as e:
            logging.error("Exception when calling Identifiers Resolution PublicApi->list_identifier_keys: %s\n" % e)
            return []

        return identifier_keys

    def load_identifiers(self, identifiers, source=None):
        """
        Load a list of source identifiers for subsequent translation
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        :param identifiers: csv, tab-delimited text, json, or direct iterable collection of identifiers to translate
        :param str source: (optional) string key for field in the 'identifiers'  )
        :return: self (resolver primed with a list of identifiers for translation)
        """

        if DEBUG:
            print("load identifiers")

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

    def directly_load_identifiers(self, identifiers):
        self.input_identifiers = [entry for entry in identifiers]

    def _read_identifiers_in_flatfile(self, identifiers, delimiter=',', source=None):
        if DEBUG:
            print("identifiers.client._read_identifiers_in_flatfile()")

        if not source:
            raise RuntimeError("Resolver._read_identifiers_in_flatfile ERROR: json file 'source' tag unspecified?")

        with open(identifiers) as id_file:
            input_reader = csv.DictReader(id_file, delimiter=delimiter)
            self.input_identifiers = [row[source] for row in input_reader]

    def translate_one(self, source_identifier, target_namespace) -> Dict:
        """
        Returns mapping of identifier source to its equivalent identifier in the specified target namespace

        :param str source_identifier: single source identifier to be mapped onto the target  (required)
        :param str target_namespace: target namespace for the mapping of the source  (required)

        :return: Python object with {'source_identifier': str, 'target_namespace': str, 'target_identifier': str}
        """
        identifier_mapping: IdentifierMapping
        status_code: str
        try:
            identifier_mapping, status_code, headers = \
                self.client.translate_one_with_http_info(source_identifier, target_namespace)

        except ApiException as e:

            logging.error(
                "Exception when calling Identifiers Resolution PublicApi->translate_one(" +
                "source_identifier:" + source_identifier + ", " +
                "target_namespace:" + target_namespace +
                "): %s\n" % e)

            # error code returned
            status_code = 500

        if status_code is not 200:

            logging.error("Identifiers Resolution server translate_one((" +
                          "source_identifier:" + source_identifier + ", " +
                          "target_namespace:" + target_namespace +
                          ") call HTTP error code: " + status_code)

            # return empty object
            identifier_mapping = \
                IdentifierMapping(
                    source_identifier=source_identifier,
                    target_namespace=target_namespace
                )

        return identifier_mapping.to_dict()

    def translate(self, target_namespace=None) -> List[Dict]:
        """
        Translates a list of identifiers previously loaded into the Resolver from source namespace to a specified target
        :param str target_namespace: Target namespace for mapping of source identifiers  (required)
        :return: list of {'source_identifier': str, 'target_namespace': str, 'target_identifier': str}
        """
        if not (self.input_identifiers and isinstance(self.input_identifiers, list)):
            logging.error("Exception when calling Identifiers Resolution translate: empty input_identifiers list?")
            return []

        identifier_list_id: IdentifierListId
        status_code: str
        try:
            identifier_list_id, status_code, headers = \
                self.client.identifier_list_with_http_info(request_body=self.input_identifiers)

        except ApiException as e:
            logging.error("Exception when calling Identifiers Resolution PublicApi->identifier_list: %s\n" % e)
            status_code = 500

        if status_code is 201:
            identifier_list_id.list_identifier
            # identifiers successfully posted for translation? then, retrieve  the result

            similarities: list[str]
            try:
                similarities, status_code, headers = \
                    self.client.translate_with_http_info(list_identifier="", target_namespace=target_namespace)

            except ApiException as e:
                logging.error("Exception when calling Identifiers Resolution PublicApi->translate: %s\n" % e)
                status_code = 500

        if status_code is not 200:
            logging.error("Identifiers Resolution server translate((" +
                          "target_namespace:" + target_namespace +
                          ") call HTTP error code: " + status_code)
            return []

        return [entry.to_dict() for entry in similarities]


def gene_symbol(identifier, symbol):
    """
    Retrieve the symbol associated with an input identifier, looking it up if empty
    :param identifier:
    :param symbol:
    :return:
    """
    if symbol:
        return symbol
    else:
        translation = \
            Resolver.get_the_resolver().translate_one(
                source_identifier=identifier,
                target_namespace=SYMBOL
            )
        return translation['target_identifier']


def main():
    fire.Fire(Resolver)


if __name__ == '__main__':
    main()
