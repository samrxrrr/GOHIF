from pathlib import Path

from gae.archive.extractor import ArchiveExtractor
from gae.reporting.inspector import DatasetInspector
from gae.validation.checksum import ChecksumValidator


class PostProcessor:

    def __init__(self):

        self.extractor = ArchiveExtractor()
        self.validator = ChecksumValidator()
        self.inspector = DatasetInspector()

    def process(
        self,
        downloaded_file: Path,
        checksum=None,
    ):

        extract_dir = downloaded_file.parent / "extracted"

        suffix = "".join(downloaded_file.suffixes)

        if suffix.endswith(".zip") \
        or suffix.endswith(".tar.gz") \
        or suffix.endswith(".tar") \
        or suffix.endswith(".gz"):

            self.extractor.extract(
                downloaded_file,
                extract_dir,
            )

            metadata = self.inspector.inspect(
                extract_dir
            )

        else:

            metadata = self.inspector.inspect(
                downloaded_file.parent
            )

        valid = self.validator.validate(
            downloaded_file,
            checksum,
        )

        return {
            "checksum_valid": valid,
            "files": metadata["files"],
            "bytes": metadata["bytes"],
            "extract_dir": str(extract_dir),
        }
