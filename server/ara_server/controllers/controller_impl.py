import logging
from typing import Dict, List

from ara_server.models.message import Message

from ncats.translator.core.knowledge_map import KnowledgeMap as kmap
from ara_server.service.processor import process_query

"""
Handler delegation functions to inject and connect into OpenAPI controller stubs:

from .controller_impl import handle_predicates_get

#or
from .controller_impl import handle_query

"""


def handle_predicates_get() -> Dict[str, Dict[str, List[str]]]:
    return kmap.get_the_knowledge_map().predicates()


def handle_query(request_body: dict) -> Message:

    if request_body:

        try:
            input_message = Message(**request_body["message"])

            # we assume that only the knowledge graph contains the query
            # pattern against which to orchestrate a computational result
            knowledge_graph = input_message.knowledge_graph

            result = process_query(knowledge_graph)

        except Exception as e:
            logging.error(e)
            return str(e), 400

        return result

    else:
        logging.error("handle_query() ERROR: Empty request body?")
        return "Empty request body?", 400
