from typing import Dict, List

from server.reasoner_server.models.message import Message

"""
Handler delegation functions to inject and connect into OpenAPI controller stubs:

from .controller_impl import handle_predicates_get

#or
from .controller_impl import handle_query
"""


def handle_predicates_get() -> Dict[str, Dict[str, List[str]]]:
    pass


def handle_query(request_body: dict | bytes) -> Message:
    return Message()
