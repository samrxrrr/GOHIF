# Global One Health Intelligence Framework (GOHIF)

## Project Vision

GOHIF is a reproducible, explainable, evidence-driven computational framework for integrating heterogeneous One Health evidence to support antimicrobial resistance surveillance, evidence harmonization, hypothesis generation, and decision support.

---

## Phase 2 Progress

- Frozen Domains: **4 / 9**
- Registered Datasets: **24**

### Domain Status

- ✅ **Human Health** (Frozen)
- ✅ **Animal Health** (Frozen)
- ✅ **Environmental Health** (Frozen)
- ✅ **Food Chain** (Frozen)
- ⏳ **Plant Health** (Pending)
- ⏳ **Genomics & Molecular Evidence** (Pending)
- ⏳ **Knowledge Resources** (Pending)
- ⏳ **Metadata & Data Quality** (Pending)
- ⏳ **Validation & Benchmarking** (Pending)

---

## Repository Architecture

```
data/registry/          Dataset registry
docs/domain_registry/   Domain registry
docs/MRD/              Research documentation
docs/MDD/              Development documentation
scripts/sync/          Synchronization engine
build/phase2/          Generated artifacts
```

---

## Synchronization

Regenerate all master documentation using:

```bash
python3 scripts/sync/sync_phase2.py
```

---

## Current Status

The project currently uses:

- Dataset Registry
- Domain Registry
- Automated Master Dataset Inventory
- Automated Master Research Document
- Automated Master Development Document
- Synchronization Engine
