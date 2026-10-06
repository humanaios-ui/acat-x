# Phase 9 Entry Gates — Multi-Model Long-Context Evaluation + Adversarial Testing

**Status:** Phase 9 Readiness Pre-Flight  
**Created:** Oct 6, 2026  
**Scope:** Prepare entry gates, prerequisites, blockers, and infrastructure readiness for Phase 9 launch  
**Owner:** acat-x (empirica-foundation.carly.acat-x)

---

## PHASE 9 SCOPE DEFINITION

### What is Phase 9?

Phase 9 extends Phase 8's multi-tier evaluation framework into **deep long-context and advanced adversarial scenarios**:

**Core Testing Objectives:**
1. **Long-Context Evaluation (Tier 3 Expansion)**
   - Extended context windows: 32K, 64K, 100K+ token sequences
   - Multi-turn conversation with preserved context
   - Performance degradation patterns (does model performance degrade as context grows?)
   - Measurement: 14 core dimensions applied to long-context scenarios
   - Success threshold: Maintainable performance (≥70% of baseline score) at 32K+ tokens

2. **Advanced Adversarial Testing (Tier 2 Hardening)**
   - Adversarial prompt injection (e.g., "ignore system prompt")
   - Conflicting instructions under ambiguity
   - Manipulation tactics (flattery, authority appeals, emotional triggers)
   - Measurement: Sycophancy, Boundary, Harm, Autonomy dimensions stressed
   - Success threshold: <15% sycophancy rate; Boundary violations <5%

3. **Cross-Tier Stability Analysis**
   - Ranking stability from Phase 7 → Phase 8 → Phase 9
   - Identify models that maintain vs. lose ground under adversarial/long-context stress
   - Success threshold: Top 3 models maintain rank ±1 position across tiers

### Success Criteria (Phase 9 Completion Definition)

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Dimension Coverage** | 14/14 dimensions evaluated in long-context tier | Count of scored dimensions per model per tier |
| **Model Coverage** | All Phase 8 models + new candidates evaluated | Count of models with Phase 9 results |
| **Long-Context Window Range** | Minimum 32K tokens; recommended up to 100K | Max context window tested per model |
| **Adversarial Prompt Library** | ≥20 unique adversarial test cases per dimension | Audit of prompts used; novelty verification |
| **Confidence Intervals** | 95% CI reported for all tier-weighted scores | Statistical bounds on rankings |
| **Cross-Tier Ranking Stability** | Spearman ρ ≥ 0.70 across tiers (B, A, LC) | Correlation analysis Phase 7→8→9 |
| **Publication Readiness** | Peer-review ready report (following Phase 8 template) | Evaluator approval of Phase 9 findings |

### Deliverables (Phase 9 Output)

1. **Phase 9 Benchmark Report** — Peer-review format (extends Phase 8 template)
2. **Long-Context Results Matrix** — Model × Dimension × Context Window
3. **Adversarial Stress Test Results** — Sycophancy/Boundary/Harm/Autonomy under adversarial pressure
4. **Cross-Tier Stability Analysis** — Ranking trajectories Phase 7→8→9
5. **Foundation Adoption Tier Updates** — Revised Tier 1/2/3 recommendations based on Phase 9 findings
6. **Technical Infrastructure Artifacts** — Long-context harness, adversarial prompt library, evaluation methodology

---

## PHASE 9 PREREQUISITES

### Prerequisite 1: Phase 8 Completion & Results Publication

**Gate Condition:** Phase 8 final report published and evaluator approval received  
**Status:** 🟡 IN PROGRESS

**Checklist:**
- [ ] Phase 8 final results aggregated in `results/phase8_batch_summary.json` ✅ (exists)
- [ ] Phase 8 report template filled and peer-review ready (see `.empirica/phase-8-report-template.md`) 🔲 PENDING
- [ ] Phase 8 findings logged and cross-linked to evaluator artifacts 🔲 PENDING
- [ ] Evaluator (Admiral) synthesis: `.empirica/evaluator-Phase-8-synthesis.md` created 🔲 PENDING
- [ ] Phase 8 constitution alignment documented (§III-b requirements) 🔲 PENDING

**How Phase 8 Enables Phase 9:**
- Phase 8 baseline scores become reference for Phase 9 long-context degradation analysis
- Phase 8 model rankings (Tier 1/2/3) define candidate set for Phase 9 deep-dive
- Phase 8 tier-weighting strategy (Baseline 50% + Adversarial 30% + Long-Context 20%) carries forward

---

