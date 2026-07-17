# GOHIF Storage Policy

## Persistent Storage

Google Drive is the permanent scientific storage backend.

Contains:

- Raw datasets
- Processed datasets
- Harmonized datasets
- Metadata
- Provenance
- Validation
- Evidence database
- Models
- Reports
- Figures
- Releases

## Local Storage

The local SSD is used only as an execution cache.

No scientific artifact should permanently reside on the local machine.

## Git Repository

Git stores:

- Source code
- Documentation
- Configuration
- Tests
- Small example files

Large datasets are never committed.

