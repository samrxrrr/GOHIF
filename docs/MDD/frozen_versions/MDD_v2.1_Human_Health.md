# Global One Health Intelligence Framework (GOHIF)

# Master Development Document (MDD)

Version: 2.1

Status: Phase 2 – Human Health Frozen

Last Updated: 2026-07-16

---

# Document Purpose

The Master Development Document (MDD) defines the technical implementation strategy for GOHIF.

The MDD translates the scientific decisions documented in the Master Research Document (MRD) into a reproducible computational framework.

Unlike the MRD, the MDD does not justify scientific decisions. Instead, it specifies how accepted datasets will be ingested, standardized, harmonized, evaluated, and integrated during framework development.

This document is the authoritative implementation blueprint for Phases 3–5.

---

# Development Philosophy

GOHIF follows the principle:

**Everything is an Artifact.**

Every dataset, transformation, metadata object, quality assessment, provenance record, harmonization step, evidence score, and computational result must be reproducible and version controlled.

---

# Development Principles

The framework shall be:

- Modular
- Reproducible
- Explainable
- Extensible
- FAIR-aligned
- Provenance-preserving
- Version controlled
- Domain independent

---

# Computational Architecture

The computational workflow will follow a layered evidence architecture.

Raw Dataset

↓

Metadata Extraction

↓

Provenance Registration

↓

Quality Assessment

↓

FAIR Assessment

↓

Evidence Harmonization

↓

Evidence Graph Construction

↓

Evidence Confidence Scoring

↓

Explainable Prioritization

↓

Hypothesis Generation

↓

Decision Support

No downstream component may bypass provenance or quality assessment.

---

# Dataset Registration Strategy

Every accepted dataset receives a permanent immutable identifier.

Format:

GOHIF-DS-0001

GOHIF-DS-0002

GOHIF-DS-0003

Dataset identifiers never change.

Versions are tracked independently.

Example:

GOHIF-DS-0001-v1

GOHIF-DS-0001-v2

---

# Human Health Implementation Status

Status

Frozen

Accepted Tier 1 Datasets

- GLASS
- ATLAS
- EARS-Net
- AMRSN
- JANIS
- UKHSA AMR
- NARMS
- ReLAVRA+

Accepted Tier 2 Datasets

- ResistanceMap
- Africa CDC AMR Surveillance Initiatives

No computational processing has begun.

Only evidence acquisition and evaluation are complete.

---

# Data Ingestion Framework

Each accepted dataset will pass through the same ingestion pipeline.

Dataset Download

↓

Integrity Verification

↓

Metadata Extraction

↓

Dataset Registration

↓

Version Registration

↓

Checksum Generation

↓

Provenance Recording

↓

Storage

↓

Validation

↓

Ready for Harmonization

Each stage produces an auditable artifact.

---

# Metadata Harmonization Strategy

Metadata harmonization will standardize:

Dataset identifiers

Country names

Geographic hierarchy

Host species

Sample source

Pathogen taxonomy

Antimicrobial identifiers

Resistance terminology

Date formats

Evidence domains

Controlled vocabularies and internationally recognized ontologies will be used whenever available.

---

# Provenance Framework

Every evidence object must preserve:

Original source

Original organization

Dataset version

Download date

Retrieval method

License

Citation

Original identifier

Transformation history

No transformation may overwrite original metadata.

---

# FAIR Integration Strategy

Each dataset will receive independent FAIR evaluation.

Findable

Accessible

Interoperable

Reusable

FAIR assessments remain independent from scientific quality assessments.

---

# Evidence Quality Framework

Quality assessment will consider:

Scientific authority

Metadata completeness

Sampling strategy

Temporal coverage

Geographic coverage

Laboratory standardization

Peer-reviewed documentation

Update frequency

Known limitations

Quality scores will be calculated after all domains have been frozen.

---

# Evidence Harmonization Framework

Harmonization will integrate evidence across:

Human Health

Animal Health

Environmental Health

Food Chain

Plant Health

Genomics

Knowledge Resources

Metadata

Validation

Cross-domain datasets (e.g., NARMS) will maintain explicit links to all relevant domains.

---

# Explainable AI Preparation

Explainable AI development will not begin until:

All evidence domains have been frozen.

The MDI is complete.

Metadata harmonization has been finalized.

Evidence quality assessment has been completed.

Provenance validation has been completed.

---

# Human Health Freeze Summary

Datasets evaluated

10

Tier 1

8

Tier 2

2

Rejected

0

Human Health evidence acquisition is complete.

---

# Pending Domains

Animal Health

Environmental Health

Food Chain

Plant Health

Genomics & Molecular Evidence

Knowledge Resources

Metadata & Data Quality

Validation & Benchmarking

---

# Immediate Development Roadmap

Phase 2

Complete evidence acquisition across all domains.

↓

Finalize global MDI.

↓

Freeze MRD.

↓

Freeze MDD.

↓

Phase 3

Begin computational framework implementation.

---

# Version Control Policy

Major scientific milestones produce:

Frozen MDI

Frozen MRD

Frozen MDD

Git tag

GitHub release

This ensures complete reproducibility throughout the project lifecycle.

---

End of Document
