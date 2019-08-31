import os.path
from abc import ABC
from urllib.parse import urlparse

import requests

import pandas as pd

from translator_modules.core.data_transfer_model import ResultList


class Payload(ABC):

    def __init__(self, mod):
        """
        Conventions for Payloads?
        - They expect CSV/TSV files or JSON files in 'record' form (a list of dictionaries that name-index tuples of data)
        - Their internal representation of these datatypes
        - If the internal representation needs to be transformed into something usable by one of its methods, it is the
            responsibility of the method to do the data conversion. For example, if we need to iterate over records, the dictionary
            conversion is done inside the method.
            - This is tenable as a design principle due to the first convention causing us to expect DataFrames by default, but
            we shouldn't know what the method is going to require and do the conversion, **as that leaks out information
            about the method into a higher layer of the code.**

        """
        self.mod = mod
        self.results = None

    def handle_input_or_input_location(self, input_or_input_location):
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

        if not type(input_or_input_location) is str:
            extension = None
            return input_or_input_location, extension

        if type(input_or_input_location) is str and os.path.isfile(input_or_input_location):
            input_file = input_or_input_location
            extension = os.path.splitext(input_file)[1][1:]  # first char is a `.`
            with open(input_file) as stream:
                payload_input = stream.read()
                return payload_input, extension

        elif type(input_or_input_location) is str and _is_url(input_or_input_location):
            input_url = input_or_input_location
            path = urlparse(input_url).path
            extension = os.path.splitext(path)[1]
            response = requests.get(input_url)
            response.raise_for_status()  # exception handling
            payload_input = response.text
            return payload_input, extension

        else:
            """
            TODO: we need to figure out why we got here: handle errors
            """
            print("good luck")
            extension = None
            return input_or_input_location, extension

    def get_data_frame(self) -> pd.DataFrame:
        return self.results

    def get_result_list(self) -> ResultList:
        """
        Alternate form of output: convert module Pandas DataFrame data into a
        NCATS Translator Module data transfer model Results in a ResultList instance.

        :return: ResultList
        """
        return ResultList.import_data_frame(self.results, self.mod)
