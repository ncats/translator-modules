#!/usr/bin/env python3

import csv
import json

import fire
from typing import Iterable
from translator_modules.core import handle_input_or_input_location

DEBUG = False

GENE = 'gene'
DISEASE = 'disease'
CHEMICAL_SUBSTANCE = 'chemical substance'

SYMBOL = 'approved symbol'


class Resolver:
    """
    This class handles identifier conversions. Note that, for now, the 'identifier_map' catalog and the 'input_ids'
    need to have matching identifier formatting, in particular, with respect to xmlns (curie) prefixes.
    """

    _the_resolver = None
    _the_identifier_map ='./HUGO_geneids_download_v2.txt'

    @classmethod
    def get_the_resolver(cls):
        if not cls._the_resolver:
            cls._the_resolver = Resolver(cls._the_identifier_map)
        return cls._the_resolver

    def handle_input_or_input_location(self, identifier_map):
        return handle_input_or_input_location(identifier_map)

    def __init__(self, identifier_map):
        if DEBUG: print("__init__")
        """
        Constructor of a Resolver map object for identifier translation across namespaces.
        :param identifier_map: csv, tab-delimited text, json, direct list or a string source of identifier mappings
        :param source: for record based inputs, the target 'source' namespace field or tag
        :param target: for record based inputs, the target 'source' namespace field or tag
        """

        if not identifier_map:
            raise RuntimeError("Resolver() ERROR: 'identifier_map' unspecified - don't know what to translate?")

        identifier_map_str, extension = self.handle_input_or_input_location(identifier_map)

        if extension in ["csv",  "txt", "json"]:
            if not self.domain:
                raise RuntimeError("Resolver() ERROR: identifier map file 'source' namespace unspecified "+
                                   "but is mandatory for csv, txt or json mapping file loading")
            elif not self.range:
                raise RuntimeError("Resolver() ERROR: identifier map file 'target' namespace unspecified "+
                                   "but is mandatory for csv, txt or json mapping file loading")

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
                raise RuntimeError("Resolver() ERROR: unrecognized 'identifier_map' specification?")
                # self.identifier_map = identifier_map_str

            elif type(identifier_map) is Iterable:
                # Could be a list of tuples or a dictionary?
                # Not sure if this is correct here... need some test cases
                self.identifier_records = [entry for entry in identifier_map]

            else:
                raise RuntimeError("Resolver() ERROR: unrecognized 'identifier_map' specification?")

        self.input_identifiers = None


    def _read_identifier_map_in_flatfile(self, identifier_map, delimiter='\t'):
        if DEBUG: print("_read_identifier_map_in_flatfile")
        with open(identifier_map) as identifier_map_file:
            input_reader = csv.DictReader(identifier_map_file, delimiter=delimiter)
            headers = list(next(input_reader))
            print("Headers:\t"+', '.join(self.headers))
            self.identifier_records = [tuple(map(lambda header: row[header], headers)) for row in input_reader]

            self.identifier_map = {}
            for h in range(0, len(headers)):
                self.identifier_map[headers[h]] = []
                for i in range(0, len(self.identifier_records)):
                    self.identifier_map[headers[h]].append(self.identifier_records[i][h])

    def load_identifiers(self, identifiers):
        if DEBUG: print("load identifiers")
        """
        Load a file of identifiers into
        :param identifiers: csv, tab-delimited text, json, or direct iterable collection of identifiers to translate \
        note that the 'source' field should match that previously provided to the Resolver constructor
        :return:
        """
        input_str, extension = self.handle_input_or_input_location(identifiers)

        self.input_identifiers: list
        # NB: push this out to the handle_input_or_input_location function?

        if extension in ["csv",  "txt", "json"]:
            if not self.domain:
                raise RuntimeError("Resolver() ERROR: identifier map file 'source' namespace unspecified "+
                                   "but is mandatory for csv, txt or json mapping file loading")
        if extension == "csv":
            self._read_identifiers_in_flatfile(identifiers)

        elif extension == "txt":
            self._read_identifiers_in_flatfile(identifiers, delimiter='\t')

        elif extension == "json":

            if not self.domain:
                raise RuntimeError("Resolver().load_identifiers ERROR: json file 'source' tag unspecified?")

            with open(identifiers) as id_file:
                input_json = json.loads(id_file)
                # assume records format
                self.input_identifiers = [record[self.domain] for record in input_json]

        elif extension is None:
            if type(identifiers) is Iterable:
                self.input_identifiers = [entry for entry in identifiers]

        return self

    def _read_identifiers_in_flatfile(self, identifiers, delimiter=','):
        if DEBUG: print("_read_identifiers_in_flatfile")
        with open(identifiers) as id_file:
            input_reader = csv.DictReader(id_file, delimiter=delimiter)
            self.input_identifiers = [row[self.domain] for row in input_reader]

    def translate_one(self, source, identifier_range):
        """
        Lookup translation of a single input identifier in the (previously loaded) identifier map
        :param source: identifier to be translated
        :param identifier_range: target namespace from which identifier is to be obtained
        :return: mapping of input onto target namespace (empty string if no mapping available)
        """
        if DEBUG:
            print("translate_one")
        # find index of source
        target = ''
        for index, idr in enumerate(self.identifier_records):
            if source in idr:
                target = self.identifier_map[identifier_range][index]
                return source, target
        return source, ""

    def translate(self):
        if DEBUG:
            print("translate")
        """
        Translate an iterable input list of identifiers.
        :param input_ids: iterable; If not specified, use a list previously loaded (using load_identifiers)
        :return: tuple mappings of input source identifiers onto target namespace
        """
        # The second entry of the tuple will be an empty string ''
        # if output/converted_id isn't found in identifier_map dict
        translated_ids = [self.translate_one(input_id, self.range) for input_id in self.input_identifiers]

        return translated_ids

if __name__ == '__main__':
    fire.Fire(Resolver)
