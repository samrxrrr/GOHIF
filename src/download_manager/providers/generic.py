from .base import APIProvider

class GenericRESTProvider(APIProvider):

    def endpoint(self, dataset):
        return (
            dataset.get("API_Base")
            or dataset.get("Download_URL")
        )
