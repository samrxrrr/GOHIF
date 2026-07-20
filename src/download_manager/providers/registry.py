from .ena import ENAProvider
from .mgnify import MGnifyProvider
from .gbif import GBIFProvider
from .ensembl import EnsemblProvider
from .panther import PantherProvider
from .ncbi import NCBIProvider
from .generic import GenericRESTProvider


class ProviderRegistry:

    def __init__(self):

        self.generic = GenericRESTProvider()

        self.providers = {

            "ena": ENAProvider(),

            "mgnify": MGnifyProvider(),

            "gbif": GBIFProvider(),

            "ensembl": EnsemblProvider(),

            "panther": PantherProvider(),

            "ncbi": NCBIProvider(),
        }

    def resolve(self,dataset):

        text=" ".join([
            str(dataset.get("Dataset_Name","")),
            str(dataset.get("Organization","")),
            str(dataset.get("Download_URL",""))
        ]).lower()

        for key,obj in self.providers.items():
            if key in text:
                return obj

        return self.generic
