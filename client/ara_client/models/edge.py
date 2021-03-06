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


class Edge(object):
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
        'id': 'str',
        'type': 'str',
        'source_id': 'str',
        'target_id': 'str'
    }

    attribute_map = {
        'id': 'id',
        'type': 'type',
        'source_id': 'source_id',
        'target_id': 'target_id'
    }

    def __init__(self, id=None, type=None, source_id=None, target_id=None, local_vars_configuration=None):  # noqa: E501
        """Edge - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._type = None
        self._source_id = None
        self._target_id = None
        self.discriminator = None

        self.id = id
        if type is not None:
            self.type = type
        self.source_id = source_id
        self.target_id = target_id

    @property
    def id(self):
        """Gets the id of this Edge.  # noqa: E501

        Local identifier for this edge which is unique within this KnowledgeGraph, and perhaps within the source reasoner's knowledge graph  # noqa: E501

        :return: The id of this Edge.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Edge.

        Local identifier for this node which is unique within this KnowledgeGraph, and perhaps within the source reasoner's knowledge graph  # noqa: E501

        :param id: The id of this Edge.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def type(self):
        """Gets the type of this Edge.  # noqa: E501

        A relation, i.e. child of related_to (snake_case)  # noqa: E501

        :return: The type of this Edge.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Edge.

        A relation, i.e. child of related_to (snake_case)  # noqa: E501

        :param type: The type of this Edge.  # noqa: E501
        :type: str
        """

        self._type = type

    @property
    def source_id(self):
        """Gets the source_id of this Edge.  # noqa: E501

        Corresponds to the @id of source node of this edge  # noqa: E501

        :return: The source_id of this Edge.  # noqa: E501
        :rtype: str
        """
        return self._source_id

    @source_id.setter
    def source_id(self, source_id):
        """Sets the source_id of this Edge.

        Corresponds to the @id of source node of this edge  # noqa: E501

        :param source_id: The source_id of this Edge.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and source_id is None:  # noqa: E501
            raise ValueError("Invalid value for `source_id`, must not be `None`")  # noqa: E501

        self._source_id = source_id

    @property
    def target_id(self):
        """Gets the target_id of this Edge.  # noqa: E501

        Corresponds to the @id of target node of this edge  # noqa: E501

        :return: The target_id of this Edge.  # noqa: E501
        :rtype: str
        """
        return self._target_id

    @target_id.setter
    def target_id(self, target_id):
        """Sets the target_id of this Edge.

        Corresponds to the @id of target node of this edge  # noqa: E501

        :param target_id: The target_id of this Edge.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and target_id is None:  # noqa: E501
            raise ValueError("Invalid value for `target_id`, must not be `None`")  # noqa: E501

        self._target_id = target_id

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
        if not isinstance(other, Edge):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Edge):
            return True

        return self.to_dict() != other.to_dict()
