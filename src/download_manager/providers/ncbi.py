from .base import APIProvider

class NCBIProvider(APIProvider):

    def endpoint(self, dataset):
        return "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/"
