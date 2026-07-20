from .base import APIProvider

class EnsemblProvider(APIProvider):

    def endpoint(self, dataset):
        return "https://rest.ensembl.org/info/ping"

    def headers(self):
        return {
            "Content-Type":"application/json",
            "User-Agent":"GOHIF/1.0"
        }
