# coding: utf-8

"""
    NCATS Translator Modules Ontology Jaccard Similarity Server

    NCATS Translator Modules Ontology Jaccard Similarity Server  # noqa: E501

    The version of the OpenAPI document: 0.0.1
    Contact: richard@starinformatics.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class GeneEntry(object):
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
        'input_id': 'str',
        'sim_input_curie': 'str',
        'input_symbol': 'str'
    }

    attribute_map = {
        'input_id': 'input_id',
        'sim_input_curie': 'sim_input_curie',
        'input_symbol': 'input_symbol'
    }

    def __init__(self, input_id=None, sim_input_curie=None, input_symbol=None):  # noqa: E501
        """GeneEntry - a model defined in OpenAPI"""  # noqa: E501

        self._input_id = None
        self._sim_input_curie = None
        self._input_symbol = None
        self.discriminator = None

        self.input_id = input_id
        self.sim_input_curie = sim_input_curie
        self.input_symbol = input_symbol

    @property
    def input_id(self):
        """Gets the input_id of this GeneEntry.  # noqa: E501


        :return: The input_id of this GeneEntry.  # noqa: E501
        :rtype: str
        """
        return self._input_id

    @input_id.setter
    def input_id(self, input_id):
        """Sets the input_id of this GeneEntry.


        :param input_id: The input_id of this GeneEntry.  # noqa: E501
        :type: str
        """
        if input_id is None:
            raise ValueError("Invalid value for `input_id`, must not be `None`")  # noqa: E501

        self._input_id = input_id

    @property
    def sim_input_curie(self):
        """Gets the sim_input_curie of this GeneEntry.  # noqa: E501


        :return: The sim_input_curie of this GeneEntry.  # noqa: E501
        :rtype: str
        """
        return self._sim_input_curie

    @sim_input_curie.setter
    def sim_input_curie(self, sim_input_curie):
        """Sets the sim_input_curie of this GeneEntry.


        :param sim_input_curie: The sim_input_curie of this GeneEntry.  # noqa: E501
        :type: str
        """
        if sim_input_curie is None:
            raise ValueError("Invalid value for `sim_input_curie`, must not be `None`")  # noqa: E501

        self._sim_input_curie = sim_input_curie

    @property
    def input_symbol(self):
        """Gets the input_symbol of this GeneEntry.  # noqa: E501


        :return: The input_symbol of this GeneEntry.  # noqa: E501
        :rtype: str
        """
        return self._input_symbol

    @input_symbol.setter
    def input_symbol(self, input_symbol):
        """Sets the input_symbol of this GeneEntry.


        :param input_symbol: The input_symbol of this GeneEntry.  # noqa: E501
        :type: str
        """
        if input_symbol is None:
            raise ValueError("Invalid value for `input_symbol`, must not be `None`")  # noqa: E501

        self._input_symbol = input_symbol

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
        if not isinstance(other, GeneEntry):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
