from .base import APIProvider

class GBIFProvider(APIProvider):

    def endpoint(self, dataset):
        return "https://api.gbif.org/v1/species"

    def params(self, dataset):
        return {
            "limit":1
        }
