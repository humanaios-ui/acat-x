# INTENT-OS Phase 1: Mission — acat-x

**Document Date:** 2026-10-05  
**Practice:** empirica-foundation.carly.acat-x  
**Status:** INTENT-OS Phase 1 Assessment

---

## Mission Statement

**acat-x solves the foundation's need for rigorous, publication-grade behavioral assessment of large language models by providing standardized evaluation infrastructure and benchmark data that enables data-driven decisions about LLM selection, safety, and integration.**

---

## The Problem acat-x Solves

### For the Foundation

**Blocker:** The foundation currently lacks a standardized, reproducible framework for evaluating LLM behavior across safety and capability dimensions.

**Impact:** 
- Evaluator seat decisions rest partly on ad-hoc assessment
- Lack of quantified behavioral baselines across multiple models
- No standardized way to compare models on safety/behavioral grounds
- Difficulty integrating new models without repeating evaluation work

**acat-x's Solution:**
- Standardized 14-dimension evaluation framework
- Reproducible, citation-able benchmark results
- Multi-tier evaluation (local, API, reference models)
- Machine-readable data for aggregation and analysis

---

## Where acat-x Fits in the Evaluation Ecosystem

### Position in Foundation Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ empirica-foundation Evaluation Ecosystem                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────┐         ┌─────────────────┐           │
│  │  acat-x          │         │ empirica-       │           │
│  │  (Behavioral     │ feeds→  │ foundation-     │           │
│  │   Benchmarks)    │         │ evaluator       │           │
│  │                  │         │ (Decision seat) │           │
│  └──────────────────┘         └─────────────────┘           │
│         ↓                             ↓                       │
│    Results: 14-dim              Decisions: model             │
│    scores per model             selection, safety            │
│                                 recommendations              │
│  ┌──────────────────┐         ┌─────────────────┐           │
│  │  humanaios       │ ←feed─  │ empirica-       │           │
│  │  (Calibration    │         │ analytics       │           │
│  │   refinement)    │         │ (Aggregation)   │           │
│  └──────────────────┘         └─────────────────┘           │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Key Integration Points

| Partner | Protocol | SLA | Purpose |
|---------|----------|-----|---------|
| **empirica-foundation-evaluator** | data-feed | 24h | ACAT-X results for evaluator decision-making |
| **empirica-analytics** | propose | 24h | Evaluation dataset aggregation & publishing |
| **humanaios** | data-feed | 24h | Calibration feedback, dimension refinement |

---

## Current State of the Problem

### Phase 7 Status (Complete)
- ✅ Single-model baseline complete: Phi (3B) evaluated across all 14 dimensions
- ✅ Publication-quality analysis and documentation
- ✅ Infrastructure stable and operational
- ✅ Phase 7 deliverables: ready to ship

### Phase 3→8 Progress
- 🟡 Phase 8 goal: 7-model multi-tier evaluation (publication-grade benchmark)
- ⏳ **Blocker:** System optimization required before Phase 8 multi-tier execution
  - CPU load: 389 (target <10)
  - Free memory: 3.5 MB (target >500 MB)
  - Duration requirement: 13+ hours continuous
- 🟡 Phase 3→6: Requirements and orchestration underway (mesh-support coordination)

### Evaluation Ecosystem Gap
**Current gap:** Single-model (Phi) baseline exists, but multi-model comparison (Phase 8 goal) is needed for publication. Without Phase 8, the foundation lacks the comparative data needed to make differentiated model selection decisions.

---

## Timeline to Problem Resolution

### Critical Path: Phase 3→8 Completion
**Phase 8 (Multi-Tier Evaluation):**
- 7 models across 4 evaluation tiers (local, API, reference)
- Publish-ready comparative benchmark
- Expected completion: 8-12 days from Oct 5 (by ~Oct 13-17)

**Phase 2 Entry Gates (INTENT-OS):**
- Phase 8 results published + baseline established
- Phase 9 (optimization & scaling) prep underway
- Expected Phase 2 start: Oct 15-20

---

## Success Criteria for acat-x Mission

1. **Phase 8 Complete:** Multi-tier evaluation (7 models) executed and results published
2. **Evaluator Integration:** Results delivered to empirica-foundation-evaluator (24h SLA)
3. **Foundation Decision Support:** Quantified behavioral baselines available for model selection
4. **Reproducibility:** Code, data, and methodology documented for external publication
5. **Cross-Practice Value:** humanaios receives calibration feedback; empirica-analytics has dataset for aggregation

---

*Mission statement articulated during INTENT-OS Phase 1 assessment (Oct 5, 2026). This mission anchors acat-x's organizational value and roadmap sequencing.*
