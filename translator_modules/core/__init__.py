class Config():

    def __init__(self):
#        # Production endpoint
        self.biolink_api_endpoint = "http://api.monarchinitiative.org/api/"

        ## CX trying this development since not getting Mod1B results from Lafora disease...
#         Development endpoint - sometimes temporarily used
#        self.biolink_api_endpoint = "http://api-dev.monarchinitiative.sorg/api/"

    def get_biolink_api_endpoint(self):
        return self.biolink_api_endpoint