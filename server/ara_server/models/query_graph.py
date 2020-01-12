# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from ara_server.models.base_model_ import Model
from ara_server.models.q_edge import QEdge
from ara_server.models.q_node import QNode
from ara_server import util

from ara_server.models.q_edge import QEdge  # noqa: E501
from ara_server.models.q_node import QNode  # noqa: E501

class QueryGraph(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, nodes=None, edges=None):  # noqa: E501
        """QueryGraph - a model defined in OpenAPI

        :param nodes: The nodes of this QueryGraph.  # noqa: E501
        :type nodes: List[QNode]
        :param edges: The edges of this QueryGraph.  # noqa: E501
        :type edges: List[QEdge]
        """
        self.openapi_types = {
            'nodes': List[QNode],
            'edges': List[QEdge]
        }

        self.attribute_map = {
            'nodes': 'nodes',
            'edges': 'edges'
        }

        self._nodes = nodes
        self._edges = edges

    @classmethod
    def from_dict(cls, dikt) -> 'QueryGraph':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The QueryGraph of this QueryGraph.  # noqa: E501
        :rtype: QueryGraph
        """
        return util.deserialize_model(dikt, cls)

    @property
    def nodes(self):
        """Gets the nodes of this QueryGraph.

        List of nodes in the QueryGraph  # noqa: E501

        :return: The nodes of this QueryGraph.
        :rtype: List[QNode]
        """
        return self._nodes

    @nodes.setter
    def nodes(self, nodes):
        """Sets the nodes of this QueryGraph.

        List of nodes in the QueryGraph  # noqa: E501

        :param nodes: The nodes of this QueryGraph.
        :type nodes: List[QNode]
        """
        if nodes is None:
            raise ValueError("Invalid value for `nodes`, must not be `None`")  # noqa: E501

        self._nodes = nodes

    @property
    def edges(self):
        """Gets the edges of this QueryGraph.

        List of edges in the QueryGraph  # noqa: E501

        :return: The edges of this QueryGraph.
        :rtype: List[QEdge]
        """
        return self._edges

    @edges.setter
    def edges(self, edges):
        """Sets the edges of this QueryGraph.

        List of edges in the QueryGraph  # noqa: E501

        :param edges: The edges of this QueryGraph.
        :type edges: List[QEdge]
        """
        if edges is None:
            raise ValueError("Invalid value for `edges`, must not be `None`")  # noqa: E501

        self._edges = edges
