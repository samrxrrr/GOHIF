"""
GOHIF Production API Client

Reusable HTTP client for all REST-based datasets.
"""

from pathlib import Path
from typing import Optional

import requests


class APIClient:

    def __init__(
        self,
        timeout: int = 60,
        verify_ssl: bool = True,
    ):

        self.timeout = timeout

        self.verify_ssl = verify_ssl

        self.session = requests.Session()

        self.session.headers.update({

            "User-Agent":
                "GOHIF/1.0",

            "Accept":
                "*/*"

        })
    def set_headers(
        self,
        headers: dict,
    ) -> None:

        """
        Add or update HTTP headers.
        """

        self.session.headers.update(headers)


    def set_bearer_token(
        self,
        token: str,
    ) -> None:

        """
        Configure Bearer authentication.
        """

        self.session.headers["Authorization"] = (
            f"Bearer {token}"
        )


    def set_api_key(
        self,
        key_name: str,
        key_value: str,
    ) -> None:

        """
        Configure API key authentication.
        """

        self.session.headers[key_name] = key_value


    def get(
        self,
        url: str,
        params: Optional[dict] = None,
    ) -> requests.Response:

        response = self.session.get(

            url,

            params=params,

            timeout=self.timeout,

            verify=self.verify_ssl,

            allow_redirects=True,

        )

        response.raise_for_status()

        return response
    def post(
        self,
        url: str,
        data: Optional[dict] = None,
        json: Optional[dict] = None,
    ) -> requests.Response:

        """
        Execute an HTTP POST request.
        """

        response = self.session.post(

            url,

            data=data,

            json=json,

            timeout=self.timeout,

            verify=self.verify_ssl,

            allow_redirects=True,

        )

        response.raise_for_status()

        return response


    def download_file(
        self,
        url: str,
        output_path: str,
        chunk_size: int = 8192,
    ) -> Path:

        """
        Download a file using streaming.
        """

        output = Path(output_path)

        output.parent.mkdir(

            parents=True,

            exist_ok=True,

        )

        with self.session.get(

            url,

            stream=True,

            timeout=self.timeout,

            verify=self.verify_ssl,

        ) as response:

            response.raise_for_status()

            with open(output, "wb") as handle:

                for chunk in response.iter_content(

                    chunk_size=chunk_size

                ):

                    if chunk:

                        handle.write(chunk)

        return output


    @staticmethod
    def to_json(
        response: requests.Response,
    ):

        """
        Convert a response to JSON.
        """

        return response.json()


    def close(self):

        """
        Close the HTTP session.
        """

        self.session.close()
if __name__ == "__main__":

    print("=" * 70)
    print("GOHIF API CLIENT SELF TEST")
    print("=" * 70)

    client = APIClient()

    try:

        response = client.get(

            "https://httpbin.org/get"

        )

        print()

        print("Status :", response.status_code)

        print("URL    :", response.url)

        print("Origin :", client.to_json(response)["origin"])

        print()

        print("API Client initialized successfully.")

    finally:

        client.close()
