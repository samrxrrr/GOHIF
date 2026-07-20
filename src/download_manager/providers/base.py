class APIProvider:

    def endpoint(self, dataset):
        raise NotImplementedError

    def params(self, dataset):
        return {}

    def headers(self):
        return {
            "User-Agent": "GOHIF/1.0",
            "Accept": "*/*"
        }

    def validate(self):
        return True
