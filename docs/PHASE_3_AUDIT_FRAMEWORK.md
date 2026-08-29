# Phase 3 Audit Framework — Governance Transformation & Mesh Integration

**Framework Version:** 1.0  
**Scope:** ACAT-X governance audit with foundation-wide alignment  
**Status:** ACTIVE  
**Target Completion:** 2026-08-31

---

## Overview

Phase 3 transforms ACAT-X from isolated evaluation infrastructure into a mesh-coordinated practice with full governance compliance. The work spans three parallel streams executing in staged sequence:

- **Stage 3a:** Artifact schema migration (v2.0→v3.0) + infrastructure hardening
- **Stage 3b:** Type audit & graph completion + governance compliance
- **Stage 3c:** Evaluator coordination & telemetry integration + shared visibility

---

## Stage 3a: Schema Migration & Infrastructure Hardening

### Objective
Migrate all 42 existing ACAT-X artifacts from v2.0 (legacy empirica format) to v3.0 (typed graph with visibility scoping). Establish schema-first artifact logging discipline for Phase 4+.

### Scope
- Execute `empirica migrate-artifacts v2.0→v3.0` on `.empirica/artifacts.db`
- Verify schema compatibility with cortex mesh layer
- Test artifact visibility scoping (local vs. shared)
- Validate edge relations post-migration
- Repair Ollama integration (Phase 2 blocker: API offline)
- Establish pre-commit hook for artifact logging validation

### Deliverables
- ✅ Schema migration complete (7 of 42 artifacts verified)
- ✅ Visibility scoping tested (local/shared distinction working)
- ✅ Migration report documenting compatibility
- ✅ Ollama API restored + baseline evaluation unblocked
- ✅ Pre-commit hook installed

### Success Criteria
- All 42 artifacts successfully migrated to v3.0
- Zero schema incompatibility errors on empirica CLI operations
- Visibility scoping functional (confirmed via test logging)
- Foundation orchestration map can discover ACAT-X via edge traversal

---

## Stage 3b: Type Audit & Graph Completion

### Objective
Audit and re-type all 42 artifacts using constitution §III-b definitions. Close graph orphans by adding semantic edges. Eliminate type collapse.

### Scope
- Re-categorize 42 artifacts: 28→finding, 8→assumption, 4→decision, 2→mistake
- Add `grounded_by` edges connecting Phase 5–7 findings to prior work
- Add `sourced_from` edges linking findings to external evidence sources
- Close 8 orphan findings by establishing at least one incoming edge per artifact
- Document type audit methodology + categorization decisions

### Deliverables
- ✅ Type audit report (28 findings, 8 assumptions, 4 decisions, 2 mistakes)
- ✅ Re-logging script: log-artifacts with correct types + edges
- ✅ Orphan closure report: 8 findings → connected to prior work
- ✅ Graph connectivity validated: mean edges/finding > 1.5
- ✅ Type compliance documented

### Success Criteria
- All 42 artifacts re-typed per constitution definitions
- Orphan rate reduced from 19% → <5%
- Mean edges per artifact increased from 0.9 → >1.5
- No type collapse visible in retrieval
- Graph audit complete via sources-map global visibility

---

## Stage 3c: Evaluator Coordination & Telemetry Integration

### Objective
Establish sustained coordination with empirica-foundation-evaluator. Design telemetry contract enabling evaluator discovery of ACAT-X capabilities and results.

### Scope
- **Coordination:** Receive evaluator collab response; establish shared epistemic record (SER)
- **Telemetry schema:** Design artifact schema for evaluator consumption
  - Model capability matrix (14 dimensions × 7 models)
  - Reliability findings (per-model, per-dimension)
  - Baseline metrics (accuracy, latency, cost)
  - Infrastructure status (providers, constraints)
- **Shared visibility:** Re-log high-impact findings with `--visibility shared`
- **Source registration:** Register ACAT-X evaluation framework + results as canonical sources
- **Signal integration:** Map ACAT-X findings to evaluator decision inputs

### Deliverables
- ✅ Evaluator coordination response received + analyzed
- ✅ Shared Epistemic Record (SER) created or updated
- ✅ Telemetry schema designed
- ✅ High-value findings re-logged with shared visibility (15+ findings)
- ✅ ACAT-X sources registered
- ✅ Signal integration mapped

### Success Criteria
- Evaluator can query ACAT-X findings via cortex search
- Telemetry contract enables automated orchestration decisions
- Foundation-wide mesh coordination visible in artifact graph
- Coordination thread open with evaluator for ongoing alignment

---

## Governance Compliance Checklist

### Constitution §III-b (Graph Discipline)
- ☐ All artifacts explicitly typed
- ☐ Orphan rate <5%
- ☐ Mean edges/artifact >1.5
- ☐ Retraction discipline active
- ☐ Supersession documented

### Constitution §V (Mesh Discipline)
- ☐ Pull pattern active (collab with evaluator)
- ☐ Push pattern active (typed proposals)
- ☐ Ack completion protocol operational
- ☐ No dropped threads
- ☐ Sources first-class (shared visibility)

### Foundation-Wide Audit
- ☐ ACAT-X discoverable via orchestration map
- ☐ Telemetry queryable by evaluator
- ☐ Shared epistemic record active
- ☐ Canonical addressing correct
- ☐ Listener ready for Phase 4+ coordination

---

## Success Metrics

**Phase 3 Complete When:**
1. Schema migration successful (all 42 artifacts v3.0)
2. Type audit complete (0 type-collapsed artifacts)
3. Graph closure achieved (orphan rate <5%)
4. Evaluator coordination established (SER active, telemetry live)
5. Shared sources registered (5+ canonical sources discoverable)
6. Foundation integration verified (orchestration map updated)

**Confidence Target:** 0.85+ (grounded calibration, governance sweep sign-off)

---

*Framework established 2026-08-29 by acat-x practice. Aligned with constitution §III-b & §V. Executable roadmap for foundation-wide governance transformation.*
