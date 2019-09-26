# coding: utf-8

"""
    NCATS Translator Modules Identifier Resolution Server

    NCATS Translator Modules Identifier Resolution Server  # noqa: E501

    The version of the OpenAPI document: 0.0.1
    Contact: richard@starinformatics.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class IdentifierMapId(object):
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
        'map_identifier': 'QueryId'
    }

    attribute_map = {
        'map_identifier': 'map_identifier'
    }

    def __init__(self, map_identifier=None):  # noqa: E501
        """IdentifierMapId - a model defined in OpenAPI"""  # noqa: E501

        self._map_identifier = None
        self.discriminator = None

        if map_identifier is not None:
            self.map_identifier = map_identifier

    @property
    def map_identifier(self):
        """Gets the map_identifier of this IdentifierMapId.  # noqa: E501


        :return: The map_identifier of this IdentifierMapId.  # noqa: E501
        :rtype: QueryId
        """
        return self._map_identifier

    @map_identifier.setter
    def map_identifier(self, map_identifier):
        """Sets the map_identifier of this IdentifierMapId.


        :param map_identifier: The map_identifier of this IdentifierMapId.  # noqa: E501
        :type: QueryId
        """

        self._map_identifier = map_identifier

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
        if not isinstance(other, IdentifierMapId):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other