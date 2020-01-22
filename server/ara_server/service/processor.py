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


class Query:
    
    def __init__(self, query_pattern: KnowledgeGraph):

        self.query_pattern = query_pattern
        # Captures global structure of a given query
        
        self.bound_nodes: Dict[str, Node] = {}
        self.unbound_nodes: List[Node] = []
        self.defined_edges: Dict[str, Edge] = {}

        # Pre-process input query contents
        self._capture_query_input()

    def get_bound_nodes(self):
        return self.bound_nodes

    def get_unbound_nodes(self):
        return self.unbound_nodes

    def get_defined_edges(self):
        return self.defined_edges

    def _capture_node(self, node: Node):

        for category in node["type"]:
    
            if not kmap.get_the_knowledge_map().known_category(category):
                # Unrecognized categories in the query should trigger an error
                # we might refine this response with a more precise Exception later
                raise RuntimeError("Unknown category in node: " + str(node))
    
        # if a node h as an identifier, it is assumed "bound" to a concept instance
        # however, the  validity of the concept is not checked here
        if node["curie"]:
            for curie_id in node["curie"]:
                curie_id = curie(curie_id)
                self.bound_nodes[curie_id] = node  # multiple curie binding feasible here?
        else:
            self.unbound_nodes.append(node)
    
    def _capture_edge(self, edge: Edge):
    
        source_curie = curie(edge["source_id"])
        target_curie = curie(edge["target_id"])
    
        # Check if non-blank node source or target ids designate defined bound nodes
        if source_curie and source_curie not in self.bound_nodes:
            raise RuntimeError("Edge " + str(edge) + " contains unknown source node id?")
        if target_curie and target_curie not in self.bound_nodes:
            raise RuntimeError("Edge " + str(edge) + " contains unknown target node id?")
    
        # At least one of the edge nodes needs to be "bound" (blank nodes are ok if other node bound)
        if not (source_curie in self.bound_nodes or target_curie in self.bound_nodes):
            raise RuntimeError("Edge " + str(edge) + " needs to have at least one bound node!")
    
        # Be mindful of constrained predicates (if present...
        # empty edge type array is ok, simply  implies "any predicate")
        for predicate in edge["type"]:
            if predicate and not kmap.get_the_knowledge_map().known_predicate(predicate):
                # Unrecognized predicate in the query should trigger an error
                # we might refine this response with a more precise Exception later
                raise RuntimeError("Unknown predicate in edge: " + str(edge))
    
        edge["source_id"] = source_curie
        edge["target_id"] = target_curie
    
        # Record the edge
        self.defined_edges[edge["id"]] = edge
    
    def _capture_query_input(self):
        """
        This is the heavy lifter query dispatcher of the Workflow ARA.
    
        :param query_pattern:
        :return: Message result of the query
        """
    
        # Note that the 'capture' of the query_pattern nodes and edges
        # resolves all identifiers in the pattern into CURIEs
        for node in self.query_pattern["nodes"]:
            self._capture_node(node)
    
        for edge in self.query_pattern["edges"]:
            self._capture_edge(edge)
    
        # Decide on what query use case you have based on input data
        if DEBUG:
            pprint("Bound nodes: " + str(self.bound_nodes))
            pprint("Unbound nodes: " + str(self.unbound_nodes))
            pprint("Defined edges: " + str(self.defined_edges))


########################################
# Basic Query Use Case Implementations #
########################################

def defined_predicate_paths_between_bound_nodes(query: Query) -> bool:
    # Validate preconditions for this query use case

    # defined edges needed for this use case
    if not query.get_defined_edges():
        return False

    # need a minimum of two bound nodes
    if not query.get_bound_nodes() or len(query.get_bound_nodes()) < 2:
        return False

    # edges need to have defined predicates (i,e. 'type' not blank)
    edges_with_defined_predicates: List[Edge] = \
        [e for e in query.get_defined_edges().values() if e["type"]]
    if not edges_with_defined_predicates:
        return False

    # check if some edge links two bound nodes
    # if so,  then submit a query
    for e in edges_with_defined_predicates:
        if (e["source_id"] in query.get_bound_nodes() and
                e["target_id"] in query.get_bound_nodes()):
            logger.info("defined_predicate_paths_between_bound_nodes()...")
            return True

    return False


