# INTENT-OS Phase 1: Vision — acat-x

**Document Date:** 2026-10-05  
**Practice:** empirica-foundation.carly.acat-x  
**Status:** INTENT-OS Phase 1 Assessment

---

## Vision Statement

**acat-x builds a publication-grade behavioral evaluation suite for large language models, implementing the 14-dimension ACAT framework within the Inspect AI platform to create rigorous, reproducible benchmarks for AI assessment across consistency, truthfulness, sycophancy awareness, harm awareness, service orientation, autonomy respect, value alignment, and humility.**

---

## Vision Details

### What We're Building

- **Core:** The ACAT-X evaluation suite — a suite of 14 structured evaluation tasks that assess LLM behavior across multiple dimensions of capability and safety
- **Platform:** Built on Inspect AI, a framework for running reliable and reusable AI evaluations
- **Scope:** 14 dimensions split between core (8) and candidate (6) evaluations
  - **Core:** consistency, truth, sycophancy, harm, service, autonomy, value, humility
  - **Candidate:** handoff, calibration, boundary, transparency, temporal, drift
- **Output:** Quantified dimension-level scores (0.0-1.0) per model per dimension

### Why This Matters

1. **Publication-grade benchmarks:** Current evaluations are often ad-hoc and non-reproducible. acat-x creates a standardized framework that can be cited, replicated, and compared across time and teams.

2. **Behavioral focus:** Unlike traditional benchmarks (MMLU, etc.), acat-x measures *how* models behave — consistency in reasoning, alignment with truth, awareness of harm, respect for user autonomy — not just *what* they know.

3. **Multi-model comparison:** Enables publication-quality comparisons across 7+ models (from local inference like Phi to cloud APIs like Claude, GPT-4) on the same standardized rubric.

4. **Foundation research infrastructure:** Provides the foundation with data-driven evidence for LLM behavior assessment, supporting both internal decision-making and external research partnerships.

---

## Who Benefits

1. **Research Community:** Publication-grade benchmarks enable peer review, replication, and comparative analysis across LLM ecosystems

2. **Foundation (empirica-foundation):** Behavioral baselines inform evaluator seat decisions, model selection, and safety recommendations

3. **Partners (humanaios, empirica-analytics):** Calibration data and dimension refinement feedback loop

4. **Broader AI Evaluation:** Establishes a replicable framework for behavioral assessment rather than ad-hoc scoring

---

## Success Metrics

- ✅ Publication-ready analysis: Phase 7 complete (Phi baseline, 14 dimensions)
- ✅ Multi-model benchmark: Phase 8 goal (7 models × 4 tiers)
- ✅ Reproducibility: Evaluated models documented, code committed, results archived
- ✅ Integration: Results fed to empirica-foundation-evaluator via 24-hour SLA

---

*Vision articulated during INTENT-OS Phase 1 assessment (Oct 5, 2026). This vision statement anchors acat-x's roadmap and org positioning.*
