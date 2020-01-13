import connexion
import six

from ara_server.models.message import Message  # noqa: E501
from ara_server import util
from .controller_impl import handle_query


def query(request_body):  # noqa: E501
    """Query reasoner via one of several inputs

     # noqa: E501

    :param request_body: Query information to be submitted
    :type request_body: dict | bytes

    :rtype: Message
    """
    return handle_query(request_body)