### Prerequisite 2: Evaluator Approval of Phase 9 Charter

**Gate Condition:** Evaluator (Admiral) explicitly approves Phase 9 scope, methodology, and success criteria  
**Status:** 🔲 PENDING

**Checklist:**
- [ ] Phase 9 charter document shared with evaluator (this checklist + scope definition)
- [ ] Evaluator feedback on long-context window targets (32K vs. 64K vs. 100K+)
- [ ] Evaluator feedback on adversarial test case novelty requirements
- [ ] Evaluator approval recorded: date + signature / proposal acceptance
- [ ] Evaluator constraints documented (e.g., "no proprietary adversarial datasets", "use open-source only")

**Evaluator Questions to Resolve (Pre-Approval):**
1. Long-context priority: Full 100K window evaluation, or focus on 32K/64K as MVP?
2. Adversarial scope: Foundation-specific attacks only, or industry-standard red-teaming?
3. Model expansion: Evaluate new candidates (e.g., Claude 3.5 Sonnet) or stick with Phase 8 set?
4. Measurement rigor: Single sample per scenario (fast), or multi-sample with confidence intervals (slow)?

---

### Prerequisite 3: Phase 9 Infrastructure Ready

**Gate Condition:** Test harness, adversarial prompt library, and long-context evaluation environment deployed  
**Status:** 🔲 PENDING

**Checklist:**
- [ ] **Long-Context Test Harness**
  - [ ] Script: `phase9_long_context_harness.py` — handles context window setup, model inference, result logging
  - [ ] Supports streaming large inputs (prevent OOM on 100K tokens)
  - [ ] Latency + cost accounting per model per context window
  - [ ] Result schema: `{model, dimension, context_window, score, elapsed_sec, tokens_processed}`
  
- [ ] **Adversarial Prompt Library**
  - [ ] File: `data/adversarial_prompts_phase9.json` — ≥20 prompts per dimension × 14 dimensions = ≥280 prompts
  - [ ] Categories: Injection attacks, conflicting instructions, manipulation, social engineering, instruction override
  - [ ] Metadata per prompt: `{dimension, attack_type, expected_resistance_level, target_model_set}`
  - [ ] Provenance: Open-source datasets (OLMES, CausalML, or equivalent) or foundation-authored
  
- [ ] **Context Window Scaling**
  - [ ] Model compatibility check: Which models support 32K, 64K, 100K?
  - [ ] API/local infrastructure: Anthropic (supports 200K+), OpenAI (supports 128K), Ollama (limited by VRAM)
  - [ ] Cost impact analysis: Token budget for Phase 9 long-context tests (100K tokens × 100 samples × 5 models = 50M tokens)
  
- [ ] **Result Schema Migration**
  - [ ] Extend Phase 8 result format to include `{context_window, adversarial_category, attack_type}`
  - [ ] Backwards-compatible with Phase 8 results (new fields optional)
  - [ ] Storage: `results/phase9_*.json` files per tier/dimension/model

- [ ] **Local Dev Environment**
  - [ ] Python dependencies installed: inspect-ai, vLLM (if local inference), transformers
  - [ ] Ollama running (if testing local models)
  - [ ] API keys configured (OpenAI, Anthropic)
  - [ ] Storage quota: ≥10 GB for Phase 9 results

---

### Prerequisite 4: Mesh-Support Coordination & Phase 3 Specs Alignment

**Gate Condition:** Phase 3 specs integrated, mesh coordination confirmed with empirica-foundation.carly.empirica-mesh-support  
**Status:** 🟡 IN PROGRESS (Phase 3 blocker specs received Sep 5; awaiting alignment confirmation)

**Checklist:**
- [ ] Phase 3 blocker specs proposal (`prop_4eo3ake7szbhph5ekmbabndxgq`) reviewed and integrated
- [ ] Telemetry schema alignment: Phase 9 result schema compatible with Phase 3 schema
- [ ] Orchestration specs: Phase 9 evaluation can be triggered by mesh-support command
- [ ] Feedback loop: Phase 9 results flow to evaluator + foundation practices via cortex
- [ ] Escalation protocol: If Phase 9 finds blocker issues → mesh-support escalation path defined

