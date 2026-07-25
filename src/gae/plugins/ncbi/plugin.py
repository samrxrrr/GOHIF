from __future__ import annotations

from pathlib import Path
from urllib.request import urlretrieve

from Bio import Entrez

from gae.interfaces.plugin import AcquisitionPlugin


class NCBIPlugin(AcquisitionPlugin):

    @property
    def name(self):
        return "ncbi"

    async def prepare(self, manifest):

        Entrez.email = getattr(
            manifest.download,
            "email",
            "gohif@example.com",
        )

    async def authenticate(self):
        return None

    async def acquire(self, manifest, destination: Path):

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        accession = manifest.download.accession

        database = manifest.download.database

        handle = Entrez.esearch(
            db=database,
            term=accession,
        )

        record = Entrez.read(handle)

        uid = record["IdList"][0]

        url = (
            "https://eutils.ncbi.nlm.nih.gov/"
            "entrez/eutils/efetch.fcgi"
            f"?db={database}"
            f"&id={uid}"
            "&rettype=fasta"
            "&retmode=text"
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
