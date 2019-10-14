# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from ncats.translator.ontology.server.openapi_server.model.base_model_ import Model
from ncats.translator.ontology.server.openapi_server.model.gene_entry import GeneEntry
from ncats.translator.ontology.server.openapi_server import util

from ncats.translator.ontology.server.openapi_server.model.gene_entry import GeneEntry  # noqa: E501


class ComputationInput(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, ontology=None, taxon=None, input_genes=None):  # noqa: E501
        """ComputationInput - a model defined in OpenAPI

        :param ontology: The ontology of this ComputationInput.  # noqa: E501
        :type ontology: str
        :param taxon: The taxon of this ComputationInput.  # noqa: E501
        :type taxon: str
        :param input_genes: The input_genes of this ComputationInput.  # noqa: E501
        :type input_genes: List[GeneEntry]
        """
        self.openapi_types = {
            'ontology': str,
            'taxon': str,
            'input_genes': List[GeneEntry]
        }

        self.attribute_map = {
            'ontology': 'ontology',
            'taxon': 'taxon',
            'input_genes': 'input_genes'
        }

        self._ontology = ontology
        self._taxon = taxon
        self._input_genes = input_genes

    @classmethod
    def from_dict(cls, dikt) -> 'ComputationInput':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ComputationInput of this ComputationInput.  # noqa: E501
        :rtype: ComputationInput
        """
        return util.deserialize_model(dikt, cls)

    @property
    def ontology(self):
        """Gets the ontology of this ComputationInput.

        Ontology catalog to be queried to compute the Jaccard similarity of input genes   # noqa: E501

        :return: The ontology of this ComputationInput.
        :rtype: str
        """
        return self._ontology

    @ontology.setter
    def ontology(self, ontology):
        """Sets the ontology of this ComputationInput.

        Ontology catalog to be queried to compute the Jaccard similarity of input genes   # noqa: E501

        :param ontology: The ontology of this ComputationInput.
        :type ontology: str
        """
        if ontology is None:
            raise ValueError("Invalid value for `ontology`, must not be `None`")  # noqa: E501

        self._ontology = ontology

    @property
    def taxon(self):
        """Gets the taxon of this ComputationInput.

        Taxonomic class of ontology to be used (i.e. human, mouse)   # noqa: E501

        :return: The taxon of this ComputationInput.
        :rtype: str
        """
        return self._taxon

    @taxon.setter
    def taxon(self, taxon):
        """Sets the taxon of this ComputationInput.

        Taxonomic class of ontology to be used (i.e. human, mouse)   # noqa: E501

        :param taxon: The taxon of this ComputationInput.
        :type taxon: str
        """

        self._taxon = taxon

    @property
    def input_genes(self):
        """Gets the input_genes of this ComputationInput.

        List of input genes upon which the Jaccard similarity computation will be applied   # noqa: E501

        :return: The input_genes of this ComputationInput.
        :rtype: List[GeneEntry]
        """
        return self._input_genes

    @input_genes.setter
    def input_genes(self, input_genes):
        """Sets the input_genes of this ComputationInput.

        List of input genes upon which the Jaccard similarity computation will be applied   # noqa: E501

        :param input_genes: The input_genes of this ComputationInput.
        :type input_genes: List[GeneEntry]
        """
        if input_genes is None:
            raise ValueError("Invalid value for `input_genes`, must not be `None`")  # noqa: E501

        self._input_genes = input_genes