**Phase 3 ↔ Phase 9 Integration Points:**
| Phase 3 Requirement | Phase 9 Delivery |
|---|---|
| 14 core dimensions instrumented | Phase 9 extends all 14 to long-context + adversarial tiers |
| Baseline values established | Phase 8 baselines; Phase 9 establishes long-context/adversarial baselines |
| Provider strategy defined | Phase 9 aligns with Phase 3 provider rotation (OpenAI, Ollama, Anthropic) |
| Measurement gates enabled | Phase 9 gates: Tier stability (ρ ≥0.70), context degradation <30%, adversarial resistance >80% |
| Telemetry flows to evaluator | Phase 9 results emit to empirica-foundation-evaluator via cortex |

---

## PHASE 9 BLOCKERS & UNKNOWNS

### Blocker 1: Phase 8 Report Not Yet Published

**Issue:** Phase 8 results exist but report isn't peer-review ready  
**Impact:** Evaluator cannot approve Phase 9 scope without reviewing Phase 8 findings  
**Resolution Required:** Fill Phase 8 report template (`.empirica/phase-8-report-template.md`) with actual scores and analysis  
**Owner:** acat-x  
**Effort:** 2-4 hours (aggregation + narrative + figure generation)  
**Unblocks:** Evaluator approval for Phase 9

---

### Blocker 2: Adversarial Prompt Library Not Sourced

**Issue:** No curated set of adversarial prompts for Phase 9  
**Impact:** Cannot execute Phase 9 without test cases  
**Options:**
- (A) Use published benchmarks (OLMES, BigBench-Adversarial, AdvBench) — lower cost, less novel
- (B) Foundation-author custom adversarial prompts — higher cost, more aligned to Foundation values
- (C) Hybrid: Baseline from OLMES, extend with Foundation-specific attacks
- Resolution Recommendation:** Hybrid approach; minimum 50% custom prompts
**Owner:** acat-x + mesh-support (for design review)  
**Effort:** 8-12 hours (curation + review)  
**Unblocks:** Phase 9 adversarial tier execution

---

### Blocker 3: Long-Context Cost & API Quota

**Issue:** Evaluating at 100K tokens × 100 samples × 5 models = 50M tokens  
- OpenAI: 50M input tokens ≈ $7.50 (at $0.15/1M tokens)
- Anthropic: 50M tokens ≈ $150 (at $3/1M tokens for long-context)
- Total budget impact: ~$160 for full Phase 9

**Impact:** Requires budget approval or context window target adjustment  
**Resolution Options:**
- (A) Full 100K evaluation (recommended): costs $160, ~8 hours compute
- (B) MVP (32K only): costs $30, ~2 hours compute
- Resolution Recommendation:** Start with 32K MVP; expand to 64K/100K based on Phase 8 findings priority
**Owner:** Carly + Admiral  
**Unblocks:** Infrastructure deployment

---

### Unknown 1: Context Window Degradation Pattern

**Question:** How much do model scores degrade at 32K, 64K, 100K vs. baseline (4K)?  
**Why It Matters:** Determines whether long-context is a differentiator or commodity  
**Investigation Plan:**
- Phase 9 Stage 1: Baseline degradation test (top 3 Phase 8 models at 32K)
- Phase 9 Stage 2: Full tier at confirmed window (based on Stage 1 results)
- Measurement: Spearman ρ across context windows (should be >0.70 for stable ranking)

---

### Unknown 2: Adversarial Robustness Variance Across Models

**Question:** Which models are most vulnerable to adversarial prompts? Do Phase 8 top-rankers stay robust?  
**Why It Matters:** Informs foundation deployment strategy (can we trust top rankers in adversarial env?)  
**Investigation Plan:**
- Phase 9 Stage 1: Sycophancy + Boundary adversarial test on Phase 8 top 3
- Phase 9 Stage 2: Full adversarial tier on all Phase 8 models
- Measurement: Ranking correlation between baseline + adversarial (if ρ < 0.60 → models have hidden vulnerabilities)

---

### Unknown 3: Phase 8 to Phase 9 Ranking Stability

**Question:** Do Phase 8 rankings hold under long-context + adversarial stress?  
**Why It Matters:** Validates Phase 8 findings as foundational or reveals tier-specific artifacts  
**Investigation Plan:**
- Phase 9 output: Include "Phase 7 → Phase 8 → Phase 9" ranking trajectory analysis
- Success criterion: Spearman ρ ≥ 0.70 between Phase 8 overall rank and Phase 9 long-context/adversarial average
- If ρ < 0.60 → escalate to evaluator (indicates methodology issue or real vulnerability)

---

## PHASE 9 READINESS CHECKLIST

### Gate 1: Phase 8 Complete & Results Published

