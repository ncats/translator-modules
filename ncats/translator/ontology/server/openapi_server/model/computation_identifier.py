# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.model.base_model_ import Model
from openapi_server import util


class ComputationIdentifier(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, uuid=None):  # noqa: E501
        """ComputationIdentifier - a model defined in OpenAPI

        :param uuid: The uuid of this ComputationIdentifier.  # noqa: E501
        :type uuid: str
        """
        self.openapi_types = {
            'uuid': str
        }

        self.attribute_map = {
            'uuid': 'uuid'
        }

        self._uuid = uuid

    @classmethod
    def from_dict(cls, dikt) -> 'ComputationIdentifier':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ComputationIdentifier of this ComputationIdentifier.  # noqa: E501
        :rtype: ComputationIdentifier
        """
        return util.deserialize_model(dikt, cls)

    @property
    def uuid(self):
        """Gets the uuid of this ComputationIdentifier.


        :return: The uuid of this ComputationIdentifier.
        :rtype: str
        """
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        """Sets the uuid of this ComputationIdentifier.


        :param uuid: The uuid of this ComputationIdentifier.
        :type uuid: str
        """

        self._uuid = uuid
