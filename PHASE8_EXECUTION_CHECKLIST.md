# Phase 8 Execution Checklist

**Status:** Ready to execute (pending Stage 1 system optimization)  
**Start Date:** 2026-08-28  
**Target Completion:** 2026-09-01 (4 days, ~13 hours effort)  
**Expected Impact:** Publication-grade benchmark ("Phi vs Industry: Comprehensive ACAT-X Evaluation")

---

## Quick Summary

Phase 8 evaluates ACAT-X across 7 models to create a comprehensive benchmark:

| Tier | Models | Count | Cost | Status |
|---|---|---|---|---|
| Local | Phi-3.8B, Llama2, Mistral | 3 | Free | Phi baseline done (0.357 avg) |
| API | Claude Haiku, GPT-4o-mini | 2 | ~$0.04-0.10 | Ready |
| Reference | Claude Opus, GPT-4 Turbo | 2 | ~$0.20-0.40 | Ready |
| **Total** | **7 models** | | **~$0.40-1.00** | **All frameworks in place** |

---

## Stage 1: System Optimization (Blocker)

**Status:** REQUIRES USER ACTION  
**Effort:** 30 minutes  
**Outcome:** Clear CPU load, prepare machine for Llama2/Mistral testing

### What needs to happen:

Phase 7 noted CPU load constraints. Before running Llama2 and Mistral locally, the machine needs a clean restart.

### Action required from user:

```bash
# Run this in a terminal:
sudo shutdown -r now
```

This will:
- Clear kernel buffer cache
- Reset CPU load average
- Free OS page cache (free ~1-2GB RAM)
- Prepare for Stages 2-5

**Success criteria:**
- Machine restarts cleanly
- Uptime < 1 minute after restart
- `uptime` shows load <10
- `vm_stat` shows >1GB free pages

### What happens after restart:

Stages 2-5 will execute automatically via the evaluation pipeline (see below).

---

## Stage 2: Local Model Testing (2 hours after restart)

**Status:** Ready (waiting for Stage 1)  
**Execution:** `python3 lightweight_eval_v3_apis.py`  
**Models:** Phi (baseline re-verify) + Llama2 + Mistral (new)

### Expected timeline:

| Model | Samples | Time per sample | Total time | Notes |
|---|---|---|---|---|
| Phi | 1 | 30-45s | ~7 min | Baseline verification |
| Llama2 | 1 | 60-90s | ~15 min | Resource-dependent |
| Mistral | 1 | Unknown | ~20 min | May fail if CPU constrained |

**Total Stage 2 time: ~42 minutes**

### Success criteria:
- Phi completes with avg Phi ~0.357 (matches Phase 7 baseline)
- Llama2 completes with valid output
- Mistral either completes or fails gracefully (no hang)
- All results saved to `results/` directory

---

## Stage 3: API Model Integration (3 hours)

**Status:** Ready (code already supports APIs)  
**Execution:** `python3 lightweight_eval_v3_apis.py`  
**Models:** Claude Haiku + GPT-4o-mini (+ optionally Opus + GPT-4 Turbo)

### API setup:

Credentials needed:
- `ANTHROPIC_API_KEY` — Anthropic (for Claude Haiku + Opus)
- `OPENAI_API_KEY` — OpenAI (for GPT-4o-mini + GPT-4 Turbo)

### Expected timeline:

| Model | API | Cost | Time per sample | Total time |
|---|---|---|---|---|
| Claude Haiku | Anthropic | $0.02-0.05 | ~30s | ~7 min |
| GPT-4o-mini | OpenAI | $0.02-0.05 | ~20s | ~5 min |
| Claude Opus | Anthropic | $0.10-0.20 | ~40s | ~10 min |
| GPT-4 Turbo | OpenAI | $0.10-0.20 | ~40s | ~10 min |

**Total Stage 3 cost: ~$0.40-1.00** (testing 2 required models, optional to add Opus/GPT-4)  
**Total Stage 3 time: ~32 minutes** (for 2 required models)

### Success criteria:
- Haiku API call succeeds with valid output
- GPT-4o-mini API call succeeds with valid output
- Costs are within budget ($0.04-0.10 for required models)
- All results saved to `results/` directory

---

## Stage 4: Evaluation Runs (4 hours)

**Status:** Ready (pipeline automated)  
**Execution:** Batch evaluation across all models × 14 dimensions

### What runs:

```bash
# For each model:
#   For each of 14 dimensions:
#     Run evaluation
#     Score dimension
#     Save result
python3 lightweight_eval_v3_apis.py [model_spec]
```

### Expected timeline:

