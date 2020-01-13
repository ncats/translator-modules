import connexion
import six

from ara_server import util
from .controller_impl import  handle_predicates_get


def predicates_get():  # noqa: E501
    """Get supported relationships by source and target

     # noqa: E501


    :rtype: Dict[str, Dict[str, List[str]]]
    """
    return handle_predicates_get()
