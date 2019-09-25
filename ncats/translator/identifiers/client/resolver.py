#!/usr/bin/env python3

import csv
import json

from typing import Iterable, List
from ...core import handle_input_or_input_location

from ncats.translator.identifiers.server.resolver import Resolver as sr

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
        self.client  = sr.get_the_resolver()
        self.input_identifiers = None

    def list_identifier_keys(self) -> List[str]:
        return self.client.list_identifier_keys()

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


def main():
    fire.Fire(Resolver)


if __name__ == '__main__':
    main()
