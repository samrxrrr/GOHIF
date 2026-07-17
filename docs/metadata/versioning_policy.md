# Versioning Policy

## Document Information

| Field | Value |
|-------|-------|
| Domain | Metadata & Data Quality Governance |
| Document | Versioning Policy |
| Version | 1.0 |
| Status | Approved |
| Applies To | All GOHIF Resources |

---

# Purpose

The Versioning Policy establishes standardized procedures for identifying, documenting, tracking, and managing changes to all resources within the Global One Health Intelligence Framework (GOHIF).

Version control ensures scientific reproducibility, governance transparency, auditability, and long-term maintenance throughout the lifecycle of GOHIF.

---

# Objectives

The Versioning Policy aims to:

- Maintain a complete history of every resource.
- Support reproducible scientific workflows.
- Prevent loss of historical information.
- Standardize release management.
- Improve governance transparency.
- Enable synchronized documentation.
- Facilitate future public releases.
- Support long-term project sustainability.

---

# Scope

This policy applies to:

- Documentation
- Datasets
- Metadata
- Registries
- Scripts
- Software
- Workflows
- Computational models
- Benchmark resources
- Validation resources
- Figures
- Tables
- Supplementary materials

---

# Versioning Principles

Every resource shall:

- have an explicit version
- maintain historical versions
- document all significant changes
- preserve backward traceability
- support reproducibility
- maintain identifier stability
- undergo review before release

---

# Version Format

GOHIF adopts Semantic Versioning.

Format:

MAJOR.MINOR.PATCH

Example:

1.0.0

---

## Major Version

Increment when:

- architecture changes
- governance redesign occurs
- incompatible structural modifications are introduced

Examples:

1.0.0 → 2.0.0

---

## Minor Version

Increment when:

- new governance domains are added
- new datasets are integrated
- significant documentation is expanded
- functionality is enhanced without breaking compatibility

Examples:

1.2.0 → 1.3.0

---

## Patch Version

Increment when:

- typographical errors are corrected
- references are updated
- formatting is improved
- minor clarifications are introduced

Examples:

1.3.1 → 1.3.2

---

# Version Assignment

Every resource shall include:

- Current Version
- Release Date
- Previous Version
- Change Summary
- Approval Status

---

# Release Categories

Approved release categories include:

- Draft
- Internal Review
- Governance Review
- Approved Release
- Archived Release

---

# Change Classification

Changes shall be classified as:

## Major

Examples:

- governance redesign
- metadata schema revision
- repository architecture changes

---

## Minor

Examples:

- new documentation
- new datasets
- new workflow modules

---

## Patch

Examples:

- grammar correction
- formatting improvements
- citation updates
- editorial revisions

---

# Version Lifecycle

Planning

↓

Development

↓

Internal Review

↓

Governance Review

↓

Approval

↓

Release

↓

Maintenance

↓

Archival

---

# Change Log Requirements

Every released version shall document:

- Version Number
- Release Date
- Summary of Changes
- Affected Resources
- Responsible Contributor
- Approval Authority

---

# Compatibility Policy

GOHIF aims to preserve compatibility whenever practical.

Major releases may introduce breaking changes.

Minor and patch releases should maintain compatibility with existing governance documentation.

---

# Archival Policy

Archived versions shall:

- remain permanently accessible
- retain original identifiers
- preserve associated provenance
- remain citable
- not be modified after archival

---

# Governance Responsibilities

The Documentation & Governance Architecture is responsible for:

- assigning versions
- maintaining release history
- reviewing changes
- approving releases
- synchronizing documentation
- preserving archived versions

---

# Relationship to Other Governance Documents

This policy complements:

- Metadata Framework
- Metadata Dictionary
- Identifier Standards
- Controlled Vocabulary
- FAIR Compliance Framework
- Data Quality Framework
- Provenance Model

---

# References

This policy is informed by:

- Semantic Versioning Specification (SemVer)
- FAIR Guiding Principles
- W3C PROV
- DataCite Metadata Schema
- ISO 11179
- ISO 8000

