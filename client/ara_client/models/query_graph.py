# coding: utf-8

"""
    OpenAPI for NCATS Biomedical Translator Reasoners

    OpenAPI for NCATS Biomedical Translator Reasoners  # noqa: E501

    The version of the OpenAPI document: 0.9.2
    Contact: edeutsch@systemsbiology.org
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from ara_client.configuration import Configuration


class QueryGraph(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'nodes': 'list[QNode]',
        'edges': 'list[QEdge]'
    }

    attribute_map = {
        'nodes': 'nodes',
        'edges': 'edges'
    }

    def __init__(self, nodes=None, edges=None, local_vars_configuration=None):  # noqa: E501
        """QueryGraph - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._nodes = None
        self._edges = None
        self.discriminator = None

        self.nodes = nodes
        self.edges = edges

    @property
    def nodes(self):
        """Gets the nodes of this QueryGraph.  # noqa: E501

        List of nodes in the QueryGraph  # noqa: E501

        :return: The nodes of this QueryGraph.  # noqa: E501
        :rtype: list[QNode]
        """
        return self._nodes

    @nodes.setter
    def nodes(self, nodes):
        """Sets the nodes of this QueryGraph.

        List of nodes in the QueryGraph  # noqa: E501

        :param nodes: The nodes of this QueryGraph.  # noqa: E501
        :type: list[QNode]
        """
        if self.local_vars_configuration.client_side_validation and nodes is None:  # noqa: E501
            raise ValueError("Invalid value for `nodes`, must not be `None`")  # noqa: E501

        self._nodes = nodes

    @property
    def edges(self):
        """Gets the edges of this QueryGraph.  # noqa: E501

        List of edges in the QueryGraph  # noqa: E501

        :return: The edges of this QueryGraph.  # noqa: E501
        :rtype: list[QEdge]
        """
        return self._edges

    @edges.setter
    def edges(self, edges):
        """Sets the edges of this QueryGraph.

        List of edges in the QueryGraph  # noqa: E501

        :param edges: The edges of this QueryGraph.  # noqa: E501
        :type: list[QEdge]
        """
        if self.local_vars_configuration.client_side_validation and edges is None:  # noqa: E501
            raise ValueError("Invalid value for `edges`, must not be `None`")  # noqa: E501

        self._edges = edges

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, QueryGraph):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, QueryGraph):
            return True

        return self.to_dict() != other.to_dict()
