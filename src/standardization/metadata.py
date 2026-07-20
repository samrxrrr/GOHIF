"""
GOHIF Canonical Metadata Builder
"""

from pathlib import Path
from datetime import datetime
import uuid


PARSER_VERSION = "1.0.0"


def build_metadata(
    *,
    object_type,
    file_class,
    path=None,
    parser_name=""
):

    if path is not None:

        path = Path(path)

        filename = path.name

        extension = path.suffix.lower()

        size_mb = round(
            path.stat().st_size / 1024 / 1024,
            6
        )

    else:

        filename = None
        extension = None
        size_mb = None

    return {

        "Object_ID": str(uuid.uuid4()),

        "Object_Type": object_type,

        "File_Class": file_class,

        "Dataset_Domain": None,

        "Source_Database": None,

        "Filename": filename,

        "Relative_Path": None,

        "Extension": extension,

        "File_Size_MB": size_mb,

        "Component_Count": None,

        "Sequence_Count": None,

        "Read_Count": None,

        "Total_Bases": None,

        "Average_Length": None,

        "Rows": None,

        "Columns": None,

        "JSON_Type": None,

        "Top_Level_Items": None,

        "SHA256": None,

        "Validation_Status": "UNKNOWN",

        "Parser_Name": parser_name,

        "Parser_Version": PARSER_VERSION,

        "Created_UTC": datetime.utcnow().isoformat()
    }
