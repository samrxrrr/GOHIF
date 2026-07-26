from pathlib import Path
from datetime import datetime
from src.gohif.metadata.core.base import MetadataExtractor

class GenericExtractor(MetadataExtractor):

    def supports(self, path):
        return True

    def extract(self, path):

        p = Path(path)

        return {
            "filename": p.name,
            "extension": p.suffix.lower(),
            "size_bytes": p.stat().st_size,
            "modified": datetime.fromtimestamp(
                p.stat().st_mtime
            ).isoformat(),
        }
