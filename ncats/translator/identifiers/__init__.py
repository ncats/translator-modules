from collections import defaultdict
from typing import Iterable

GENE = 'gene'
DISEASE = 'disease'
CHEMICAL_SUBSTANCE = 'chemical substance'

SYMBOL = 'Approved symbol'


def fix_curies(identifiers, prefix=''):
    """
    Adds a suitable XMLNS prefix to (an) identifier(s) known to
    be "raw" IDs as keys in a dictionary or elements in a list (or a simple string)
    :param identifiers:
    :param prefix:
    :return:
    """
    if not prefix:
        # return identifiers without modification
        # Caller may already consider them in curie format
        return identifiers

    if isinstance(identifiers, dict):
        curie_dict = defaultdict(dict)
        for key in identifiers.keys():
            curie_dict[prefix + ':' + key] = identifiers[key]
        return curie_dict

    # identifiers assumed to be just a single object identifier
    elif isinstance(identifiers, str):
        # single string to convert
        return prefix + ':' + identifiers

    elif isinstance(identifiers, Iterable):
        return [prefix + ':' + x for x in identifiers]

    else:
        raise RuntimeError("fix_curie() is not sure how to fix an instance of data type '", type(identifiers))


def object_id(curie) -> str:
    """
    Returns the object_id of a curie
    :param curie:
    :return:
    """
    if not curie:
        return curie
    part = curie.split(':')
    return part[-1]