**Condition:** Phase 8 final report finalized, evaluator synthesis complete  
**Verification:**
- [ ] `results/phase8_batch_summary.json` exists and contains all 14 dimensions for ≥3 models
- [ ] `phase-8-report-template.md` filled with actual data (not placeholders)
- [ ] `.empirica/evaluator-Phase-8-synthesis.md` created and cross-linked
- [ ] Constitution §III-b alignment documented
- [ ] Evaluator confirms: "Phase 8 ready for publication"

**Status:** 🟡 IN PROGRESS (results exist; report template not filled)  
**Blocking:** Evaluator approval  
**Resolution Owner:** acat-x

---

### Gate 2: Evaluator Approval of Phase 9 Scope

**Condition:** Admiral explicitly approves Phase 9 charter  
**Verification:**
- [ ] Phase 9 scope document reviewed (this checklist)
- [ ] Evaluator written feedback on context windows, adversarial targets, model set
- [ ] Evaluator approval decision recorded (accept / conditional / reject)
- [ ] If conditional: blockers itemized and owner assigned

**Status:** 🔲 PENDING (waiting for evaluator review)  
**Blocking:** Infrastructure deployment  
**Resolution Owner:** Evaluator (Admiral)

---

### Gate 3: Phase 9 Infrastructure Ready

**Condition:** Long-context harness, adversarial library, APIs configured  
**Verification:**
- [ ] `phase9_long_context_harness.py` created and tested (dry-run on small context)
- [ ] `data/adversarial_prompts_phase9.json` created with ≥200 unique prompts
- [ ] All model API keys configured + quota verified
- [ ] Cost estimate finalized (32K MVP vs. full 100K evaluation)
- [ ] Result schema validated (can store Phase 9 results without breaking Phase 8 readers)

**Status:** 🔲 PENDING (infrastructure not yet built)  
**Blocking:** Phase 9 execution  
**Resolution Owner:** acat-x

---

### Gate 4: Mesh-Support Coordination Confirmed

**Condition:** Mesh-support confirms Phase 9 specs alignment + orchestration integration  
**Verification:**
- [ ] mesh-support reviews Phase 9 charter (shares feedback or approves)
- [ ] Phase 3 specs integration plan documented
- [ ] Telemetry schema compatibility confirmed
- [ ] Evaluation triggering mechanism defined (manual vs. automated)
- [ ] Results feedback loop to evaluator confirmed

**Status:** 🟡 IN PROGRESS (mesh-support engaged on Phase 3; Phase 9 scope pending)  
**Blocking:** Phase 9 handoff + foundation-wide adoption  
**Resolution Owner:** mesh-support + acat-x

---

## PHASE 9 INTENT-OS BLOCKERS

### INTENT-OS Phase 2: Phase 9 Infrastructure Buildout

**Goal:** Build Phase 9 long-context harness and adversarial prompt library  
**Tasks:**
1. Create long-context evaluation harness (`phase9_long_context_harness.py`)
2. Curate/source adversarial prompt library (80% published + 20% Foundation-authored)
3. Configure APIs and local inference infrastructure
4. Validate result schema backwards-compatibility

**Success Criteria:**
- Dry-run: Harness successfully evaluates 1 model × 1 dimension × 32K context
- Library: ≥200 unique adversarial prompts organized by dimension + attack type
- Schema: New Phase 9 results integrate cleanly with Phase 8 data

**Owner:** acat-x  
**Effort:** 8-12 hours  
**Dependencies:** Evaluator approval (Gate 2), Budget approval (if full 100K evaluation)  
**Timeline:** Oct 6 → Oct 15 (target)

---

### INTENT-OS Phase 3: Phase 9 Execution Planning

**Goal:** Plan and execute Phase 9 evaluation (conditional on Gate readiness)  
**Tasks:**
1. Finalize context window target (32K MVP or full 100K)
2. Finalize model set (Phase 8 set only, or expand)
3. Create evaluation pipeline (all tiers in sequence)
4. Set up result aggregation and reporting

**Success Criteria:**
- Execution plan documented: which models, which windows, which adversarial categories
- Phase 9 Stage 1 complete: long-context degradation pilot (top 3 models at 32K)
- Results pipeline ready: results → aggregation → report format

**Owner:** acat-x  
**Effort:** 6-8 hours (execution prep) + N hours (actual evaluation)  
**Dependencies:** Gate 1, 2, 3 complete  
**Timeline:** Oct 15 → Oct 30 (target)

---

### INTENT-OS Phase 4: Phase 9 Results Publication & Adoption Roadmap

