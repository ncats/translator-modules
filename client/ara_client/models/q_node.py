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


class QNode(object):
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
        'curie': 'list[str]',
        'type': 'list[str]'
    }

    attribute_map = {
        'id': 'id',
        'curie': 'curie',
        'type': 'type'
    }

    def __init__(self, id=None, curie=None, type=None, local_vars_configuration=None):  # noqa: E501
        """QNode - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._curie = None
        self._type = None
        self.discriminator = None

        self.id = id
        if curie is not None:
            self.curie = curie
        if type is not None:
            self.type = type

    @property
    def id(self):
        """Gets the id of this QNode.  # noqa: E501

        QueryGraph internal identifier for this QNode. Recommended form: n00, n01, n02, etc.  # noqa: E501

        :return: The id of this QNode.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this QNode.

        QueryGraph internal identifier for this QNode. Recommended form: n00, n01, n02, etc.  # noqa: E501

        :param id: The id of this QNode.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def curie(self):
        """Gets the curie of this QNode.  # noqa: E501

        CURIE identifier for this node  # noqa: E501

        :return: The curie of this QNode.  # noqa: E501
        :rtype: list[str]
        """
        return self._curie

    @curie.setter
    def curie(self, curie):
        """Sets the curie of this QNode.

        CURIE identifier for this node  # noqa: E501

        :param curie: The curie of this QNode.  # noqa: E501
        :type: list[str]
        """

        self._curie = curie

    @property
    def type(self):
        """Gets the type of this QNode.  # noqa: E501


        :return: The type of this QNode.  # noqa: E501
        :rtype: list[str]
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this QNode.


        :param type: The type of this QNode.  # noqa: E501
        :type: list[str]
        """

        self._type = type

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
        if not isinstance(other, QNode):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, QNode):
            return True

        return self.to_dict() != other.to_dict()
