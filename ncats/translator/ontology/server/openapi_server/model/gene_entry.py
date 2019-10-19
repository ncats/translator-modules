# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.model.base_model_ import Model
from openapi_server import util


class GeneEntry(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, input_id=None, sim_input_curie=None, input_symbol=None):  # noqa: E501
        """GeneEntry - a model defined in OpenAPI

        :param input_id: The input_id of this GeneEntry.  # noqa: E501
        :type input_id: str
        :param sim_input_curie: The sim_input_curie of this GeneEntry.  # noqa: E501
        :type sim_input_curie: str
        :param input_symbol: The input_symbol of this GeneEntry.  # noqa: E501
        :type input_symbol: str
        """
        self.openapi_types = {
            'input_id': str,
            'sim_input_curie': str,
            'input_symbol': str
        }

        self.attribute_map = {
            'input_id': 'input_id',
            'sim_input_curie': 'sim_input_curie',
            'input_symbol': 'input_symbol'
        }

        self._input_id = input_id
        self._sim_input_curie = sim_input_curie
        self._input_symbol = input_symbol

    @classmethod
    def from_dict(cls, dikt) -> 'GeneEntry':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The GeneEntry of this GeneEntry.  # noqa: E501
        :rtype: GeneEntry
        """
        return util.deserialize_model(dikt, cls)

    @property
    def input_id(self):
        """Gets the input_id of this GeneEntry.


        :return: The input_id of this GeneEntry.
        :rtype: str
        """
        return self._input_id

    @input_id.setter
    def input_id(self, input_id):
        """Sets the input_id of this GeneEntry.


        :param input_id: The input_id of this GeneEntry.
        :type input_id: str
        """
        if input_id is None:
            raise ValueError("Invalid value for `input_id`, must not be `None`")  # noqa: E501

        self._input_id = input_id

    @property
    def sim_input_curie(self):
        """Gets the sim_input_curie of this GeneEntry.


        :return: The sim_input_curie of this GeneEntry.
        :rtype: str
        """
        return self._sim_input_curie

    @sim_input_curie.setter
    def sim_input_curie(self, sim_input_curie):
        """Sets the sim_input_curie of this GeneEntry.


        :param sim_input_curie: The sim_input_curie of this GeneEntry.
        :type sim_input_curie: str
        """
        if sim_input_curie is None:
            raise ValueError("Invalid value for `sim_input_curie`, must not be `None`")  # noqa: E501

        self._sim_input_curie = sim_input_curie

    @property
    def input_symbol(self):
        """Gets the input_symbol of this GeneEntry.


        :return: The input_symbol of this GeneEntry.
        :rtype: str
        """
        return self._input_symbol

    @input_symbol.setter
    def input_symbol(self, input_symbol):
        """Sets the input_symbol of this GeneEntry.


        :param input_symbol: The input_symbol of this GeneEntry.
        :type input_symbol: str
        """
        if input_symbol is None:
            raise ValueError("Invalid value for `input_symbol`, must not be `None`")  # noqa: E501

        self._input_symbol = input_symbol