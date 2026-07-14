# GOHIF Laboratory Manual

**Project:** Global One Health Intelligence Framework (GOHIF)

**Version:** v1.0

**Status:** Active

---

# Purpose

This manual defines the operating procedures of the GOHIF Digital Research Laboratory.

Every contributor must follow this manual throughout the lifetime of the project.

---

# Laboratory Philosophy

GOHIF is a research platform rather than a single research project.

Every activity must prioritize:

* Scientific rigor
* Reproducibility
* Transparency
* Documentation
* Validation
* Collaboration
* Long-term maintainability

---

# Core Principles

1. Framework-first.
2. One Health by design.
3. Everything is a Research Object.
4. Documentation before implementation.
5. Validation before publication.
6. No undocumented code.
7. No unreviewed merges.
8. No fabricated results.
9. No shortcuts.
10. Reproducibility is mandatory.

---

# Team Roles

## Principal Investigator

Responsibilities:

* Scientific leadership
* Engineering leadership
* Repository management
* Code review
* Architecture decisions
* Final approval
* Release management

---

## Research Collaborator

Responsibilities:

* Literature review
* Scientific documentation
* Biological interpretation
* Assigned software modules
* Validation support
* Manuscript contributions

---

# Repository Rules

The Git repository is the single source of truth.

Do not exchange project files using email or messaging applications.

All project work must flow through Git.

---

# Branch Strategy

```text
main
│
develop
│
feature/sameer/*
│
feature/collaborator/*
```

Rules:

* `main` contains only frozen releases.
* `develop` contains reviewed work.
* Feature branches are used for active development.

---

# Milestone Workflow

Every milestone follows the same lifecycle.

```text
Plan
↓
Design
↓
Implement
↓
Test
↓
Validate
↓
Review
↓
Documentation
↓
Research Objects
↓
MRD Update
↓
MDD Update
↓
Git Commit
↓
Git Tag
↓
Freeze
```

No milestone may skip any step.

---

# Coding Standards

Every source file must include:

* Module description
* Purpose
* Version
* Author
* Type hints
* Docstrings
* Error handling
* Logging
* Unit-test compatibility

No experimental code is committed to the main branch.

---

# Documentation Standards

Every major activity must update the appropriate documents.

Scientific work:

* MRD

Engineering work:

* MDD

Architecture:

* Specifications

Knowledge:

* Knowledge Base

Governance:

* Governance documents

---

# Research Objects

Every meaningful output is treated as a Research Object.

Each Research Object includes:

* Identifier
* Category
* Version
* Owner
* Reviewer
* Status
* Milestone
* Git Commit
* Validation Status

---

# Version Control

Every milestone ends with:

1. Documentation update
2. Git commit
3. Git tag (major milestones)
4. Freeze

No milestone is considered complete without version control.

---

# Validation Policy

Every engineering component must pass:

* Functional testing
* Unit testing (where applicable)
* Documentation review
* Reproducibility verification

Every scientific result must pass:

* Internal validation
* External validation (where feasible)
* Robustness assessment
* Scientific review

---

# Meeting Policy

Weekly meetings should review:

* Completed work
* Current milestone
* Open issues
* Risks
* Decisions
* Next tasks

Important decisions must be recorded in the governance decision log.

---

# Collaboration Policy

Every contribution should be:

* Assigned
* Reviewed
* Approved
* Documented
* Traceable

No anonymous or undocumented work is accepted.

---

# File Naming

Use descriptive names.

Avoid:

* final.py
* new.py
* test2.py

Prefer names that describe the purpose of the file.

---

# Commit Messages

Commits should clearly describe the completed work.

Examples:

* Initialize repository architecture
* Add configuration engine
* Implement logging framework
* Add metadata validation module

Avoid vague messages such as:

* update
* changes
* fix

---

# Freeze Policy

A milestone may be frozen only if:

* Objectives completed
* Validation passed
* Documentation updated
* MRD updated
* MDD updated
* Git commit created
* Git tag created (if applicable)

---

# Long-Term Goal

GOHIF is intended to become:

* A reusable computational framework
* A reproducible research platform
* A publication ecosystem
* A community-driven scientific resource

Every decision should support this long-term vision.
