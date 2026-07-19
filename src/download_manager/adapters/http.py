from pathlib import Path
import time
import requests
from requests.adapters import HTTPAdapter as RequestsHTTPAdapter
from urllib3.util.retry import Retry

from src.download_manager.adapters.base import BaseAdapter


class HTTPAdapter(BaseAdapter):

    def __init__(self):

        super().__init__()

        self.timeout = 60

        self.chunk_size = 1024 * 1024

        self.max_retries = 3

        self.session = self._build_session()

    def _build_session(self):

        session = requests.Session()

        retry = Retry(

            total=self.max_retries,

            connect=self.max_retries,

            read=self.max_retries,

            backoff_factor=2,

            status_forcelist=[
                429,
                500,
                502,
                503,
                504
            ],

            allowed_methods=[
                "GET",
                "HEAD"
            ]

        )

        adapter = RequestsHTTPAdapter(

            max_retries=retry

        )

        session.mount("http://", adapter)

        session.mount("https://", adapter)

        return session

    @staticmethod
    def sanitize_filename(name):

        invalid = '<>:"/\\|?*'

        for c in invalid:
            name = name.replace(c, "_")

        name = name.replace("\n", " ")

        return name.strip()

    def output_file(self, row):

        folder = self.dataset_directory(row)

        filename = self.sanitize_filename(

            row["Dataset_Name"]

        )

        return folder / f"{filename}.dat"

    def download(self, row):

        url = str(row.get("Download_URL", "")).strip()

        if not url:

            return self.result(

                success=False,

                row=row,

                message="Download_URL is empty"

            )

        destination = self.output_file(row)

        tmp_file = Path(str(destination) + ".part")

        try:

            response = self.session.get(

                url,

                stream=True,

                timeout=self.timeout,

                allow_redirects=True

            )

            response.raise_for_status()

            total_size = int(

                response.headers.get(

                    "Content-Length",

                    0

                )

            )

            downloaded = 0

            start = time.time()

            with open(tmp_file, "wb") as handle:

                for chunk in response.iter_content(

                    chunk_size=self.chunk_size

                ):

                    if not chunk:

                        continue

                    handle.write(chunk)

                    downloaded += len(chunk)

                    if total_size > 0:

                        percent = (

                            downloaded / total_size

                        ) * 100

                        print(
                            f"\r{row['GOHIF_ID']} "
                            f"{percent:6.2f}% ",
                            end=""
                        )
                    if total_size > 0:

                        elapsed = max(
                            time.time() - start,
                            1e-6
                        )

                        speed = downloaded / elapsed

                        print(

                            f"{speed / 1024 / 1024:6.2f} MB/s",

                            end=""

                        )

            print()

            tmp_file.rename(destination)

            return self.result(

                success=True,

                row=row,

                filepath=destination,

                message="Downloaded successfully"

            )

        except requests.exceptions.HTTPError as e:

            if tmp_file.exists():

                tmp_file.unlink()

            return self.result(

                success=False,

                row=row,

                message=f"HTTP Error: {e}"

            )

        except requests.exceptions.ConnectionError as e:

            if tmp_file.exists():

                tmp_file.unlink()

            return self.result(

                success=False,

                row=row,

                message=f"Connection Error: {e}"

            )
        except requests.exceptions.Timeout as e:

            if tmp_file.exists():

                tmp_file.unlink()

            return self.result(

                success=False,

                row=row,

                message=f"Timeout: {e}"

            )

        except requests.exceptions.RequestException as e:

            if tmp_file.exists():

                tmp_file.unlink()

            return self.result(

                success=False,

                row=row,

                message=f"Request Error: {e}"

            )

        except KeyboardInterrupt:

            if tmp_file.exists():

                tmp_file.unlink()

            print()

            return self.result(

                success=False,

                row=row,

                message="Download interrupted by user"

            )

        except Exception as e:

            if tmp_file.exists():

                tmp_file.unlink()

            return self.result(

                success=False,

                row=row,

                message=f"Unexpected Error: {e}"

            )
    def test_connection(self, url):

        try:

            response = self.session.head(

                url,

                allow_redirects=True,

                timeout=20

            )

            return {

                "reachable": True,

                "status_code": response.status_code,

                "content_type": response.headers.get(

                    "Content-Type",

                    ""

                ),

                "content_length": response.headers.get(

                    "Content-Length",

                    ""

                )

            }

        except Exception as e:

            return {

                "reachable": False,

                "status_code": None,

                "content_type": "",

                "content_length": "",

                "error": str(e)

            }

    def close(self):

        self.session.close()
if __name__ == "__main__":

    adapter = HTTPAdapter()

    print("=" * 60)
    print("GOHIF HTTP ADAPTER SELF TEST")
    print("=" * 60)

    test_url = "https://httpbin.org/bytes/1024"

    print()

    print("Testing connection...")

    info = adapter.test_connection(test_url)

    print(info)

    print()

    print("HTTP Adapter initialized successfully.")

    adapter.close()

