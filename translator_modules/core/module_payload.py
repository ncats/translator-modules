import os.path
from abc import ABC
from urllib.parse import urlparse
from collections import defaultdict

import pandas as pd
import requests

from translator_modules.core.data_transfer_model import ResultList


def fix_curies(raw_list, prefix=''):
    """
    Adds a suitable XMLNS prefix to identifiers known to
    be "raw" IDs assumed to be in the leading item in a tuple
    :param id_list:
    :param prefix:
    :return:
    """
    curie_list = defaultdict(dict)
    for key in raw_list.keys():
        curie_list[prefix+':'+key] = raw_list[key]
    return curie_list


def get_input_gene_set(input_genes, extension) -> pd.DataFrame:

    if extension == "csv":
        input_gene_set = pd.read_csv(input_genes, orient='records')

    elif extension == "json":

        # assuming it's Pandas DataFrame compliant JSON and it's a record list
        input_gene_set = pd.read_json(input_genes, orient='records')

    elif extension == "ncats":

        # assuming it's NCATS ResultList compliant JSON
        input_result_list = ResultList.load(input_genes)

        # I coerce the ResultList internally into a Pandas DataFrame
        # Perhaps we'll remove this intermediate step sometime in the future
        input_gene_set = input_result_list.export_data_frame()

    elif extension is None:
        # TODO: this was written for the sharpener. maybe
        # more generic if we get Biolink Model adherence
        gene_ids = []
        symbols = []
        if isinstance(input_genes, str):
            # simple list of curies?
            input_genes = input_genes.split(',')
            for gene in input_genes:
                gene_ids.append(gene)
                symbols.append('') # symbol unknown for now?
        else: # assume iterable
            for gene in input_genes:
                symbol = None
                for attribute in gene.attributes:
                    if attribute.name == 'gene_symbol':
                        symbol = attribute.value
                if symbol is not None:
                    gene_ids.append(gene.gene_id)
                    symbols.append(symbol)
        genes = {"hit_id": gene_ids, "hit_symbol": symbols}
        input_gene_set = pd.DataFrame(data=genes)

    return input_gene_set


class Payload(ABC):

    def __init__(self, mod):
        """
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
        self.mod = mod
        self.results = None

    def handle_input_or_input_location(self, input_or_input_location):
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

        if not type(input_or_input_location) is str:
            extension = None
            return input_or_input_location, extension

        if type(input_or_input_location) is str and os.path.isfile(input_or_input_location):
            input_file = input_or_input_location
            extension = os.path.splitext(input_file)[1][1:]  # first char is a `.`
            with open(input_file) as stream:
                payload_input = stream.read()
                return payload_input, extension

        elif type(input_or_input_location) is str and _is_url(input_or_input_location):
            input_url = input_or_input_location
            path = urlparse(input_url).path
            extension = os.path.splitext(path)[1]
            response = requests.get(input_url)
            response.raise_for_status()  # exception handling
            payload_input = response.text
            return payload_input, extension

        else:
            """
            Raw input from command line processed directly?
            """
            extension = None
            return input_or_input_location, extension

    def get_data_frame(self) -> pd.DataFrame:
        return self.results

    def get_result_list(self) -> ResultList:
        """
        Alternate form of output: convert module Pandas DataFrame data into a
        NCATS Translator Module data transfer model Results in a ResultList instance.

        :return: ResultList
        """
        return ResultList.import_data_frame(self.results, self.mod)
