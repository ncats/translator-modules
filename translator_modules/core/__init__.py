class Config():

    def __init__(self):
        # Production endpoint
        self.biolink_api_endpoint = "http://api.monarchinitiative.org/api/"

        # Development endpoint - sometimes temporarily used
        #self.biolink_api_endpoint = "http://api-dev.monarchinitiative.org/api/"

    def get_biolink_api_endpoint(self):
        return self.biolink_api_endpoint