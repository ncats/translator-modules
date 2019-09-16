import os.path
from io import StringIO

import json
from pprint import pprint

from abc import ABC
from urllib.parse import urlparse
from collections import defaultdict

import pandas as pd
import requests
from typing import List, Iterable

from translator_modules.core.data_transfer_model import ModuleMetaData, ResultList


def fix_curies(object_id, prefix=''):
    """
    Adds a suitable XMLNS prefix to (an) identifier(s) known to
    be "raw" IDs as keys in a dictionary or elements in a list (or a simple string)
    :param object_id:
    :param prefix:
    :return:
    """
    if not prefix:
        raise RuntimeWarning('fix_curies(): empty prefix argument?')

    if isinstance(object_id, dict):
        curie_dict = defaultdict(dict)
        for key in object_id.keys():
            curie_dict[prefix + ':' + key] = object_id[key]
        return curie_dict

    elif isinstance(object_id, str):
        # single string to convert
        return prefix + ':' + object_id

    elif isinstance(object_id, Iterable):
        return [prefix + ':' + x for x in object_id]

    else:
        raise RuntimeError("fix_curie() is not sure how to fix an instance of data type '", type(object_id))


class Payload(ABC):

    def __init__(self, module, metadata: ModuleMetaData):
        """
        TODO: TO REVIEW THIS PAYLOAD COMMENT - MAYBE OBSOLETE (AS OF SEPTEMBER 15, 2019)
        Conventions for Payloads?
        - They expect CSV/TSV files or JSON files in 'record' form (a list of dictionaries that name-index tuples of data)
        - Their internal representation of these datatypes
        - If the internal representation needs to be transformed into something usable by one of its methods, it is the
            responsibility of the method to do the data conversion. For example, if we need to iterate over records, the dictionary
            conversion is done inside the method.
            - This is tenable as a design principle due to the first convention causing us to expect DataFrames by default, but
            we shouldn't know what the method is going to require and do the conversion, **as that leaks out information
            about the method into a higher layer of the code.**

        """
        self.module = module
        self.metadata: ModuleMetaData = metadata
        self.results = None

    def metadata(self):
        # metadata is now a complex DataClass...
        # not sure if or how  this will print properly?
        pprint(self.metadata)

    @staticmethod
    def handle_input_or_input_location(input_or_input_location):
        """
        Figures out whether the input being opened is from a remote source or on the file-system;
        then returns the value of the input once it is extracted.
        """

        # https://stackoverflow.com/a/52455972
        def _is_url(url):
            try:
                result = urlparse(url)
                return all([result.scheme, result.netloc])
            except ValueError:
                return False
            except AttributeError:
                return False

        if not input_or_input_location:
            raise RuntimeError("Payload.handle_input_or_input_location(): Null or empty 'input_or_input_location'?")

        if not type(input_or_input_location) is str:
            extension = None
            return input_or_input_location, extension

        else:
            if _is_url(input_or_input_location):
                input_url = input_or_input_location
                path = urlparse(input_url).path
                extension = os.path.splitext(path)[1]
                response = requests.get(input_url)
                response.raise_for_status()  # exception handling
                payload_input = response.text

                # not sure if a CSV file will be properly read in..
                return payload_input, extension

            else:
                if os.path.isabs(input_or_input_location):
                    input_file = input_or_input_location
                else:
                    input_file = os.path.abspath(input_or_input_location)

                if os.path.isfile(input_file):
                    extension = os.path.splitext(input_file)[1][1:]  # first char is a `.`
                    with open(input_file) as stream:
                        payload_input = stream.read()
                    return payload_input, extension
                else:
                    """
                    Raw input from command line processed directly?
                    """
                    extension = None
                    return input_or_input_location, extension

    def get_input_data_frame(self, input_spec) -> pd.DataFrame:

        input_obj, extension = self.handle_input_or_input_location(input_spec)

        if extension == "csv":
            input_data_frame = pd.read_csv(StringIO(input_obj))
            # , encoding='utf8', sep=" ", index_col="id", dtype={"switch": np.int8})

        elif extension == "json":

            # Load the json text document into a Python Object
            input_genes_obj = json.loads(input_obj)

            # check if the json object input has a
            # characteristic high level ResultList key (i.e. 'result_list_name')
            if 'result_list_name' in input_genes_obj:
                # assuming it's NCATS ResultList compliant JSON
                input_result_list = ResultList.load(input_genes_obj)

                # I coerce the ResultList internally into a Pandas DataFrame
                # Perhaps we'll remove this intermediate step sometime in the future
                input_data_frame = input_result_list.export_data_frame()
            else:
                # Assume that it's Pandas DataFrame compliant JSON
                input_data_frame = pd.DataFrame(input_genes_obj)

        elif extension is None:
            # TODO: this was written for the sharpener. maybe
            # more generic if we get Biolink Model adherence
            input_ids = []
            input_symbols = []
            if isinstance(input_obj, str):
                # simple list of curies?
                input_obj = input_obj.split(',')
                for entry in input_obj:
                    input_ids.append(entry)
                    input_symbols.append('')  # symbol unknown for now?
            elif isinstance(input_obj, tuple):
                # another simple list of curies?
                for entry in input_obj:
                    input_ids.append(entry)
                    input_symbols.append('')  # symbol unknown for now?
            else:  # assume iterable
                #  This piece of code assumes inputs compliant with the
                #  Translator Indigo Gene Sharpener Gene List data model
                for entry in input_obj:
                    symbol = None
                    for attribute in entry.attributes:
                        if attribute.name == 'gene_symbol':
                            symbol = attribute.value
                    if symbol is not None:
                        input_ids.append(entry.gene_id)
                        input_symbols.append(symbol)

            input_data = {"hit_id": input_ids, "hit_symbol": input_symbols}
            input_data_frame = pd.DataFrame(data=input_data)
        else:
            raise RuntimeWarning("Unrecognized data file extension: '" + extension + "'?")

        return input_data_frame

    def get_simple_input_identifier_list(self, input_spec) -> List[str]:
        """
        This function returns a simple list of identifiers rather than a Pandas DataFrame

        :param input_spec:
        :return: simple flat  List[str] of input identifiers
        """
        input_data_frame = self.get_input_data_frame(input_spec)
        simple_identifier_list = [hit_id for hit_id in input_data_frame['hit_id']]
        return simple_identifier_list

    def get_data_frame(self) -> pd.DataFrame:
        return self.results

    def get_result_list(self) -> ResultList:
        """
        Alternate form of output: convert module Pandas DataFrame data into a
        NCATS Translator Module data transfer model Results in a ResultList instance.

        :return: ResultList
        """
        return ResultList.import_data_frame(self.results, self.metadata)
