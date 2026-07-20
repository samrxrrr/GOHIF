from .base import APIProvider

class MGnifyProvider(APIProvider):

    def endpoint(self, dataset):
        return "https://www.ebi.ac.uk/metagenomics/api/v2/studies"
