import logging
from typing import Dict, List
from pprint import pprint

from ncats.translator.identifiers import curie

from ncats.translator.core.knowledge_map import KnowledgeMap as kmap

from server.ara_server.models.knowledge_graph import KnowledgeGraph
from server.ara_server.models.message import Message
from server.ara_server.models.node import Node
from server.ara_server.models.edge import Edge

DEBUG = True

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

_bound_nodes: Dict[str, Node] = {}
_unbound_nodes: List[Node] = []
_defined_edges: Dict[str, Edge] = {}


def capture_node(node: Node):
    for category in node["type"]:

        if not kmap.get_the_knowledge_map().known_category(category):
            # Unrecognized categories in the query should trigger an error
            # we might refine this response with a more precise Exception later
            raise RuntimeError("Unknown category in node: " + str(node))

    # if a node h as an identifier, it is assumed "bound" to a concept instance
    # however, the  validity of the concept is not checked here
    # TODO: we blissfully(?) assume no duplication of nodes id's... might have to be more careful here!
    # TODO: probably also need to normalize URI's  with CURIES here(?)
    if node["id"]:
        node["id"] = curie(node["id"])
        _bound_nodes[node["id"]] = node
    else:
        _unbound_nodes.append(node)


def capture_edge(edge: Edge):
    source_curie = curie(edge["source_id"])
    target_curie = curie(edge["target_id"])

    # Check if non-blank node source or target ids designate defined bound nodes
    if source_curie and source_curie not in _bound_nodes:
        raise RuntimeError("Edge " + str(edge) + " contains unknown source node id?")
    if target_curie and target_curie not in _bound_nodes:
        raise RuntimeError("Edge " + str(edge) + " contains unknown target node id?")

    # At least one of the edge nodes needs to be "bound" (blank nodes are ok if other node bound)
    if not (source_curie in _bound_nodes or target_curie in _bound_nodes):
        raise RuntimeError("Edge " + str(edge) + " needs to have at least one bound node!")

    # Be mindful of constrained predicates (if present...
    # blank edge type is ok, simply  implies "any predicate")
    if edge["type"] and not kmap.get_the_knowledge_map().known_predicate(edge["type"]):
        # Unrecognized predicate in the query should trigger an error
        # we might refine this response with a more precise Exception later
        raise RuntimeError("Unknown predicate in edge: " + str(edge))

    edge["source_id"] = source_curie
    edge["target_id"] = target_curie

    # Record the edge
    _defined_edges[edge["id"]] = edge


def capture_query_input(query_pattern: KnowledgeGraph):
    """
    This is the heavy lifter query dispatcher of the Workflow ARA.

    :param query_pattern:
    :return: Message result of the query
    """

    # Note that the 'capture' of the query_pattern nodes and edges
    # resolves all identifiers in the pattern into CURIEs
    for node in query_pattern["nodes"]:
        capture_node(node)

    for edge in query_pattern["edges"]:
        capture_edge(edge)

    # Decide on what query use case you have based on input data
    if DEBUG:
        pprint("Bound nodes: " + str(_bound_nodes))
        pprint("Unbound nodes: " + str(_unbound_nodes))
        pprint("Defined edges: " + str(_defined_edges))


########################################
# Basic Query Use Case Implementations #
########################################

def defined_predicate_paths_between_bound_nodes() -> bool:
    # Validate preconditions for this query use case

    # defined edges needed for this use case
    if not _defined_edges:
        return False

    # need a minimum of two bound nodes
    if not _bound_nodes or len(_bound_nodes) < 2:
        return False

    # edges need to have defined predicates (i,e. 'type' not blank)
    edges_with_defined_predicates: List[Edge] = \
        [e for e in _defined_edges.values() if e["type"]]
    if not edges_with_defined_predicates:
        return False

    # check if some edge links two bound nodes
    # if so,  then submit a query
    for e in edges_with_defined_predicates:
        if (e["source_id"] in _bound_nodes and
                e["target_id"] in _bound_nodes):
            logger.info("defined_predicate_paths_between_bound_nodes()...")
            return True

    return False


def any_paths_between_bound_nodes() -> bool:
    # Validate preconditions for this query use case

    # defined edges need for this use case
    if not _defined_edges:
        return False

    # need a minimum of two bound nodes
    if not _bound_nodes or len(_bound_nodes) < 2:
        return False

    # check if some edge has at least on bound node
    # if so,  then submit a query
    for e in _defined_edges.values():
        if (e["source_id"] in _bound_nodes and
                e["target_id"] in _bound_nodes):
            logger.info("any_paths_between_bound_nodes()...")
            return True

    return False


# Hmm... this use case implies edges with unbound nodes, which is perhaps
# technically infeasible since unbound edges don't have curie ids?
# Do I rather need to "fill in the blanks" with an inferred edge(?)
def defined_predicate_path_between_single_bound_start_node_and_unbound_nodes() -> bool:
    # Validate preconditions for this query use case

    # defined edges need for this use case
    if not _defined_edges:
        return False

    # need a some bound nodes
    if not _bound_nodes:
        return False

    # also need some unbound nodes
    if not _unbound_nodes:
        return False

    edges_with_defined_predicates: List[Edge] = \
        [e for e in _defined_edges.values()
         if e["type"] and
         (e["source_id"] in _bound_nodes or
          e["target_id"] in _bound_nodes)
         ]

    if not edges_with_defined_predicates:
        return False

    # check if some edge with a defined predicate has
    # at least one bound node;if so,  then submit a query
    for e in edges_with_defined_predicates:
        if (e["source_id"] in _bound_nodes or
                e["target_id"] in _bound_nodes):
            logger.info("defined_predicate_path_between_single_bound_start_node_and_unbound_nodes()...")
            return True

    return False


# Hmm... this use case implies edges with unbound nodes, which is perhaps
# technically infeasible since unbound edges don't have curie ids?
# Do I rather need to "fill in the blanks" with an inferred edge(?)
def any_paths_between_single_bound_start_node_and_unbound_nodes() -> bool:
    # Validate preconditions for this query use case

    # defined edges need for this use case
    if not _defined_edges:
        return False

    # need a some bound nodes
    if not _bound_nodes:
        return False

    # need a some unbound nodes too
    if not _unbound_nodes:
        return False

    # check if some edge has at least on bound node
    # if so,  then submit a query
    for e in _defined_edges.values():
        if (e["source_id"] in _bound_nodes or
                e["target_id"] in _bound_nodes):
            logger.info("any_paths_between_single_bound_start_node_and_unbound_nodes()...")
            return True

    return False


def with_a_single_bound_node() -> bool:
    # Validate preconditions for this query use case

    # need a some bound nodes
    if not _bound_nodes:
        return False

    logger.info("with_a_single_bound_node()...")
    return True


def process_query(query_pattern: KnowledgeGraph) -> Message:
    # Pre-process input query contents
    capture_query_input(query_pattern)

    # Match query use cases in order of precision
    if defined_predicate_paths_between_bound_nodes():
        pass
    elif any_paths_between_bound_nodes():
        pass
    elif defined_predicate_path_between_single_bound_start_node_and_unbound_nodes():
        pass
    elif any_paths_between_single_bound_start_node_and_unbound_nodes():
        pass
    elif with_a_single_bound_node():
        pass
    else:
        raise RuntimeError("Don't know how to answer answer query pattern:" + str(query_pattern))

    return Message(knowledge_graph=query_pattern)
