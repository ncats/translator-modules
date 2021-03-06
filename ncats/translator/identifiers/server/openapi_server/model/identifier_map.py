# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.model.base_model_ import Model
from openapi_server.model.query_id import QueryId
from openapi_server import util

from openapi_server.model.query_id import QueryId  # noqa: E501

class IdentifierMap(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, map_identifier=None, keys=None, records=None):  # noqa: E501
        """IdentifierMap - a model defined in OpenAPI

        :param map_identifier: The map_identifier of this IdentifierMap.  # noqa: E501
        :type map_identifier: QueryId
        :param keys: The keys of this IdentifierMap.  # noqa: E501
        :type keys: List[str]
        :param records: The records of this IdentifierMap.  # noqa: E501
        :type records: List[List]
        """
        self.openapi_types = {
            'map_identifier': QueryId,
            'keys': List[str],
            'records': List[List]
        }

        self.attribute_map = {
            'map_identifier': 'map_identifier',
            'keys': 'keys',
            'records': 'records'
        }

        self._map_identifier = map_identifier
        self._keys = keys
        self._records = records

    @classmethod
    def from_dict(cls, dikt) -> 'IdentifierMap':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The IdentifierMap of this IdentifierMap.  # noqa: E501
        :rtype: IdentifierMap
        """
        return util.deserialize_model(dikt, cls)

    @property
    def map_identifier(self):
        """Gets the map_identifier of this IdentifierMap.


        :return: The map_identifier of this IdentifierMap.
        :rtype: QueryId
        """
        return self._map_identifier

    @map_identifier.setter
    def map_identifier(self, map_identifier):
        """Sets the map_identifier of this IdentifierMap.


        :param map_identifier: The map_identifier of this IdentifierMap.
        :type map_identifier: QueryId
        """
        if map_identifier is None:
            raise ValueError("Invalid value for `map_identifier`, must not be `None`")  # noqa: E501

        self._map_identifier = map_identifier

    @property
    def keys(self):
        """Gets the keys of this IdentifierMap.

        ordered list of identifier map (header/column) keys  # noqa: E501

        :return: The keys of this IdentifierMap.
        :rtype: List[str]
        """
        return self._keys

    @keys.setter
    def keys(self, keys):
        """Sets the keys of this IdentifierMap.

        ordered list of identifier map (header/column) keys  # noqa: E501

        :param keys: The keys of this IdentifierMap.
        :type keys: List[str]
        """
        if keys is None:
            raise ValueError("Invalid value for `keys`, must not be `None`")  # noqa: E501

        self._keys = keys

    @property
    def records(self):
        """Gets the records of this IdentifierMap.

        list of identifier map entries for every identifier registered in the map   # noqa: E501

        :return: The records of this IdentifierMap.
        :rtype: List[List]
        """
        return self._records

    @records.setter
    def records(self, records):
        """Sets the records of this IdentifierMap.

        list of identifier map entries for every identifier registered in the map   # noqa: E501

        :param records: The records of this IdentifierMap.
        :type records: List[List]
        """
        if records is None:
            raise ValueError("Invalid value for `records`, must not be `None`")  # noqa: E501

        self._records = records
