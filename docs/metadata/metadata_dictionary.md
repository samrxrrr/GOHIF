# Metadata Dictionary

## Document Information

| Field | Value |
|-------|-------|
| Domain | Metadata & Data Quality Governance |
| Document | Metadata Dictionary |
| Version | 1.0 |
| Status | Approved |
| Applies To | All GOHIF Resources |

---

# Purpose

The Metadata Dictionary defines the standard metadata elements required to describe, identify, validate, manage, and preserve all resources within the Global One Health Intelligence Framework (GOHIF).

It provides a common vocabulary and schema to ensure consistency, interoperability, discoverability, and reproducibility across all governance and computational domains.

---

# Metadata Classes

GOHIF metadata is organized into the following classes:

1. Administrative Metadata
2. Descriptive Metadata
3. Technical Metadata
4. Structural Metadata
5. Provenance Metadata
6. Quality Metadata
7. Access Metadata
8. Preservation Metadata

---

# Core Metadata Schema

| Field | Required | Data Type | Description |
|------|----------|-----------|-------------|
| Resource_ID | Yes | String | Globally unique resource identifier |
| Resource_Name | Yes | String | Human-readable resource name |
| Resource_Type | Yes | Controlled Vocabulary | Dataset, Document, Workflow, Script, Model, Figure, Table, etc. |
| Domain | Yes | Controlled Vocabulary | GOHIF governance domain |
| Description | Yes | Text | Summary of the resource |
| Version | Yes | Semantic Version | Resource version identifier |
| Status | Yes | Controlled Vocabulary | Draft, Review, Approved, Archived |
| Owner | Yes | String | Responsible individual or team |
| Created_Date | Yes | ISO 8601 Date | Resource creation date |
| Last_Modified | Yes | ISO 8601 Date | Most recent modification |
| License | Yes | String | Usage license |
| Language | Yes | ISO Language Code | Primary language |
| Keywords | Recommended | List | Searchable keywords |
| Source | Recommended | String | Original source or provider |
| Citation | Recommended | Text | Preferred citation |
| DOI | Optional | String | Digital Object Identifier |
| URL | Optional | URI | Persistent resource location |

---

# Dataset Metadata

Every dataset shall additionally include:

| Field | Required |
|------|----------|
| Dataset_ID | Yes |
| Dataset_Type | Yes |
| Organism | Yes |
| Host | If Applicable |
| Pathogen | If Applicable |
| Sample_Size | Recommended |
| Geographic_Coverage | Recommended |
| Temporal_Coverage | Recommended |
| Data_Modality | Yes |
| File_Format | Yes |
| File_Size | Recommended |
| Checksum | Recommended |

---

# Provenance Metadata

Each resource shall record:

- Source Institution
- Original Repository
- Acquisition Method
- Processing History
- Transformation Steps
- Responsible Contributor
- Validation Status
- Approval Date

---

# Quality Metadata

Quality metadata shall include:

- Completeness Score
- Consistency Score
- Validation Status
- Error Count
- Missing Values
- Duplicate Assessment
- Review Status
- Quality Notes

---

# Version Metadata

Each resource shall record:

- Major Version
- Minor Version
- Patch Version
- Release Date
- Previous Version
- Change Summary

---

# Controlled Fields

The following fields shall use controlled vocabularies:

- Domain
- Resource_Type
- Dataset_Type
- Status
- Validation_Status
- Access_Level
- License
- Organism
- Evidence_Type

---

# Identifier Requirements

Every metadata record shall contain at least one persistent identifier.

Preferred identifiers include:

- DOI
- UUID
- Accession Number
- GOHIF Resource ID

---

# Validation Rules

Metadata records shall satisfy the following rules:

- Mandatory fields populated
- Valid controlled vocabulary values
- Valid identifier format
- ISO-compliant dates
- No duplicate identifiers
- Consistent version numbering
- Traceable provenance

---

# Relationship to Other Governance Documents

This Metadata Dictionary is implemented alongside:

- Metadata Framework
- Identifier Standards
- Controlled Vocabulary
- FAIR Compliance Framework
- Data Quality Framework
- Provenance Model
- Versioning Policy

