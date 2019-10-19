# coding: utf-8

"""
    NCATS Translator Modules Ontology Jaccard Similarity Server

    NCATS Translator Modules Ontology Jaccard Similarity Server  # noqa: E501

    The version of the OpenAPI document: 0.0.1
    Contact: richard@starinformatics.com
    Generated by: https://openapi-generator.tech
"""


import pprint

import six


class Results(object):
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
        'computation_id': 'ComputationIdentifier',
        'similarities': 'list[Similarity]'
    }

    attribute_map = {
        'computation_id': 'computation_id',
        'similarities': 'similarities'
    }

    def __init__(self, computation_id=None, similarities=None):  # noqa: E501
        """Results - a model defined in OpenAPI"""  # noqa: E501

        self._computation_id = None
        self._similarities = None
        self.discriminator = None

        self.computation_id = computation_id
        self.similarities = similarities

    @property
    def computation_id(self):
        """Gets the computation_id of this Results.  # noqa: E501


        :return: The computation_id of this Results.  # noqa: E501
        :rtype: ComputationIdentifier
        """
        return self._computation_id

    @computation_id.setter
    def computation_id(self, computation_id):
        """Sets the computation_id of this Results.


        :param computation_id: The computation_id of this Results.  # noqa: E501
        :type: ComputationIdentifier
        """
        if computation_id is None:
            raise ValueError("Invalid value for `computation_id`, must not be `None`")  # noqa: E501

        self._computation_id = computation_id

    @property
    def similarities(self):
        """Gets the similarities of this Results.  # noqa: E501

        List of annotated Jaccard similarity results   # noqa: E501

        :return: The similarities of this Results.  # noqa: E501
        :rtype: list[Similarity]
        """
        return self._similarities

    @similarities.setter
    def similarities(self, similarities):
        """Sets the similarities of this Results.

        List of annotated Jaccard similarity results   # noqa: E501

        :param similarities: The similarities of this Results.  # noqa: E501
        :type: list[Similarity]
        """
        if similarities is None:
            raise ValueError("Invalid value for `similarities`, must not be `None`")  # noqa: E501

        self._similarities = similarities

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
        if not isinstance(other, Results):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
