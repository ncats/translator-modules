#!/usr/bin/env python3

import csv
import json

import fire
from typing import Iterable

from translator_modules.core.module_payload import Payload


class Resolver(Payload):
    """
    This class handles identifier conversions. Note that, for now, the 'identifier_map' catalog and the 'input_ids'
    need to have matching identifier formatting, in particular, with respect to xmlns (curie) prefixes.
    """

    def _read_identifier_map_in_flatfile(self, identifier_map, delimiter=','):
        with open(identifier_map) as identifier_map_file:
            input_reader = csv.DictReader(identifier_map_file, delimiter)
            headers = input_reader.fieldnames
            print("Headers:\t"+','.join(headers))
            self.identifier_map = list([(row[self.source], row[self.target]) for row in input_reader])

    def __init__(self, identifier_map, source, target):
        """
        Constructor of a Resolver map object for identifier translation across namespaces.
        :param identifier_map: csv, tab-delimited text, json, direct list or a string source of identifier mappings
        :param source: for record based inputs, the target 'source' namespace field or tag
        :param target: for record based inputs, the target 'source' namespace field or tag
        """
        super(Resolver, self).__init__(None)

        if not identifier_map:
            raise RuntimeError("Resolver() ERROR: 'identifier_map' unspecified - don't know what to translate?")

        self.source = source
        self.target = target
        self.ids = None

        identifier_map_str, extension = self.handle_input_or_input_location(identifier_map)

        if extension in ["csv",  "txt", "json"]:
            if not self.source:
                raise RuntimeError("Resolver() ERROR: identifier map file 'source' namespace unspecified "+
                                   "but is mandatory for csv, txt or json mapping file loading")
            elif not self.target:
                raise RuntimeError("Resolver() ERROR: identifier map file 'target' namespace unspecified "+
                                   "but is mandatory for csv, txt or json mapping file loading")

        self.identifier_map: list
        # NB: push this out to the handle_input_or_input_location function?
        if extension == "csv":
            self._read_identifier_map_in_flatfile(identifier_map)

        elif extension == "txt":  # CX: tabbed, correct input
            self._read_identifier_map_in_flatfile(identifier_map, delimiter='\t')

        elif extension == "json":

            with open(identifier_map) as identifier_map_file:
                input_json = json.loads(identifier_map_file)
                # assume records format
                self.identifier_map = [(record[source], record[target]) for record in input_json]

        elif extension is None:

            # Not yet sure how to interpret a single string identifier map?
            if type(identifier_map) is str:
                raise RuntimeError("Resolver() ERROR: unrecognized 'identifier_map' specification?")
                # self.identifier_map = identifier_map_str

            elif type(identifier_map) is Iterable:
                # Could be a list of tuples or a dictionary?
                # Not sure if this is correct here... need some test cases
                self.identifier_map = [entry for entry in identifier_map]

            else:
                raise RuntimeError("Resolver() ERROR: unrecognized 'identifier_map' specification?")

    def load_identifiers(self, identifiers):
        """
        Load a file of identifiers into
        :param identifiers: csv, tab-delimited text, json, or direct iterable collection of identifiers to translate \
        note that the 'source' field should match that previously provided to the Resolver constructor
        :return:
        """
        input_str, extension = self.handle_input_or_input_location(identifiers)

        self.ids: list
        # NB: push this out to the handle_input_or_input_location function?

        if extension in ["csv",  "txt", "json"]:
            if not self.source:
                raise RuntimeError("Resolver() ERROR: identifier map file 'source' namespace unspecified "+
                                   "but is mandatory for csv, txt or json mapping file loading")
        if extension == "csv":
            self._read_identifiers_in_flatfile(identifiers)

        elif extension == "txt":
            self._read_identifiers_in_flatfile(identifiers, delimiter='\t')

        elif extension == "json":

            if not self.source:
                raise RuntimeError("Resolver().load_identifiers ERROR: json file 'source' tag unspecified?")

            with open(identifiers) as id_file:
                input_json = json.loads(id_file)
                # assume records format
                self.ids = [record[self.source] for record in input_json]

        elif extension is None:
            if type(identifiers) is Iterable:
                self.ids = [entry for entry in identifiers]

        return self

    def translate_one(self, input_id):
        """
        Lookup translation of a single input identifier in the (previously loaded) identifier map
        :param input_id:
        :return: mapping of input onto target namespace (empty string if no mapping available)
        """
        return input_id, self.identifier_map.get(input_id, '')

    def translate(self):
        """
        Translate an iterable input list of identifiers.
        :param input_ids: iterable; If not specified, use a list previously loaded (using load_identifiers)
        :return: tuple mappings of input source identifiers to target namespace
        """
        # The second entry of the tuple will be an empty string ''
        # if output/converted_id isn't found in identifier_map dict
        translated_ids = [self.translate_one(input_id) for input_id in self.ids]

        return translated_ids

    def _read_identifiers_in_flatfile(self, identifiers, delimiter=','):
        with open(identifiers) as id_file:
            input_reader = csv.DictReader(id_file, delimiter)
            self.ids = list([row[self.source] for row in input_reader])

if __name__ == '__main__':
    fire.Fire(Resolver)
