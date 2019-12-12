from io import StringIO

import json
from pprint import pprint

from abc import ABC

import pandas as pd
from typing import List

from . import handle_input_or_input_location
from .data_transfer_model import ModuleMetaData, ResultList

from ncats.translator.identifiers import object_id
from ncats.translator.core.identifiers_resolver import gene_symbol


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
    def get_input_data_frame(input_spec) -> pd.DataFrame:

        input_obj, extension = handle_input_or_input_location(input_spec)

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
            elif isinstance(input_obj, list) or isinstance(input_obj, tuple):
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

        # Probably a good place to check if the "hit_symbol" is present;
        # If not, attempt to use the Identifiers Resolution service to add them in
        input_ids = []
        input_symbols  =  []
        for gene in input_data_frame.to_dict(orient='records'):
            gene['hit_symbol'] = gene_symbol(gene['hit_id'], gene['hit_symbol'])
            input_ids.append(gene['hit_id'])
            input_symbols.append(gene['hit_symbol'])

        input_data = {"hit_id": input_ids, "hit_symbol": input_symbols}
        input_data_frame = pd.DataFrame(data=input_data)

        return input_data_frame

    def get_simple_input_identifier_list(self, input_spec, object_id_only=False) -> List[str]:
        """
        This function returns a simple list of identifiers rather than a Pandas DataFrame

        :param input_spec:
        :param object_id_only:
        :return: list[str] simple list of identifiers from the DataFrame
        """
        input_data_frame = self.get_input_data_frame(input_spec)
        simple_identifier_list = [object_id(hit_id) if object_id_only else hit_id for hit_id in input_data_frame['hit_id']]
        return sorted(simple_identifier_list, key=object_id)

    def get_data_frame(self) -> pd.DataFrame:
        return self.results

    def get_result_list(self) -> ResultList:
        """
        Alternate form of output: convert module Pandas DataFrame data into a
        NCATS Translator Module data transfer model Results in a ResultList instance.

        :return: ResultList
        """
        return ResultList.import_data_frame(self.results, self.metadata)
