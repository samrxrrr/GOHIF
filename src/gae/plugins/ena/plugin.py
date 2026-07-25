from __future__ import annotations

from pathlib import Path
from urllib.request import urlretrieve

from gae.interfaces.plugin import AcquisitionPlugin


class ENAPlugin(AcquisitionPlugin):

    @property
    def name(self):
        return "ena"

    async def prepare(self, manifest):
        return None

    async def authenticate(self):
        return None

    async def acquire(self, manifest, destination: Path):

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        accession = manifest.download.accession

        url = (
            "https://www.ebi.ac.uk/ena/browser/api/fasta/"
            f"{accession}"
        )

        urlretrieve(
            url,
            destination,
        )

        return destination

    async def verify(self, downloaded_file):

        return downloaded_file.exists()

    async def metadata(self, downloaded_file):

        return {
            "size": downloaded_file.stat().st_size
        }

    async def cleanup(self):
        return None
