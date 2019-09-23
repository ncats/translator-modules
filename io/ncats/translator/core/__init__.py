import os.path
from urllib.parse import urlparse
import requests


def handle_input_or_input_location(input_or_input_location):
    """
    Figures out whether the input being opened is from a remote source or on the file-system;
    then returns the value of the input once it is extracted.
    """

    # https://stackoverflow.com/a/52455972
    def _is_url(url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False
        except AttributeError:
            return False

    if not input_or_input_location:
        raise RuntimeError("handle_input_or_input_location(): Null or empty 'input_or_input_location'?")

    if not type(input_or_input_location) is str:
        extension = None
        return input_or_input_location, extension

    else:
        if _is_url(input_or_input_location):
            input_url = input_or_input_location
            path = urlparse(input_url).path
            extension = os.path.splitext(path)[1]
            response = requests.get(input_url)
            response.raise_for_status()  # exception handling
            payload_input = response.text

            # not sure if a CSV file will be properly read in..
            return payload_input, extension

        else:
            if os.path.isabs(input_or_input_location):
                input_file = input_or_input_location
            else:
                input_file = os.path.abspath(input_or_input_location)

            if os.path.isfile(input_file):
                extension = os.path.splitext(input_file)[1][1:]  # first char is a `.`
                with open(input_file) as stream:
                    payload_input = stream.read()
                return payload_input, extension
            else:
                """
                Raw input from command line processed directly?
                """
                extension = None
                return input_or_input_location, extension

class Config():

    def __init__(self):
        # Production endpoint
        self.biolink_api_endpoint = "http://api.monarchinitiative.org/api/"

        # Development endpoint - sometimes temporarily used
        #self.biolink_api_endpoint = "http://api-dev.monarchinitiative.org/api/"

    def get_biolink_api_endpoint(self):
        return self.biolink_api_endpoint