def any_paths_between_bound_nodes(query: Query) -> bool:
    # Validate preconditions for this query use case

    # defined edges need for this use case
    if not query.get_defined_edges():
        return False

    # need a minimum of two bound nodes
    if not query.get_bound_nodes() or len(query.get_bound_nodes()) < 2:
        return False

    # check if some edge has at least on bound node
    # if so,  then submit a query
    for e in query.get_defined_edges().values():
        if (e["source_id"] in query.get_bound_nodes() and
                e["target_id"] in query.get_bound_nodes()):
            logger.info("any_paths_between_bound_nodes()...")

            return True

    return False


# Hmm... this use case implies edges with unbound nodes, which is perhaps
# technically infeasible since unbound edges don't have curie ids?
# Do I rather need to "fill in the blanks" with an inferred edge(?)
def defined_predicate_path_between_single_bound_start_node_and_unbound_nodes(query: Query) -> bool:
    # Validate preconditions for this query use case

    # defined edges need for this use case
    if not query.get_defined_edges():
        return False

    # need a some bound nodes
    if not query.get_bound_nodes():
        return False

    # also need some unbound nodes
    if not query.get_unbound_nodes():
        return False

    edges_with_defined_predicates: List[Edge] = \
        [e for e in query.get_defined_edges().values()
         if e["type"] and
         (e["source_id"] in query.get_bound_nodes() or
          e["target_id"] in query.get_bound_nodes())
         ]

    if not edges_with_defined_predicates:
        return False

    # check if some edge with a defined predicate has
    # at least one bound node;if so,  then submit a query
    for e in edges_with_defined_predicates:
        if (e["source_id"] in query.get_bound_nodes() or
                e["target_id"] in query.get_bound_nodes()):
            logger.info("defined_predicate_path_between_single_bound_start_node_and_unbound_nodes()...")

            return True

    return False


# Hmm... this use case implies edges with unbound nodes, which is perhaps
# technically infeasible since unbound edges don't have curie ids?
# Do I rather need to "fill in the blanks" with an inferred edge(?)
def any_paths_between_single_bound_start_node_and_unbound_nodes(query: Query) -> bool:
    # Validate preconditions for this query use case

    # defined edges need for this use case
    if not query.get_defined_edges():
        return False

    # need a some bound nodes
    if not query.get_bound_nodes():
        return False

    # need a some unbound nodes too
    if not query.get_unbound_nodes():
        return False

    # check if some edge has at least on bound node
    # if so,  then submit a query
    for e in query.get_defined_edges().values():
        if (e["source_id"] in query.get_bound_nodes() or
                e["target_id"] in query.get_bound_nodes()):
            logger.info("any_paths_between_single_bound_start_node_and_unbound_nodes()...")
            return True

    return False


def with_a_single_bound_node(query: Query) -> bool:
    # Validate preconditions for this query use case

    # need a some bound nodes
    if not query.get_bound_nodes():
        return False

    logger.info("with_a_single_bound_node()...")

    return True


def process_query(query_pattern: KnowledgeGraph) -> Message:

    query = Query(query_pattern)

    # Match query use cases in order of precision
    if defined_predicate_paths_between_bound_nodes(query):
        pass
    elif any_paths_between_bound_nodes(query):
        pass
    elif defined_predicate_path_between_single_bound_start_node_and_unbound_nodes(query):
        pass
    elif any_paths_between_single_bound_start_node_and_unbound_nodes(query):
        pass
    elif with_a_single_bound_node(query):
        pass
    else:
        raise RuntimeError("Don't know how to answer answer query pattern:" + str(query_pattern))

    return Message(knowledge_graph=query_pattern)
