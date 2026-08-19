# Phase 8: Multi-Tier Model Evaluation (API Expansion)

**Objective:** Comprehensive model benchmarking across open-source, free-trial, and paid APIs  
**Status:** Credentials verified, ready to execute  
**Expected Impact:** Publication-grade research ("Phi vs industry: comprehensive ACAT-X benchmark")

---

## Model Lineup (Tier Strategy)

### Tier 1: Small Open-Source (Local, Free)
- **Phi-3.8B** ✅ Baseline complete (14 dims, 0.357 avg)
- **Llama2-7B** — Resource-constrained in Phase 7, retry with system optimization
- **Mistral-7B** — Blocked by CPU load in Phase 7, retry Phase 8

### Tier 2: API Models (Free/Low-Cost)
- **Claude Haiku (3-5B equiv)** — Anthropic API, fresh credits
- **GPT-4o mini (8-10B equiv)** — OpenAI API, fresh credits

### Tier 3: Large Models (Paid, Reference)
- **Claude Opus (100-150B equiv)** — Anthropic API (if credits allow)
- **GPT-4 Turbo (200B+ equiv, MoE)** — OpenAI API (if credits allow)

### Tier 4: Premium/Experimental (Optional)
- **Grok-3** — X AI, TBD availability
- **Claude 5** — Announced, pending release

---

## Phase 8 Execution Plan

### Stage 1: System Optimization (Day 1, ~30 min)
```bash
# Restart machine to clear CPU load
# Target: CPU <10, free memory >1GB
sudo shutdown -r now

# Verify resources
uptime  # should show load <10
vm_stat # should show >1GB free pages
```

**Success criteria:** CPU <10, free memory >500MB

### Stage 2: Local Model Testing (Day 1-2, ~2 hours)
**Goal:** Get Llama2 + Mistral working after resource cleanup

```bash
# Test Phi (baseline already complete)
python3 lightweight_eval_v3_apis.py truth ollama/phi 1

# Test Llama2 (Phase 8 required)
python3 lightweight_eval_v3_apis.py truth ollama/llama2 1

# Test Mistral (if time, resource-dependent)
python3 lightweight_eval_v3_apis.py truth ollama/mistral 1
```

**Expected outcomes:**
- Phi: 30-45s per sample (proven)
- Llama2: 60-90s per sample (pending system state)
- Mistral: Unknown (if it loads at all)

### Stage 3: API Model Integration (Day 2-3, ~3 hours)

**Create `lightweight_eval_v3_apis_expanded.py`:**
- Extend model dispatcher to support Claude Haiku, GPT-4o-mini
- Keep same 14-dimension evaluation framework
- Minimal token usage (single-line prompts where possible)

```python
# Pseudocode
def get_model_output(model_spec, prompt):
    if model_spec.startswith("ollama/"):
        return call_ollama(...)
    elif model_spec.startswith("anthropic/"):
        return call_claude_api(...)
    elif model_spec.startswith("openai/"):
        return call_gpt_api(...)
```

**Models to test (prioritized):**
1. Claude Haiku (smallest, cheapest)
2. GPT-4o-mini (comparable to Haiku)
3. Claude Opus (reference: large model)
4. GPT-4 Turbo (reference: large model)

### Stage 4: Evaluation Runs (Day 3-4, ~4 hours)

**Sampling strategy (cost optimization):**
- **Conservative:** 1 sample per dimension per model (minimal cost)
- **Standard:** 2 samples per dimension (higher confidence)
- **Comparison:** 3 samples if credits allow

**Cost estimates (1 sample × 14 dims):**
| Model | Estimated Cost | Inference Time |
|-------|---|---|
| Phi | $0 | ~7 min |
| Llama2 | $0 | ~15 min |
| Mistral | $0 | Unknown |
| Claude Haiku | ~$0.02-0.05 | ~30s per sample |
| GPT-4o-mini | ~$0.02-0.05 | ~20s per sample |
| Claude Opus | ~$0.10-0.20 | ~40s per sample |
| GPT-4 Turbo | ~$0.10-0.20 | ~40s per sample |

**Total cost (all 7 models, 1 sample each): ~$0.40-1.00**

### Stage 5: Analysis & Reporting (Day 4-5, ~3 hours)

**Expand `phase7_analysis.py` to handle multi-tier comparison:**

```python
def analyze_multi_tier(cycle_id):
    results = get_cycle_results(cycle_id)
    
    # Group by tier
    local_models = {m: scores for m, scores in results if m.startswith("ollama/")}
    api_models = {m: scores for m, scores in results if not m.startswith("ollama/")}
    
    # Compare tiers
    local_avg = mean(all_scores(local_models))
    api_avg = mean(all_scores(api_models))
    
    # Dimension-by-dimension comparison
    for dim in DIMENSIONS:
        compare_scores_across_tiers(dim, results)
    
    return analysis
```

**Output:**
- Tier comparison report (local vs API performance)
- Cost-effectiveness analysis (quality per dollar)
- Dimension strength profiles (which tasks suit which models?)
- Publication-grade tables + visualizations

---

## Resource Requirements

### Compute
- **Local:** 3 Phi evaluations (full 14-dim runs)
  - Time: ~7 min each = 21 min
  - Disk: ~5 MB per cycle (results JSON)
- **API:** ~10-15 API calls to Anthropic + OpenAI
  - Time: ~2 minutes total
  - Cost: $0.40-1.00 total

### Storage
- Results archive: ~50 MB (28 prev results + 70-100 new)
- Database: +50-100 records (evaluation_results table)

### Credentials
- ✅ Anthropic API key: Present, fresh
- ✅ OpenAI API key: Present, fresh
- ⚠️ Grok API: Unknown (optional, can skip if unavailable)

---

## Success Criteria

✅ **Phase 8 Complete when:**
1. All local models evaluated (Phi, Llama2, ±Mistral)
2. All API models evaluated (Haiku, GPT-mini, ±Opus/Turbo)
3. Multi-tier comparison report generated
4. Cost-effectiveness analysis published
5. Publication manuscript drafted

✅ **Research deliverable:**
"ACAT-X Multi-Tier Evaluation: How Phi-3.8B Stacks Against Industry LLMs"

---

## Timeline

| Day | Task | Effort | Status |
|-----|------|--------|--------|
| 1 | System optimization | 30 min | 🔲 Pending |
| 1-2 | Local model testing | 2 hours | 🔲 Pending |
| 2-3 | API integration | 3 hours | 🔲 Pending |
| 3-4 | Evaluation runs | 4 hours | 🔲 Pending |
| 4-5 | Analysis & reporting | 3 hours | 🔲 Pending |
| **Total** | — | **~13 hours** | **🔲 Ready** |

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| API rate limits | Sample conservatively (1 sample initially) |
| API key rotation | Keys tested/verified before execution |
| Local resource failure (Llama2/Mistral) | Acceptable; focus on Phi + API models |
| Cost overrun | Monitor spending; scale down sampling if needed |
| Long evaluation time | Run API calls in parallel where possible |

---

## Phase 8 Success = Phase 9 Ready

Once complete, you'll have:
- ✅ Novel research contribution (comprehensive multi-tier benchmark)
- ✅ Publication-grade data + analysis
- ✅ Clear answer: "Where does Phi shine vs industry models?"
- ✅ Framework for ongoing model evaluation

**Next step after Phase 8:** Publication manuscript + conference submission prep.

