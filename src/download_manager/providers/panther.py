
from .base import APIProvider

class PantherProvider(APIProvider):

    def endpoint(self,dataset):
        return "https://pantherdb.org/"

    def params(self,dataset):
        return {}
