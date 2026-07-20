"""
GOHIF Common File Metadata Utilities
"""

from pathlib import Path


def basic_file_metadata(path):

    path = Path(path)

    return {

        "Filename":
            path.name,

        "Extension":
            path.suffix.lower(),

        "File_Size_MB":
            round(
                path.stat().st_size /
                1024 /
                1024,
                6
            )

    }