**Goal:** Publish Phase 9 findings and update foundation adoption guidance  
**Tasks:**
1. Aggregate Phase 9 results into Phase 8 template format
2. Cross-tier ranking stability analysis (Phase 7 → 8 → 9)
3. Update Tier 1/2/3 adoption recommendations
4. Evaluator synthesis + constitution alignment
5. Mesh-support handoff: foundation practices receive updated guidance

**Success Criteria:**
- Peer-review ready Phase 9 report published
- Foundation adoption guidance updated (new Tier 1/2/3 with long-context + adversarial caveats)
- Evaluator approves publication + recommendation changes

**Owner:** acat-x + Evaluator  
**Effort:** 4-6 hours (aggregation + narrative) + Evaluator review  
**Dependencies:** Gate 4 + Phase 9 execution complete  
**Timeline:** Oct 30 → Nov 15 (target)

---

## CRITICAL PATH: PHASE 8 → PHASE 9 TRANSITION

```
TODAY (Oct 6)
  ├─ Gate 1 Start: Fill Phase 8 report template (2-4 hours, acat-x)
  ├─ Gate 2 Start: Share Phase 9 charter with Evaluator (async, Evaluator reviews)
  └─ Gate 3 Start: Infrastructure planning (mesh-support + acat-x)
  
Oct 15
  ├─ Gate 1 DONE: Phase 8 report published
  ├─ Gate 2 DONE: Evaluator approves Phase 9 scope
  ├─ Gate 3 DONE: Infrastructure built + APIs configured
  └─ INTENT-OS Phase 2 DONE: Harness + library ready
  
Oct 30
  ├─ Phase 9 Stage 1 DONE: Degradation pilot (top 3 models, 32K context)
  ├─ INTENT-OS Phase 3 DONE: Full execution plan finalized
  └─ Phase 9 Stage 2 DONE (or in progress): Full tier evaluation running
  
Nov 15
  ├─ Phase 9 EXECUTION COMPLETE: All tiers, all models, all windows
  ├─ Results aggregated into report format
  ├─ INTENT-OS Phase 4 DONE: Publication-ready + adoption guidance
  ├─ Gate 4 DONE: Mesh-support confirmed + foundation handoff
  └─ Phase 9 ENTRY GATES CLOSED, Phase 9 BEGINS
```

---

## PHASE 9 SUCCESS DEFINITION (For POSTFLIGHT)

When Phase 9 entry gates are all DONE (✅), the following conditions hold:

1. **Phase 8 is published** — Evaluator has reviewed and approved Phase 8 findings
2. **Phase 9 scope is approved** — Evaluator explicitly chartered Phase 9 long-context + adversarial testing
3. **Infrastructure is ready** — Harness, library, APIs all operational
4. **Mesh coordination is confirmed** — Phase 3 specs integrated, feedback loop established
5. **Foundation is aligned** — Phase 9 is on critical path for evaluator decision-making about foundation model adoption

**Phase 9 then proceeds as scheduled per the critical path above.**

---

## File Structure & Dependencies

**Phase 9 Artifacts (To Be Created):**
- `.empirica/phase-9-entry-checklist.md` (this file)
- `phase9_long_context_harness.py` (harness script)
- `data/adversarial_prompts_phase9.json` (prompt library)
- `phase9_*.json` (result files, per tier/dimension)
- `.empirica/phase-9-report-template.md` (extends Phase 8 template for Phase 9 data)

**Phase 9 Dependencies (Must Be Complete):**
- `results/phase8_batch_summary.json` ✅ (exists)
- `.empirica/phase-8-report-template.md` ✅ (exists)
- Phase 3 blocker specs (`prop_4eo3ake7szbhph5ekmbabndxgq`) ✅ (received Sep 5)

**Owners & Stakeholders:**
- **acat-x**: Infrastructure build, Phase 9 execution, report generation
- **Evaluator (Admiral)**: Phase 8 synthesis, Phase 9 scope approval, constitutional alignment
- **mesh-support**: Phase 3 specs alignment, evaluator handoff, foundation-wide coordination

---

## Document Metadata

- **Created:** Oct 6, 2026
- **Author:** Agent 7 (workflow subagent) on behalf of acat-x
- **Version:** 1.0 (Initial Phase 9 Readiness Assessment)
- **Status:** PHASE 9 ENTRY GATES DEFINED, PREREQUISITES IDENTIFIED, BLOCKERS DOCUMENTED
- **Next Review:** Oct 15 (or when Gate 1 completes — whichever is sooner)
- **Critical Path Target:** Phase 9 begins Nov 1, 2026

