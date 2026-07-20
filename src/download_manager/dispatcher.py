"""
GOHIF Download Dispatcher

Routes registry datasets to the appropriate download adapter.
"""

from src.download_manager.adapters.http import HTTPAdapter
from src.download_manager.adapters.api import APIAdapter
from src.download_manager.adapters.git import GitAdapter
from src.download_manager.adapters.ncbi import NCBIAdapter
from src.download_manager.adapters.sra import SRAAdapter
from src.download_manager.adapters.manual import ManualAdapter


class DownloadDispatcher:
    """
    Dispatches dataset download requests to the appropriate adapter.
    """

    def __init__(self):

        self.adapters = {
            "http": HTTPAdapter(),
            "api": APIAdapter(),
            "git": GitAdapter(),
            "ncbi": NCBIAdapter(),
            "sra": SRAAdapter(),
            "manual": ManualAdapter(),
            "cli": ManualAdapter(),
        }

    def dispatch(self, row):
        """
        Dispatch a dataset row to the appropriate adapter.

        Parameters
        ----------
        row : dict or pandas.Series
            Registry entry for a dataset.

        Returns
        -------
        dict
            Standardized download result.
        """

        adapter_name = str(row.get("Adapter", "")).strip().lower()

        if adapter_name == "":
            raise ValueError(
                "Registry entry does not contain an 'Adapter' value."
            )

        if adapter_name not in self.adapters:
            raise ValueError(
                f"No adapter registered for '{adapter_name}'."
            )

        adapter = self.adapters[adapter_name]

        try:

            result = adapter.download(row)

            if isinstance(result, dict):
                return result

            return {
                "success": True,
                "adapter": adapter_name,
                "result": result,
            }

        except Exception as exc:

            return {
                "success": False,
                "adapter": adapter_name,
                "dataset": row.get("Dataset_Name", "Unknown Dataset"),
                "message": str(exc),
            }

    def close(self):
        """
        Close all adapters that expose a close() method.
        """

        for adapter in self.adapters.values():

            if hasattr(adapter, "close"):

                try:
                    adapter.close()
                except Exception:
                    pass


if __name__ == "__main__":

    print("=" * 70)
    print("GOHIF DOWNLOAD DISPATCHER")
    print("=" * 70)

    dispatcher = DownloadDispatcher()

    print()
    print("Registered adapters:")

    for name in sorted(dispatcher.adapters):
        print(f"  • {name}")

    dispatcher.close()

    print()
    print("Dispatcher initialized successfully.")
