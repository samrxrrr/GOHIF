# GOHIF Synchronization Engine

Version: 1.0

Status: Frozen

Date: 2026-07-16

-------------------------------------------------------------------------------

## Purpose

The GOHIF Synchronization Engine automatically regenerates all master
documentation from the authoritative project registries.

-------------------------------------------------------------------------------

## Authoritative Sources

1. Dataset Registry
2. Domain Registry

The synchronization engine must not use manually maintained master
documents as sources of truth.

-------------------------------------------------------------------------------

## Generated Artifacts

- Master Dataset Inventory (CSV)
- Master Dataset Inventory (Markdown)
- Master Research Document
- Master Development Document
- README
- Synchronization Report
- Decision Summary

-------------------------------------------------------------------------------

## Validation

Before generation the engine validates:

- Frozen domains
- Coverage Analyses
- Scientific Review Records

Synchronization stops if validation fails.

-------------------------------------------------------------------------------

## Entry Point

python3 scripts/sync/sync_phase2.py

-------------------------------------------------------------------------------

## Governance Policy

The synchronization engine is frozen as Version 1.0.

Future modifications should be limited to:

- bug fixes
- support for new scientific domains
- compatibility updates

Architectural changes require a documented design decision.

