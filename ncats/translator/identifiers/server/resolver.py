#!/usr/bin/env python3

import os
import csv
import json

import fire
from typing import Iterable, List

from ncats.translator.identifiers import IdentifierResolverException

from ...core import handle_input_or_input_location

DEBUG = False

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
_the_identifier_map = os.path.abspath(dir_path+'/HUGO_geneids_download_v2.txt')


class Resolver:
    """
    This class handles identifier conversions. Note that, for now, the 'identifier_map' catalog and the 'input_ids'
    need to have matching identifier formatting, in particular, with respect to xmlns (curie) prefixes.
    """
    _the_resolver = None

    @classmethod
    def get_the_resolver(cls):
        if not cls._the_resolver:
            cls._the_resolver = Resolver(_the_identifier_map)
        return cls._the_resolver

    def __init__(self, identifier_map):
        if DEBUG:
            print("__init__")
        """
        Constructor of a Resolver map object for identifier translation across namespaces.
        :param identifier_map: csv, tab-delimited text, json, direct list or a string source of identifier mappings
        """

        if not identifier_map:
            raise IdentifierResolverException(
                "Resolver() ERROR: 'identifier_map' unspecified - don't know what to translate?"
            )

        identifier_map_str, extension = handle_input_or_input_location(identifier_map)

        self.identifier_records: list
        self.full_identifier_dict: dict
        # NB: push this out to the handle_input_or_input_location function?
        if extension == "csv":
            self._read_identifier_map_in_flatfile(identifier_map)

        elif extension == "txt":  # CX: tabbed, correct input
            self._read_identifier_map_in_flatfile(identifier_map, delimiter='\t')

        elif extension == "json":

            with open(identifier_map) as identifier_map_file:
                input_json = json.loads(identifier_map_file)
                # assume records format
                # self.result_map = [(record[domain], record[range]) for record in input_json]

        elif extension is None:

            # Not yet sure how to interpret a single string identifier map?
            if type(identifier_map) is str:
                raise IdentifierResolverException(
                    "Resolver() ERROR: unrecognized 'identifier_map' specification: "+identifier_map+"?"
                )
                # self.identifier_map = identifier_map_str

            elif type(identifier_map) is Iterable:
                # Could be a list of tuples or a dictionary?
                # Not sure if this is correct here... need some test cases
                self.identifier_records = [entry for entry in identifier_map]

            else:
                raise IdentifierResolverException("Resolver() ERROR: unrecognized 'identifier_map' specification?")

        self.input_identifiers: List[str] = list()

    def list_identifier_keys(self) -> List[str]:
        return list(self.identifier_map.keys())

    def _read_identifier_map_in_flatfile(self, identifier_map, delimiter='\t'):
        if DEBUG:
            print("_read_identifier_map_in_flatfile")
        with open(identifier_map) as identifier_map_file:
            input_reader = csv.DictReader(identifier_map_file, delimiter=delimiter)
            headers = list(next(input_reader))
            # print("Headers:\t"+', '.join(headers))
            self.identifier_records = [tuple(map(lambda header: row[header], headers)) for row in input_reader]

            self.identifier_map = {}
            for h in range(0, len(headers)):
                self.identifier_map[headers[h]] = []
                for i in range(0, len(self.identifier_records)):
                    self.identifier_map[headers[h]].append(self.identifier_records[i][h])

    def translate_one(self, source, target):
        """
        Lookup translation of a single input identifier in the (previously loaded) identifier map
        :param source: identifier to be translated
        :param target: target namespace key from which identifier is to be obtained
        :return: mapping of input onto target namespace (empty string if no mapping available)
        """
        if DEBUG:
            print("translate_one")

        if not target:
            raise IdentifierResolverException("Resolver.translate_one() ERROR: json file 'target' tag unspecified?")

        # find index of source
        for index, idr in enumerate(self.identifier_records):
            if source in idr:
                target = self.identifier_map[target][index]
                return source, target
        return source, ""

    def translate(self, target=None):
        """
        Translate an iterable input list of identifiers previously loaded (using load_identifiers)
        :param target:
        :return: tuple mappings of input source identifiers onto target namespace
        """
        if DEBUG:
            print("translate")

        if not target:
            raise IdentifierResolverException("Resolver.translate ERROR: json file 'target' tag unspecified?")

        # The second entry of the tuple will be an empty string ''
        # if output/converted_id isn't found in identifier_map dict
        translated_ids = [self.translate_one(input_id, target) for input_id in self.input_identifiers]

        return translated_ids

    ########################################################
    # The following functions are  kept  here only in case
    # that this module is directly invoked as a command line
    # or CWL module.
    ########################################################
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

        if extension == "csv":
            self._read_identifiers_in_flatfile(identifiers, source=source)

        elif extension == "txt":
            self._read_identifiers_in_flatfile(identifiers, delimiter='\t', source=source)

        elif extension == "json":

            if not source:
                raise IdentifierResolverException(
                    "Resolver.load_identifiers ERROR: json file 'domain' tag unspecified?"
                )

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
            raise IdentifierResolverException(
                "Resolver._read_identifiers_in_flatfile ERROR: json file 'source' tag unspecified?"
            )

        with open(identifiers) as id_file:
            input_reader = csv.DictReader(id_file, delimiter=delimiter)
            self.input_identifiers = [row[source] for row in input_reader]


def main():
    fire.Fire(Resolver)


if __name__ == '__main__':
    main()
