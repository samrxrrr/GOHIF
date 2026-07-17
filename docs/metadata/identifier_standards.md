# Identifier Standards

## Document Information

| Field | Value |
|-------|-------|
| Domain | Metadata & Data Quality Governance |
| Document | Identifier Standards |
| Version | 1.0 |
| Status | Approved |
| Applies To | All GOHIF Resources |

---

# Purpose

Persistent and globally unique identifiers are fundamental to the reproducibility, traceability, interoperability, and long-term sustainability of the Global One Health Intelligence Framework (GOHIF).

This document establishes the identifier policy governing every resource managed within GOHIF.

---

# Objectives

The identifier framework aims to:

- Ensure every resource has a unique identity.
- Prevent identifier collisions.
- Support reproducibility.
- Enable automated synchronization.
- Facilitate provenance tracking.
- Improve interoperability.
- Support FAIR principles.
- Enable future public repository integration.

---

# Identifier Principles

Identifiers shall be:

- Globally unique
- Persistent
- Human-readable where practical
- Machine-readable
- Stable over time
- Non-reusable
- Version aware
- Traceable

---

# Identifier Hierarchy

GOHIF identifiers follow a hierarchical structure.

## Level 1

Project Identifier

Example:

GOHIF

---

## Level 2

Domain Identifier

Examples:

GOHIF-HH
GOHIF-AH
GOHIF-EH
GOHIF-FC
GOHIF-PH
GOHIF-GM
GOHIF-KR
GOHIF-MD
GOHIF-VA

---

## Level 3

Dataset Identifier

Example

GOHIF-HH-DS-0001

---

## Level 4

Resource Identifier

Example

GOHIF-HH-DOC-0012

GOHIF-HH-FIG-0004

GOHIF-HH-TBL-0010

GOHIF-HH-SCR-0007

---

## Level 5

Artifact Identifier

Example

GOHIF-HH-ART-0123

---

# Identifier Prefixes

| Prefix | Resource |
|---------|----------|
| DS | Dataset |
| DOC | Documentation |
| FIG | Figure |
| TBL | Table |
| SCR | Script |
| WF | Workflow |
| MOD | Model |
| ART | Computational Artifact |
| BEN | Benchmark |
| VAL | Validation |
| LOG | Log |
| SUP | Supplementary Material |

---

# Domain Codes

| Domain | Code |
|---------|------|
| Human Health | HH |
| Animal Health | AH |
| Environmental Health | EH |
| Food Chain | FC |
| Plant Health | PH |
| Genomics & Molecular Evidence | GM |
| Knowledge Resources | KR |
| Metadata & Data Quality | MD |
| Validation & Benchmarking | VA |

---

# Identifier Assignment Rules

Every identifier shall:

- be assigned once
- never be reused
- remain permanently associated with its resource
- survive file relocation
- survive repository restructuring
- remain stable across versions

---

# External Identifiers

Where available, external identifiers shall be preserved.

Examples include:

- DOI
- PMID
- PMCID
- BioProject
- BioSample
- GEO
- SRA
- ENA
- GenBank
- UniProt
- PDB
- ChEBI
- MeSH
- NCBI Taxonomy

These identifiers complement, but do not replace, GOHIF identifiers.

---

# Identifier Validation

Identifiers shall be validated for:

- uniqueness
- format compliance
- domain consistency
- resource type consistency
- version compatibility
- registry integrity

---

# Identifier Lifecycle

Identifier creation

↓

Registration

↓

Validation

↓

Resource publication

↓

Version updates

↓

Archival

Identifiers are never reassigned after archival.

---

# Governance Responsibilities

The Documentation & Governance Architecture is responsible for:

- identifier allocation
- registry maintenance
- collision prevention
- validation
- synchronization
- long-term persistence

---

# Relationship to Other Governance Documents

This document shall be implemented together with:

- Metadata Framework
- Metadata Dictionary
- Controlled Vocabulary
- FAIR Compliance Framework
- Provenance Model
- Versioning Policy

