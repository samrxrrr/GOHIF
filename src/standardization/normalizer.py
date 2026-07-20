"""
GOHIF Metadata Normalizer
Phase 3.2

Converts parser outputs into the canonical 23-field schema.
"""

from datetime import datetime
import uuid

PARSER_NAME = "GOHIF Universal Pipeline"
PARSER_VERSION = "1.0.0"

CANONICAL_FIELDS = [
    "Object_ID",
    "Object_Type",
    "File_Class",
    "Dataset_Domain",
    "Source_Database",
    "Filename",
    "Relative_Path",
    "Extension",
    "File_Size_MB",
    "Component_Count",
    "Sequence_Count",
    "Read_Count",
    "Total_Bases",
    "Average_Length",
    "Rows",
    "Columns",
    "JSON_Type",
    "Top_Level_Items",
    "SHA256",
    "Validation_Status",
    "Parser_Name",
    "Parser_Version",
    "Created_UTC"
]


def normalize(record):

    record = dict(record)

    record.setdefault("Object_ID", str(uuid.uuid4()))
    record.setdefault("Object_Type", "FILE")
    record.setdefault("Dataset_Domain", None)
    record.setdefault("Source_Database", None)
    record.setdefault("Extension", None)
    record.setdefault("Component_Count", None)
    record.setdefault("Sequence_Count", None)
    record.setdefault("Read_Count", None)
    record.setdefault("Total_Bases", None)
    record.setdefault("Average_Length", None)
    record.setdefault("Rows", None)
    record.setdefault("Columns", None)
    record.setdefault("JSON_Type", None)
    record.setdefault("Top_Level_Items", None)
    record.setdefault("SHA256", None)

    record.setdefault("Validation_Status", "VALID")

    record.setdefault("Parser_Name", PARSER_NAME)
    record.setdefault("Parser_Version", PARSER_VERSION)
    record.setdefault("Created_UTC", datetime.utcnow().isoformat())

    for field in CANONICAL_FIELDS:
        record.setdefault(field, None)

    return {k: record[k] for k in CANONICAL_FIELDS}
