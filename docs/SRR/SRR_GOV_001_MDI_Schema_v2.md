# GOHIF Scientific Review Record

ID: SRR-GOV-001

Title: Master Dataset Inventory (MDI) Schema Review

Version: 2.0

Status: Approved

Date: 2026-07-16

-------------------------------------------------------------------------------

# Scientific Question

Should the Master Dataset Inventory (MDI) schema be expanded before additional
One Health domains are synchronized?

-------------------------------------------------------------------------------

# Background

The initial MDI schema was designed during the Human Health domain.

Subsequent evaluation of the Animal Health domain introduced several new
scientific concepts including:

- Evidence Class
- Primary Evidence Layer
- Secondary Evidence Layers
- Coverage Function
- Governance Traceability

The original schema cannot adequately represent these concepts.

-------------------------------------------------------------------------------

# Alternatives Considered

Alternative 1

Keep the existing MDI schema.

Assessment:

Rejected.

Reason:

Important scientific information would be lost.

-------------------------------------------------------------------------------

Alternative 2

Rename MDI to Master Evidence Registry (MER).

Assessment:

Deferred.

Reason:

Scientifically attractive but would require repository-wide changes.

Recommendation:

Revisit near publication.

-------------------------------------------------------------------------------

Alternative 3

Upgrade MDI while retaining the existing name.

Assessment:

Accepted.

-------------------------------------------------------------------------------

# Strengths of Proposed Schema

- Better scientific classification
- Supports evidence ontology
- Supports governance
- Supports FAIR assessment
- Supports future evidence harmonization
- Better publication readiness
- Improved scalability

-------------------------------------------------------------------------------

# Weaknesses

- One-time migration required
- Existing Human Health records must be updated

-------------------------------------------------------------------------------

# Trade-offs

Additional columns increase documentation complexity.

However, they substantially improve scientific expressiveness,
traceability, and long-term maintainability.

-------------------------------------------------------------------------------

# Bias Assessment

No additional scientific bias introduced.

-------------------------------------------------------------------------------

# FAIR Assessment

The upgraded schema improves:

- Findability
- Interoperability
- Reusability

without reducing accessibility.

-------------------------------------------------------------------------------

# Reproducibility

Excellent.

The upgraded schema improves reproducibility by preserving additional
scientific metadata.

-------------------------------------------------------------------------------

# Novelty Assessment

The schema shifts GOHIF from a simple dataset inventory toward an
evidence-centric scientific registry.

-------------------------------------------------------------------------------

# Scientific Recommendation

Approve MDI Schema Version 2.0.

Do not rename MDI during Phase 2.

Reconsider terminology before publication.

-------------------------------------------------------------------------------

# Principal Investigator Decision

Approved

-------------------------------------------------------------------------------

End of Record

