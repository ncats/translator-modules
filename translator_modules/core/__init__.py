import os.path
from urllib.parse import urlparse
from collections import defaultdict
import requests
from typing import List, Iterable
import pandas as pd
import json
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
        # return object_id - invoker may already consider it a curie?
        return object_id

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


def object_id(curie) -> str:
    """
    Returns the object_id of a curie
    :param curie:
    :return:
    """
    if not curie:
        return curie
    part = curie.split(':')
    return part[:-1]

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
        raise RuntimeError("handle_input_or_input_location(): Null or empty 'input_or_input_location'?")

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

def get_simple_input_gene_list(input_genes, extension) -> List[str]:
    """
    This function returns a simple list of genes identifiers rather than a Pandas DataFrame
    :param input_genes:
    :param extension:
    :return: List[str] of input gene identifiers
    """
    input_gene_data_frame = get_input_gene_data_frame(input_genes, extension)
    simple_gene_list = [hit_id for hit_id in input_gene_data_frame['hit_id']]
    return simple_gene_list


def get_input_gene_data_frame(input_genes, extension) -> pd.DataFrame:

    if extension == "csv":
        input_gene_data_frame = pd.read_csv(input_genes, orient='records')

    elif extension == "json":

        # Load the json into a Python Object
        input_genes_obj = json.loads(input_genes)

        # check if the json object input has a
        # characteristic high level ResultList key (i.e. 'result_list_name')
        if 'result_list_name' in input_genes_obj:
            # assuming it's NCATS ResultList compliant JSON
            input_result_list = ResultList.load(input_genes_obj)

            # I coerce the ResultList internally into a Pandas DataFrame
            # Perhaps we'll remove this intermediate step sometime in the future
            input_gene_data_frame = input_result_list.export_data_frame()
        else:
            # Assume that it's Pandas DataFrame compliant JSON
            input_gene_data_frame = pd.DataFrame(input_genes_obj)

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
                symbols.append('')  # symbol unknown for now?
        elif isinstance(input_genes, tuple):
            # another simple list of curies?
            for gene in input_genes:
                gene_ids.append(gene)
                symbols.append('')  # symbol unknown for now?
        else:  # assume iterable
            for gene in input_genes:
                symbol = None
                for attribute in gene.attributes:
                    if attribute.name == 'gene_symbol':
                        symbol = attribute.value
                if symbol is not None:
                    gene_ids.append(gene.gene_id)
                    symbols.append(symbol)

        genes = {"hit_id": gene_ids, "hit_symbol": symbols}
        input_gene_data_frame = pd.DataFrame(data=genes)
    else:
        raise RuntimeWarning("Unrecognized data file extension: '"+extension+"'?")

    return input_gene_data_frame


def get_simple_input_gene_list(input_genes, extension) -> List[str]:
    """
    This function returns a simple list of genes identifiers rather than a Pandas DataFrame
    :param input_genes:
    :param extension:
    :return: List[str] of input gene identifiers
    """
    input_gene_data_frame = get_input_gene_data_frame(input_genes, extension)
    simple_gene_list = [hit_id for hit_id in input_gene_data_frame['hit_id']]
    return simple_gene_list


class Config():

    def __init__(self):
        # Production endpoint
        self.biolink_api_endpoint = "http://api.monarchinitiative.org/api/"

        # Development endpoint - sometimes temporarily used
        #self.biolink_api_endpoint = "http://api-dev.monarchinitiative.org/api/"

    def get_biolink_api_endpoint(self):
        return self.biolink_api_endpoint