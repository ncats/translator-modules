from typing import List, Tuple, Any
from uuid import uuid4
import logging

from ncats.translator.identifiers import IdentifierResolverException
from ncats.translator.identifiers.server.openapi_server.model.query_id import QueryId
from ncats.translator.identifiers.server.openapi_server.model.identifier_mapping import IdentifierMapping
from ncats.translator.identifiers.server.resolver import Resolver

"""
Handler delegation functions to inject and connect into OpenAPI controller stubs:

from .controller_impl import (
    handle_identifier_list, 
    handle_list_identifier_keys, 
    handle_translate, 
    handle_translate_one
)
"""

#  A simple-minded cache for client uploaded identifier lists
_identifier_list_cache = {}


def handle_identifier_list(request_body: List[str]) -> Tuple[Any, int]:
    """post a list of identifiers

    Post a list of source identifiers for subsequent translation  # noqa: E501

    :param request_body: Identifier list to post on server (for translation)
    :type request_body: List[str]

    :rtype: QueryId
    """

    # Make a copy of the identifier string list, just be safe
    if request_body:

        uuid = str(uuid4())

        _identifier_list_cache[uuid] = [identifier for identifier in request_body]

        list_id = QueryId(uuid)

        return list_id, 201

    else:
        logging.error("handle_identifier_list() ERROR: Empty request body?")
        return "empty request body", 400


def handle_list_identifier_keys() -> List[str]:
    """list of valid key strings for identifier sources and targets

    Returns list of valid key strings for source and target parameters in other API calls  # noqa: E501


    :rtype: List[str]
    """
    resolver = Resolver.get_the_resolver()

    keys: List[str]
    try:
        keys = resolver.list_identifier_keys()

    except IdentifierResolverException as e:
        # need to log error here?
        keys = list()

    return keys


def handle_translate(list_identifier: str, target_namespace:  str) -> List[IdentifierMapping]:
    """Translates list of identifiers from source to target namespace

    Translates a previously posted list of identifiers from source namespace to a specified target namespace  # noqa: E501

    :param list_identifier: UUID from identifier_list post of source identifiers
    :type list_identifier: str
    :param target_namespace: Target namespace for mapping of source identifiers
    :type target_namespace: str

    :rtype: List[IdentifierMapping]
    """
    # need to look up a previously cached uuid indexed identifier list here?
    mappings = list()

    if list_identifier in _identifier_list_cache:

        identifier_list = _identifier_list_cache[list_identifier]

        resolver = Resolver.get_the_resolver()

        resolver.directly_load_identifiers(identifier_list)

        try:
            mappings = resolver.translate(target_namespace)

        except IdentifierResolverException as ire:
            # need to log error here?
            pass
    else:
        # probably should report this as an error?
        pass

    # Load the return data accordingly (could be empty)

    identifier_mappings: List[IdentifierMapping] = [
        IdentifierMapping(
            source_identifier=source_identifier,
            target_namespace=target_namespace,
            target_identifier=target_identifier
        ) for source_identifier, target_identifier in mappings
    ]

    return identifier_mappings


def handle_translate_one(source_identifier: str, target_namespace: str) -> IdentifierMapping:
    """translates one identifier source to target namespace

    Returns mapping of identifier source to its equivalent identifier in the specified target namespace  # noqa: E501

    :param source_identifier: single source identifier to be mapped onto the target
    :type source_identifier: str
    :param target_namespace: target namespace for the mapping of the source
    :type target_namespace: str

    :rtype: IdentifierMapping
    """
    resolver = Resolver.get_the_resolver()

    try:
        source_identifier, target_identifier = resolver.translate_one(source_identifier, target_namespace)

    except IdentifierResolverException as ire:
        # need to log error here?
        target_identifier = ""

    mapping: IdentifierMapping = IdentifierMapping(source_identifier, target_namespace, target_identifier)

    return mapping
