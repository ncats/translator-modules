import logging
from typing import Dict, List

from ara_server.models.query_graph import QueryGraph
from ara_server.models.message import Message
from ara_server.models.message import Message

from ncats.translator.admin.load_predicates import KnowledgeMap

"""
Handler delegation functions to inject and connect into OpenAPI controller stubs:

from .controller_impl import handle_predicates_get

#or
from .controller_impl import handle_query
"""


def handle_predicates_get() -> Dict[str, Dict[str, List[str]]]:

    if not hasattr(handle_predicates_get,"kmap"):
        handle_predicates_get.kmap = KnowledgeMap()

    return handle_predicates_get.kmap.predicates()


def handle_query(request_body: dict) -> Message:

    if request_body:

        try:
            message = Message(**request_body["message"])

        except Exception as e:
            logging.error(e)
            return "invalid request body", 400

        return message

    else:
        logging.error("handle_query() ERROR: Empty request body?")
        return "empty request body", 400
