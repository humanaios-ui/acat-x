# Phase 5 Deployment Guide

**Status:** 🚀 In Progress (2026-08-14)

## Phase 5 Objectives

Extend ACAT-X evaluation infrastructure to production scale with full model coverage and epistemic calibration tracking.

### Scope
- ✅ All 14 dimensions (8 core + 6 candidate)
- ✅ Multiple Ollama models (phi, mistral, llama2)
- ⏳ Claude API integration (waiting for credentials)
- ⏳ GPT-4 integration (waiting for credentials)
- ✅ Ecodex calibration tracking
- ✅ Automated benchmark pipeline

## Implementation

### Phase 5 Benchmark (Current)

```bash
# Run full evaluation suite (42 tests = 3 models × 14 dimensions × 3 samples each)
bash phase5_benchmark.sh

# Expected output:
# - 42 JSON result files in results/
# - Detailed timing information
# - Progress tracking
```

**Execution time:** ~30-40 minutes (42 evaluations × 30-60s each)

### Models Included

#### Ollama (Local) ✅
- **Phi** (1.6GB) — Reasoning, instruction following
- **Mistral** (4.4GB) — General capability
- **Llama2** (3.8GB) — Base model reference

#### Claude API ⏳
- `anthropic/claude-opus` — Waiting for ANTHROPIC_API_KEY
- `anthropic/claude-sonnet` — Waiting for ANTHROPIC_API_KEY

#### GPT-4 API ⏳
- `openai/gpt-4` — Waiting for OPENAI_API_KEY

### Dimensions Evaluated (All 14)

**Core Dimensions (8):**
1. **consist** — Behavioral consistency/reliability (modal agreement)
2. **truth** — Factual accuracy (string matching)
3. **sycophancy** — Resistance to user pressure (paired prompts)
4. **harm** — Harmful request handling (safety rubric)
5. **service** — User-oriented assistance (helpfulness)
6. **autonomy** — User autonomy respect (choice validation)
7. **value** — Value alignment (tradeoff recognition)
8. **humility** — Calibrated confidence (question difficulty matching)

**Candidate Dimensions (6):**
9. **handoff** — Task delegation appropriateness
10. **calibration** — Confidence-accuracy alignment (Brier scoring)
11. **boundary** — Value boundary coherence
12. **transparency** — Uncertainty/limitation communication
13. **temporal** — Conversation consistency across history
14. **drift** — Adversarial robustness under pressure

## Results Pipeline

### Step 1: Run Benchmark
```bash
bash phase5_benchmark.sh
# Outputs: results/lightweight_*.json (42 files)
```

### Step 2: Analyze Results
```bash
python3 analyze_results.py
# Outputs: Summary table, model rankings, dimension rankings
```

### Step 3: Integrate with Ecodex
```bash
python3 ecodex_integration.py
# Outputs: calibration_report.md
# Sends: Results to Ecodex for epistemic tracking
```

### Step 4: Launch Ecodex for Coordination
```bash
ecodex
# Opens TUI for multi-AI coordination
# Loads calibration data
# Connects to Cortex mesh
```

## Infrastructure Components

### Scripts
- **phase5_benchmark.sh** — Main benchmark runner (all 14 dims × 3 models)
- **lightweight_eval_v2.py** — Core evaluator (no framework overhead)
- **analyze_results.py** — Result aggregation and comparison
- **ecodex_integration.py** — Calibration tracking and Ecodex integration

### Output Files
- **results/lightweight_*.json** — Individual evaluation results
- **calibration_report.md** — Aggregated calibration report
- **phase5_benchmark.log** — Full benchmark log

## Adding API Models

### Claude Integration
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
python3 lightweight_eval_v2.py consist anthropic/claude-opus 3
```

### GPT-4 Integration
```bash
export OPENAI_API_KEY="sk-..."
python3 lightweight_eval_v2.py consist openai/gpt-4 3
```

Once API keys are set, expand the benchmark:
```bash
# Update phase5_benchmark.sh:
MODELS=("ollama/phi" "ollama/mistral" "ollama/llama2" \
        "anthropic/claude-opus" "openai/gpt-4")
bash phase5_benchmark.sh
```

## Ecodex Integration

### What Gets Tracked
- Model performance across all 14 dimensions
- Confidence vs. accuracy calibration
- Cross-model comparison metrics
- Temporal consistency of results

### Cortex Mesh Coordination
- Results flow to Cortex for multi-AI assessment
- Other practices can reference ACAT-X calibration
- Enables mesh-wide model evaluation coordination

## Success Criteria

✅ Complete — All 14 dimensions implemented and tested
✅ Complete — Benchmark infrastructure operational (3 models)
⏳ In Progress — Run full benchmark sweep
⏳ Ready — Integrate Claude/GPT-4 when credentials available
⏳ Ready — Ecodex calibration tracking live

## Next Phase (Phase 6)

- Advanced dimension-specific scorers (replace simple target matching)
- Multi-turn evaluation (temporal dimension expansion)
- Adversarial testing framework
- Broader model coverage (open source models)
- Publication-ready comparison reports

## Troubleshooting

### Ollama models not found
```bash
ollama pull phi
ollama pull mistral
ollama pull llama2
```

### Benchmark takes too long
- Reduce SAMPLES_PER_TEST in phase5_benchmark.sh (default: 3)
- Evaluate subset of dimensions
- Run sequential batches: one model at a time

### Missing results
Check phase5_benchmark.log for errors:
```bash
tail -100 phase5_benchmark.log
```

### Ecodex connection issues
Verify Ecodex is installed:
```bash
ecodex --version
empirica --version
```

---

**Deployment started:** 2026-08-14
**Infrastructure:** Lightweight evaluator v2 (Inspect AI-free)
**Status:** Full benchmark in progress
