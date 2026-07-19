"""
GOHIF Download Engine v4
Manifest-driven acquisition framework
"""

from manifest import ManifestManager
from dispatcher import DownloadDispatcher

from http_downloader import download as http_download
from repository_downloader import RepositoryDownloader
from api_downloader import APIDownloader
from ncbi_downloader import NCBIDownloader
from cli_downloader import CLIDownloader
from sra_downloader import SRADownloader


MANIFEST = "metadata/downloads/GOHIF_Download_Manifest.csv"


def main():

    manifest = ManifestManager(MANIFEST)

    dispatcher = DownloadDispatcher()

    repo = RepositoryDownloader()

    api = APIDownloader()

    ncbi = NCBIDownloader()

    cli = CLIDownloader()

    sra = SRADownloader()

    print("=" * 70)
    print("GOHIF DOWNLOAD ENGINE v4")
    print("=" * 70)

    for idx, row in manifest.datasets():

        method = dispatcher.dispatch(row)

        if method is None:
            continue

        dataset = row["Dataset_Name"]

        print()
        print("=" * 60)
        print(dataset)
        print("=" * 60)

        success = False

        try:

            if method == "HTTP":

                print("HTTP backend")

                # Existing HTTP workflow
                # (keep your current output mapping here)

                success = True

            elif method == "REST_API":

                print("REST API backend")

                success = api.download(
                    row["Download_URL"],
                    row["Local_Path"]
                )

            elif method == "REPOSITORY":

                print("Repository backend")

                success = repo.download(
                    row["Git_Repo"],
                    row["Local_Path"]
                )

            elif method == "NCBI_DATASETS_CLI":

                print("NCBI Datasets backend")

                success = ncbi.download(
                    row["Accession"],
                    row["Local_Path"]
                )

            elif method == "CLI":

                print("CLI backend")

                success = cli.download(
                    row["CLI_Command"]
                )

            elif method == "SRA_TOOLKIT":

                print("SRA backend")

                success = sra.download(
                    accession=row["Accession"],
                    output_dir=row["Local_Path"]
                )

            else:

                print(f"Unknown backend: {method}")

        except Exception as e:

            print(e)

            success = False

        if success:

            manifest.update(
                idx,
                status="Success"
            )

        else:

            manifest.update(
                idx,
                status="Failed",
                error="Download failed"

            )

    print("\nGOHIF acquisition completed.")


if __name__ == "__main__":
    main()
