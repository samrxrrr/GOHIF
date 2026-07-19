from src.download_manager.adapters.http import HTTPAdapter
from src.download_manager.adapters.api import APIAdapter
from src.download_manager.adapters.git import GitAdapter
from src.download_manager.adapters.ncbi import NCBIAdapter
from src.download_manager.adapters.sra import SRAAdapter
from src.download_manager.adapters.manual import ManualAdapter


class DownloadDispatcher:

    def __init__(self):

        self.adapters = {

            "http": HTTPAdapter(),

            "api": APIAdapter(),

            "git": GitAdapter(),

            "ncbi": NCBIAdapter(),

            "sra": SRAAdapter(),

            "manual": ManualAdapter(),

            "cli": ManualAdapter()

        }

    def dispatch(self, row):

        adapter_name = str(row["Adapter"]).lower()

        if adapter_name not in self.adapters:

            raise ValueError(
                f"No adapter registered for '{adapter_name}'"
            )

        return self.adapters[adapter_name].download(row)