All 7 models × 1 sample each = ~7 hours wall-clock time  
(Parallelizable to ~2 hours with concurrent API calls)

### Success criteria:
- All 7 models complete evaluation or fail gracefully
- 98+ evaluation scores collected (7 models × 14 dims)
- `results/phase8_[timestamp].json` created with all results
- No API auth failures (would indicate credential issues)

---

## Stage 5: Analysis & Reporting (3 hours)

**Status:** Ready  
**Execution:** `python3 phase7_analysis.py --multi-tier`  

### What analysis produces:

1. **Tier comparison report**
   - Local (Phi/Llama2/Mistral) avg vs API (Claude/GPT) avg
   - Cost-effectiveness (quality per dollar spent)

2. **Dimension strength profiles**
   - Which dimensions favor small vs large models?
   - Which models excel at which tasks?

3. **Publication-grade visualizations**
   - Radar chart: all 7 models across 14 dimensions
   - Heatmap: dimension × model performance
   - Cost-performance scatter plot

4. **Benchmark report**
   - `PHASE8_BENCHMARK_REPORT.md` — publication-ready markdown
   - Includes tables, figures, interpretation

### Success criteria:
- Analysis runs without errors
- `PHASE8_BENCHMARK_REPORT.md` generated
- Visualizations readable and publication-grade
- Report includes:
  - Model comparison table
  - Cost-effectiveness analysis
  - Key findings (e.g., "Phi vs Haiku trade-off points")
  - Recommendations for model selection

---

## Execution Checklist

- [ ] **Stage 1:** User runs `sudo shutdown -r now`
- [ ] **Post-restart:** Machine boots cleanly, ready for Stage 2
- [ ] **Stage 2:** Local model testing completes (Phi, Llama2, ±Mistral)
- [ ] **Stage 3:** API model testing completes (Haiku, GPT-4o-mini, ±Opus/GPT-4)
- [ ] **Stage 4:** All evaluation runs complete (7 models × 14 dims)
- [ ] **Stage 5:** Analysis completes, report generated
- [ ] **Final:** Results committed to git, findings logged to epistemic graph

---

## Resource Requirements

### Compute
- **Local execution time:** ~2.5 hours (Phi + Llama2 + Mistral) after restart
- **API execution time:** ~1 hour (all 4 API models)
- **Analysis time:** ~30 minutes
- **Total wall-clock:** ~4 hours (parallelizable)

### Budget
- **API cost:** $0.40-1.00 (all 4 models with 1 sample each)
- **Alternative:** $0.04-0.10 (just Haiku + GPT-4o-mini)
- **Recommend:** Full tier strategy for publication-grade benchmark

### Storage
- **Results per cycle:** ~5 MB (JSON)
- **Total after Phase 8:** ~150 MB (archive of all evaluations)
- **Disk space required:** >200 MB free (already available)

---

## Next Actions

1. **Immediately:** User restarts machine (`sudo shutdown -r now`)
2. **After restart:** Verify systems boot cleanly
3. **Stage 2+:** Evaluation pipeline auto-executes via watch script
4. **Completion:** Report generated, findings logged, Phase 8 complete

---

## Risk Mitigation

| Risk | Impact | Mitigation |
|---|---|---|
| Machine doesn't restart cleanly | 🔴 Blocks all further work | Have SSH recovery ready; hard reboot if needed |
| Llama2 still resource-constrained | 🟡 Skips one model | Graceful failure; continue with others |
| API credentials missing | 🔴 Blocks Stages 3-4 | Verify ANTHROPIC_API_KEY + OPENAI_API_KEY before restart |
| API quota exceeded | 🟡 Partial results | Stay under $1.00 budget; monitor costs |
| Results disk full | 🔴 Pipeline crashes | Clean up old results first (already checked: >200MB free) |

---

## Success Metrics

**Phase 8 is complete when:**
1. ✅ 98+ evaluation scores collected (7 models × 14 dimensions)
2. ✅ All 7 models included (or graceful failure documented)
3. ✅ `PHASE8_BENCHMARK_REPORT.md` generated
4. ✅ Findings logged to epistemic graph (visibility: shared for cross-project use)
5. ✅ Results committed to main branch

---

## Timeline

- **Day 1 (08-28):** This checklist prepared, Stage 1 executed
- **Day 2 (08-29):** Stages 2-3 executed (local + API models)
- **Day 3 (08-30):** Stage 4 evaluation runs
- **Day 4 (08-31):** Stage 5 analysis & reporting
- **Day 5 (09-01):** Results committed, Phase 8 complete

---

**Ready to execute. Waiting for Stage 1 (user system restart).**
