import connexion
import six

from ncats.translator.identifiers.server.openapi_server.model.identifier_map import IdentifierMap  # noqa: E501
from ncats.translator.identifiers.server.openapi_server.model.identifier_map_id import IdentifierMapId  # noqa: E501
from ncats.translator.identifiers.server.openapi_server import util


def load_identifier_map(identifier_map=None):  # noqa: E501
    """Identifier Resolver map initial creation

    Adds an identifier map to the Identifier Resolver  # noqa: E501

    :param identifier_map: Identifier map to be uploaded
    :type identifier_map: dict | bytes

    :rtype: IdentifierMapId
    """
    if connexion.request.is_json:
        identifier_map = IdentifierMap.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def update_identifier_map(identifier_map=None):  # noqa: E501
    """Identifier Resolver map update

    Updates identifier map in the Identifier Resolver  # noqa: E501

    :param identifier_map: Identifier map to be updated
    :type identifier_map: dict | bytes

    :rtype: IdentifierMapId
    """
    if connexion.request.is_json:
        identifier_map = IdentifierMap.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
