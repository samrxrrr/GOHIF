"""
GOHIF Production REST API Adapter
"""

from pathlib import Path

from .base import BaseAdapter

from src.download_manager.api.client import APIClient
from src.download_manager.providers.registry import ProviderRegistry


class APIAdapter(BaseAdapter):

    def __init__(self):

        super().__init__()

        self.client = APIClient()
        self.registry = ProviderRegistry()


    def connect(self):

        return True

    def download(
        self,
        dataset: dict,
    ) -> dict:
        """
        Download a dataset using the GOHIF API client.
        """

        dataset_id = dataset.get("GOHIF_ID", "UNKNOWN")

        dataset_name = dataset.get("Dataset_Name", "Unknown Dataset")

        provider = self.registry.resolve(dataset)

        url = provider.endpoint(dataset)

        params = provider.params(dataset)

        output_path = dataset.get("Local_Path")

        if not url:

            return {
                "success": False,
                "dataset_id": dataset_id,
                "dataset_name": dataset_name,
                "message": "Download_URL is missing."
            }

        if not output_path:

            return {
                "success": False,
                "dataset_id": dataset_id,
                "dataset_name": dataset_name,
                "message": "Local_Path is missing."
            }

        try:

            output = self.client.download_file(
                url=url,
                output_path=output_path,
                params=params,
                headers=provider.headers()
            )

            return {
                "success": True,
                "dataset_id": dataset_id,
                "dataset_name": dataset_name,
                "output_file": str(output),
                "message": "Download completed."
            }

        except Exception as exc:

            return {
                "success": False,
                "dataset_id": dataset_id,
                "dataset_name": dataset_name,
                "message": str(exc)
            }

    def close(self):

        """
        Close the API client session.
        """

        self.client.close()

if __name__ == "__main__":

    adapter = APIAdapter()

    print("=" * 70)
    print("GOHIF API ADAPTER")
    print("=" * 70)

    print()

    print("Connection:", adapter.connect())

    adapter.close()

    print()

    print("API Adapter initialized successfully.")
