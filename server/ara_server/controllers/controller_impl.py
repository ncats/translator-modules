from typing import Dict, List

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
    return Message()
