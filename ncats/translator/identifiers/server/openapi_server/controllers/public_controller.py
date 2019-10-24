import connexion
import six

from openapi_server.model.identifier_mapping import IdentifierMapping  # noqa: E501
from openapi_server.model.query_id import QueryId  # noqa: E501
from openapi_server import util

from .controller_impl import (
    handle_identifier_list,
    handle_list_identifier_keys,
    handle_translate,
    handle_translate_one
)


def identifier_list(request_body=None):  # noqa: E501
    """post a list of identifiers

    Post a list of source identifiers for subsequent translation  # noqa: E501

    :param request_body: Identifier list to post on server (for translation) 
    :type request_body: List[str]

    :rtype: Tuple( QueryId, int ) representing the identifier_list_id and status code 201  (if successful)
    """
    return handle_identifier_list(request_body)


def list_identifier_keys():  # noqa: E501
    """list of valid key strings for identifier sources and targets

    Returns list of valid key strings for source and target parameters in other API calls  # noqa: E501


    :rtype: List[str]
    """
    return handle_list_identifier_keys()


def translate(list_identifier, target_namespace):  # noqa: E501
    """Translates list of identifiers from source to target namespace 

    Translates a previously posted list of identifiers from source namespace to a specified target namespace  # noqa: E501

    :param list_identifier: UUID from identifier_list post of source identifiers 
    :type list_identifier: str
    :param target_namespace: Target namespace for mapping of source identifiers 
    :type target_namespace: str

    :rtype: List[IdentifierMapping]
    """
    return handle_translate(list_identifier, target_namespace)


def translate_one(source_identifier, target_namespace):  # noqa: E501
    """translates one identifier source to target namespace

    Returns mapping of identifier source to its equivalent identifier in the specified target namespace  # noqa: E501

    :param source_identifier: single source identifier to be mapped onto the target 
    :type source_identifier: str
    :param target_namespace: target namespace for the mapping of the source 
    :type target_namespace: str

    :rtype: IdentifierMapping
    """
    return handle_translate_one(source_identifier, target_namespace)
