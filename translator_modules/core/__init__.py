from abc import ABC


class Config():

    def __init__(self):
        # Production endpoint
        self.biolink_api_endpoint = "http://api.monarchinitiative.org/api/"

        # Development endpoint - sometimes temporarily used
        #self.biolink_api_endpoint = "http://api-dev.monarchinitiative.org/api/"

    def get_biolink_api_endpoint(self):
        return self.biolink_api_endpoint


class Payload(ABC):


    def __init__(self, mod):
        """
        Conventions for Payloads:
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

    def echo_input_object(self, output=None):
        return self.mod.echo_input_object(output)

    def get_input_object_id(self):
        return self.mod.get_input_object_id()

    def get_data_frame(self):
        return self.results

    def get_hits(self):
        hits = self.get_data_frame()[['hit_id', 'hit_symbol']]
        return hits

    def get_hits_dict(self):
        hits_dict = self.get_hits().to_dict(orient='records')
        return hits_dict
