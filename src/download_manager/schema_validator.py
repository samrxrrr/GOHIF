"""
GOHIF Manifest Schema Validator
"""

REQUIRED_FIELDS = {
    "HTTP": ["Download_URL", "Local_Path"],
    "REST_API": ["Download_URL", "Local_Path"],
    "REPOSITORY": ["Git_Repo", "Local_Path"],
    "NCBI_DATASETS_CLI": ["Local_Path"],
    "SRA_TOOLKIT": ["SRR", "Local_Path"],
    "CLI": ["CLI_Command"],
}


def validate_row(row):
    method = row.get("Download_Method", "").strip()

    required = REQUIRED_FIELDS.get(method, [])

    missing = []

    for field in required:
        if not row.get(field):
            missing.append(field)

    return missing
