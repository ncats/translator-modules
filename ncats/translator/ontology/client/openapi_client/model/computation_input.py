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


class ComputationInput(object):
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
        'ontology': 'str',
        'taxon': 'str',
        'lower_bound': 'float',
        'input_genes': 'list[GeneEntry]'
    }

    attribute_map = {
        'ontology': 'ontology',
        'taxon': 'taxon',
        'lower_bound': 'lower_bound',
        'input_genes': 'input_genes'
    }

    def __init__(self, ontology=None, taxon=None, lower_bound=None, input_genes=None):  # noqa: E501
        """ComputationInput - a model defined in OpenAPI"""  # noqa: E501

        self._ontology = None
        self._taxon = None
        self._lower_bound = None
        self._input_genes = None
        self.discriminator = None

        self.ontology = ontology
        if taxon is not None:
            self.taxon = taxon
        if lower_bound is not None:
            self.lower_bound = lower_bound
        self.input_genes = input_genes

    @property
    def ontology(self):
        """Gets the ontology of this ComputationInput.  # noqa: E501

        Ontology catalog to be queried to compute the Jaccard similarity of input genes   # noqa: E501

        :return: The ontology of this ComputationInput.  # noqa: E501
        :rtype: str
        """
        return self._ontology

    @ontology.setter
    def ontology(self, ontology):
        """Sets the ontology of this ComputationInput.

        Ontology catalog to be queried to compute the Jaccard similarity of input genes   # noqa: E501

        :param ontology: The ontology of this ComputationInput.  # noqa: E501
        :type: str
        """
        if ontology is None:
            raise ValueError("Invalid value for `ontology`, must not be `None`")  # noqa: E501

        self._ontology = ontology

    @property
    def taxon(self):
        """Gets the taxon of this ComputationInput.  # noqa: E501

        Taxonomic class of ontology to be used (i.e. human, mouse)   # noqa: E501

        :return: The taxon of this ComputationInput.  # noqa: E501
        :rtype: str
        """
        return self._taxon

    @taxon.setter
    def taxon(self, taxon):
        """Sets the taxon of this ComputationInput.

        Taxonomic class of ontology to be used (i.e. human, mouse)   # noqa: E501

        :param taxon: The taxon of this ComputationInput.  # noqa: E501
        :type: str
        """

        self._taxon = taxon

    @property
    def lower_bound(self):
        """Gets the lower_bound of this ComputationInput.  # noqa: E501

        Lower bound threshold of Jaccard Similarity scores for similarities returned   # noqa: E501

        :return: The lower_bound of this ComputationInput.  # noqa: E501
        :rtype: float
        """
        return self._lower_bound

    @lower_bound.setter
    def lower_bound(self, lower_bound):
        """Sets the lower_bound of this ComputationInput.

        Lower bound threshold of Jaccard Similarity scores for similarities returned   # noqa: E501

        :param lower_bound: The lower_bound of this ComputationInput.  # noqa: E501
        :type: float
        """

        self._lower_bound = lower_bound

    @property
    def input_genes(self):
        """Gets the input_genes of this ComputationInput.  # noqa: E501

        List of input genes upon which the Jaccard similarity computation will be applied   # noqa: E501

        :return: The input_genes of this ComputationInput.  # noqa: E501
        :rtype: list[GeneEntry]
        """
        return self._input_genes

    @input_genes.setter
    def input_genes(self, input_genes):
        """Sets the input_genes of this ComputationInput.

        List of input genes upon which the Jaccard similarity computation will be applied   # noqa: E501

        :param input_genes: The input_genes of this ComputationInput.  # noqa: E501
        :type: list[GeneEntry]
        """
        if input_genes is None:
            raise ValueError("Invalid value for `input_genes`, must not be `None`")  # noqa: E501

        self._input_genes = input_genes

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
        if not isinstance(other, ComputationInput):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other