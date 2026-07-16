# Chapter 06 — Dataset Registry

## 6.1 Purpose

Datasets constitute the primary evidence layer of GOHIF. They originate from
numerous repositories, surveillance programs, research initiatives, reference
databases, and scientific publications spanning the One Health ecosystem.

The Dataset Registry provides the conceptual architecture for describing,
organizing, and governing these datasets throughout their lifecycle within
GOHIF.

Rather than functioning as a static inventory, the Dataset Registry defines the
principles by which datasets are identified, classified, related, versioned,
and managed. The authoritative list of registered datasets, identifiers,
coverage analyses, and operational metadata is maintained separately within the
Governance Documentation.

---

## 6.2 Objectives

The Dataset Registry is designed to achieve several complementary objectives.

### Discoverability

Provide a consistent conceptual framework through which datasets can be located,
identified, and referenced across the GOHIF ecosystem.

### Interoperability

Support integration of heterogeneous datasets originating from multiple
scientific disciplines without requiring dataset-specific architectural changes.

### Traceability

Preserve the provenance and lineage of every registered dataset throughout its
lifecycle.

### Reproducibility

Enable analyses to reference stable dataset identities, versions, and
processing histories.

### Scalability

Allow the registry to expand as new repositories, surveillance programs,
reference resources, and evidence types become available.

---

## 6.3 Conceptual Scope

The Dataset Registry applies to all datasets incorporated into GOHIF,
irrespective of:

- scientific domain;
- repository of origin;
- data modality;
- analytical purpose;
- storage technology;
- file format;
- computational workflow.

The registry defines conceptual organization only and does not prescribe
implementation-specific storage or indexing mechanisms.

---

## 6.4 Dataset Lifecycle

Datasets progress through a conceptual lifecycle within GOHIF.

Typical stages include:

1. Discovery
2. Eligibility assessment
3. Registration
4. Metadata enrichment
5. Quality evaluation
6. Harmonization
7. Integration
8. Validation
9. Version update
10. Archival or retirement

Each stage contributes additional metadata while preserving provenance and
historical traceability.

---

## 6.5 Dataset Classification

Datasets may be classified using multiple complementary dimensions.

Representative classifications include:

- scientific domain;
- evidence type;
- biological system;
- observational scale;
- temporal coverage;
- geographic scope;
- analytical role;
- validation status.

Multiple classifications may coexist for a single dataset, reflecting the
multidisciplinary nature of One Health evidence.

---

## 6.6 Dataset Identity

Every registered dataset should possess a stable conceptual identity.

Identity enables:

- unambiguous referencing;
- version tracking;
- provenance preservation;
- metadata linkage;
- reproducible analyses.

Implementation details, identifier formats, and registry keys are governed by
the authoritative Dataset Registry documentation and are intentionally excluded
from this architectural specification.

---

## 6.7 Dataset Relationships

Datasets rarely exist in isolation.

Conceptual relationships may include:

- derived from another dataset;
- validation cohort;
- external reference dataset;
- complementary evidence source;
- longitudinal continuation;
- independent replication;
- harmonized integration product.

These relationships strengthen evidence interpretation while maintaining
explicit provenance.

---

## 6.8 Dataset Provenance

Provenance forms a foundational principle of GOHIF.

For every registered dataset, provenance conceptually captures:

- source repository;
- originating organization;
- acquisition pathway;
- release information;
- processing history;
- transformation lineage;
- stewardship.

Complete provenance supports transparent evidence integration and reproducible
research.

---

## 6.9 Metadata Integration

The Dataset Registry operates in conjunction with the Metadata Model.

Metadata provides descriptive context for datasets, while the Dataset Registry
provides organizational context.

Together they enable:

- semantic discovery;
- evidence integration;
- provenance tracking;
- quality assessment;
- governance;
- explainable analytical workflows.

---

## 6.10 Relationship to the Domain Registry

Datasets are associated with one or more scientific domains defined by the
Domain Registry.

This separation provides several advantages:

- domains remain scientifically stable;
- datasets may evolve independently;
- multiple datasets may support the same domain;
- multidisciplinary datasets may contribute to multiple domains
  simultaneously.

The Dataset Registry therefore complements rather than duplicates the Domain
Registry.

---

## 6.11 Relationship to Governance

This chapter defines the conceptual architecture only.

The authoritative Dataset Registry—including registered datasets, persistent
identifiers, repository mappings, coverage analyses, synchronization status,
version history, validation records, and governance policies—is maintained
within the Governance Documentation Architecture.

This separation ensures that architectural documentation remains stable while
operational registry content evolves independently.

---

## 6.12 Versioning

Scientific datasets evolve continuously through new releases, corrections,
expansions, and revisions.

The Dataset Registry therefore supports conceptual version management that
enables:

- identification of dataset releases;
- preservation of historical versions;
- comparison between successive releases;
- reproducibility of published analyses;
- transparent tracking of updates.

Versioning policies and synchronization procedures are governed by the
Documentation Architecture and supporting governance documents rather than this
chapter.

---

## 6.13 Extensibility

The Dataset Registry is intentionally designed for long-term expansion.

Future datasets may be incorporated provided they:

- satisfy governance requirements;
- align with the Metadata Model;
- preserve provenance;
- support transparent evidence integration;
- remain compatible with the Documentation Architecture.

This modular approach enables GOHIF to incorporate emerging repositories,
surveillance systems, reference databases, and future evidence sources without
requiring architectural redesign.

---

## 6.14 Interaction with GOHIF Components

The Dataset Registry conceptually interacts with multiple components of the
GOHIF architecture.

- The Domain Registry provides scientific classification.
- The Metadata Model supplies descriptive metadata.
- Governance documentation maintains authoritative registrations.
- Validation frameworks evaluate dataset suitability and quality.
- AI components consume registered datasets during evidence integration.
- Reproducibility mechanisms reference stable dataset identities and versions.
- Documentation synchronization ensures consistency across all generated
  artifacts.

Each component maintains a distinct responsibility while contributing to a
coherent evidence management architecture.

---

## 6.15 Summary

The Dataset Registry provides the conceptual foundation for organizing
scientific datasets throughout GOHIF.

By separating architectural principles from operational governance, the
registry enables scalable dataset management, transparent provenance, semantic
interoperability, reproducible analyses, and sustainable evolution of the
framework across the complete One Health evidence ecosystem.

