from .base import APIProvider

class ENAProvider(APIProvider):

    def endpoint(self, dataset):
        return "https://www.ebi.ac.uk/ena/portal/api/search"

    def params(self, dataset):
        return {
            "result":"study",
            "limit":1
        }
