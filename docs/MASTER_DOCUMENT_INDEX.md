# GOHIF Master Document Index

Version: 1.0

Status: Frozen

Last Updated: 2026-07-16

---

# Purpose

This document defines the documentation architecture used throughout the Global One Health Intelligence Framework (GOHIF).

Every scientific, technical, and operational artifact within GOHIF has a clearly defined purpose.

The objective is to eliminate ambiguity, prevent duplication, preserve reproducibility, and support long-term project maintenance.

---

# Documentation Architecture

```
README

↓

Master Document Index

↓

Master Research Document (MRD)

↓

Master Development Document (MDD)

↓

Master Dataset Inventory (MDI)

↓

Decision Log
```

---

# Master Documents

## README

Purpose

Project overview.

Audience

Everyone.

Contains

- Project description
- Scientific vision
- Current status
- Repository overview
- Documentation links

---

## Master Document Index

Purpose

Defines the documentation system.

Audience

Developers

Researchers

Collaborators

Contains

- Document responsibilities
- Relationships between documents
- Documentation governance

---

## Master Research Document (MRD)

Purpose

Scientific foundation.

Contains

- Research gap
- Objectives
- Scientific rationale
- Methodology
- Evidence hierarchy
- Scientific decisions

Does NOT contain

Implementation details.

---

## Master Development Document (MDD)

Purpose

Implementation blueprint.

Contains

- Computational architecture
- Data ingestion
- Harmonization
- Provenance
- FAIR implementation
- Evidence processing
- Framework development

Does NOT justify scientific decisions.

---

## Master Dataset Inventory (MDI)

Purpose

Authoritative dataset registry.

Contains

- Dataset metadata
- FAIR assessment
- Quality assessment
- Provenance
- Acceptance decisions
- Tier classification

The MDI is the single source of truth for datasets.

---

## Decision Log

Purpose

Permanent record of major project decisions.

Examples

Dataset acceptance

Framework changes

Architecture freezes

Methodology updates

Version freezes

No decision should be lost.

---

# Documentation Rules

Every major scientific milestone must update:

- README

- Master Research Document

- Master Development Document

- Master Dataset Inventory

- Decision Log

---

# Document Relationships

```
Scientific Decisions
        │
        ▼
MRD
        │
        ▼
MDD
        │
        ▼
MDI
        │
        ▼
Framework Development
```

---

# Version Control

Every frozen milestone includes

- Git commit

- Git tag

- Frozen MDI

- Frozen MRD

- Frozen MDD

---

# Current Freeze Status

README

Frozen

Master Document Index

Frozen

MDI

Human Health Frozen

MRD

Human Health Frozen

MDD

Human Health Frozen

Decision Log

Pending Initialization

---

# Next Documentation Milestone

Initialize the Decision Log.

Following that,

Animal Health evidence acquisition begins.

---

End of Document
