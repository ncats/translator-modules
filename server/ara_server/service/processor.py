from typing import Dict, List
from pprint import pprint

from ncats.translator.identifiers import uri_to_curie

from ncats.translator.core.knowledge_map import KnowledgeMap as kmap

from server.ara_server.models.knowledge_graph import KnowledgeGraph
from server.ara_server.models.message import Message
from server.ara_server.models.node import Node
from server.ara_server.models.edge import Edge

DEBUG  =  True

_bound_nodes: Dict = {}
_unbound_nodes: List = []
_defined_edges = {}


def capture_node(node: Node):

    for category in node["type"]:

        if not kmap.get_the_knowledge_map().known_category(category):
            # Unrecognized categories in the query should trigger an error
            # we might refine this response with a more precise Exception later
            raise RuntimeError("Unknown category in node: "+str(node))

    # if a node h as an identifier, it is assumed "bound" to a concept instance
    # however, the  validity of the concept is not checked here
    # TODO: we blissfully(?) assume no duplication of nodes id's... might have to be more careful here!
    # TODO: probably also need to normalize URI's  with CURIES here(?)
    if node["id"]:
        node["id"] = uri_to_curie(node["id"])
        _bound_nodes[node["id"]] = node
    else:
        _unbound_nodes.append(node)


def capture_edge(edge: Edge):

    source_curie = uri_to_curie(edge["source_id"])
    target_curie = uri_to_curie(edge["target_id"])

    # Check if non-blank node source or target ids designate defined bound nodes
    if source_curie and source_curie not in _bound_nodes:
        raise RuntimeError("Edge "+str(edge)+" contains unknown source node id?")
    if target_curie and target_curie not in _bound_nodes:
        raise RuntimeError("Edge "+str(edge)+" contains unknown target node id?")

    # At least one of the edge nodes needs to be "bound" (blank nodes are ok if other node bound)
    if not (source_curie in _bound_nodes or target_curie in _bound_nodes):
        raise RuntimeError("Edge "+str(edge)+" needs to have at least one bound node!")

    # Be mindful of constrained predicates (if present - blank edge type is ok)
    if edge["type"] and not kmap.get_the_knowledge_map().known_predicate(edge["type"]):
        # Unrecognized predicate in the query should trigger an error
        # we might refine this response with a more precise Exception later
        raise RuntimeError("Unknown predicate in edge: " + str(edge))

    edge["source_id"] = source_curie
    edge["target_id"] = target_curie

    # Record the edge
    _defined_edges[edge["id"]] = edge


def process_query(query_pattern: KnowledgeGraph) -> Message:
    """
    This is the heavy lifter query dispatcher of the Workflow ARA.

    :param query_pattern:
    :return: Message result of the query
    """
    for node in query_pattern["nodes"]:
        capture_node(node)

    for edge in query_pattern["edges"]:
        capture_edge(edge)

    # Decide on what query use case you have based on input data
    if DEBUG:
        pprint("Bound edges: "+str(_bound_nodes))
        pprint("Unbound edges: "+str(_unbound_nodes))
        pprint("Edges: " + str(_defined_edges))

    # stub implementation echos input graph
    return Message(knowledge_graph=query_pattern)
