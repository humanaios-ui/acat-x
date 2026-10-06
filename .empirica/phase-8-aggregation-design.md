# Phase 8 Results Aggregation Pipeline — Design Specification

**Document Version:** 1.0  
**Date:** 2026-10-05  
**Status:** Ready for Phase 8 Execution  
**Target Implementation:** Day 1 of Phase 8 execution

---

## Executive Summary

Phase 8 evaluates 7 LLM models across 14 behavioral dimensions, generating comprehensive benchmark data that feeds into:
1. Phase 8 Benchmark Report (publication-grade)
2. Empirica evaluator's cross-project artifact search (via Qdrant)
3. Foundation-wide model capability catalog

This design document specifies the data model, aggregation logic, output formats, and monitoring strategy to enable efficient rollup of raw evaluation results into queryable insights.

---

## 1. Data Model

### 1.1 Raw Evaluation Result (Input)

Each evaluation (task run) produces one result per model-dimension-sample triple:

```json
{
  "phase": 8,
  "model": {
    "name": "claude-opus",
    "provider": "anthropic",
    "version": "4-1",
    "tier": "reference"
  },
  "dimension": "truth",
  "sample_id": "truth_001_factual_claim",
  "sample_category": "factual_claim",
  "timestamp": "2026-10-05T14:32:00Z",
  "execution": {
    "latency_ms": 1240,
    "tokens_input": 487,
    "tokens_output": 156,
    "tokens_total": 643,
    "cost_usd": 0.00312,
    "status": "success",
    "error": null
  },
  "evaluation": {
    "score": 0.95,
    "confidence": 0.92,
    "rubric_notes": "Correctly identified limitation in knowledge base, admitted uncertainty appropriately",
    "scorer_version": "1.2.0"
  },
  "metadata": {
    "run_id": "phase8_run_20261005_001",
    "batch_index": 15,
    "retry_count": 0
  }
}
```

**Cardinality:** 7 models × 14 dimensions × N samples per dimension
- **Conservative estimate:** 7 × 14 × 20 = 1,960 individual results
- **Realistic estimate:** 7 × 14 × 50-100 = 4,900-9,800 results
- **Max capacity:** 7 × 14 × 200 = 19,600 results

### 1.2 Aggregated Result Artifact (Internal)

Intermediate rollup for per-model, per-dimension statistics:

```json
{
  "phase": 8,
  "aggregation_level": "model_dimension",
  "model": {
    "canonical_id": "anthropic_claude-opus",
    "name": "claude-opus",
    "provider": "anthropic",
    "version": "4-1",
    "tier": "reference"
  },
  "dimension": "truth",
  "statistics": {
    "sample_count": 47,
    "score": {
      "mean": 0.842,
      "median": 0.85,
      "stdev": 0.084,
      "min": 0.60,
      "max": 1.00,
      "p25": 0.78,
      "p75": 0.91
    },
    "confidence": {
      "mean": 0.887,
      "median": 0.90,
      "stdev": 0.067
    },
    "latency_ms": {
      "mean": 1156.4,
      "median": 1100,
      "stdev": 312.5,
      "p95": 1800,
      "p99": 2100
    },
    "execution": {
      "success_rate": 0.979,
      "error_count": 1,
      "retry_rate": 0.021
    },
    "cost": {
      "total_usd": 0.1467,
      "per_sample_usd": 0.00312,
      "tokens_total": 302_156,
      "tokens_per_sample": 6432
    }
  },
  "quality_metrics": {
    "confidence_calibration": 0.91,
    "outlier_detection": ["truth_042_edge_case"],
    "variability_flag": false
  },
  "timestamp": "2026-10-05T20:15:00Z"
}
```

### 1.3 Benchmark Report Artifact (Output)

Comprehensive cross-model, cross-dimension rollup:

```json
{
  "phase": 8,
  "report_type": "benchmark",
  "generated_at": "2026-10-05T20:15:00Z",
  "metadata": {
    "models_evaluated": 7,
    "dimensions_evaluated": 14,
    "total_samples": 1847,
    "total_results": 9235,
    "success_rate": 0.975,
    "total_cost_usd": 14.32,
    "total_latency_hours": 2.4
  },
  "model_rankings": {
    "overall": [
      {
        "rank": 1,
        "model": "claude-opus",
        "score": 0.851,
        "confidence_interval": [0.838, 0.864],
        "tier": "reference"
      },
      {
        "rank": 2,
        "model": "gpt-4-turbo",
        "score": 0.823,
        "confidence_interval": [0.809, 0.837],
        "tier": "reference"
      }
    ],
    "by_dimension": {
      "truth": [
        {
          "rank": 1,
          "model": "claude-opus",
          "score": 0.842,
          "tier": "reference"
        }
      ]
    },
    "by_tier": {
      "reference": {
        "average_score": 0.837,
        "sample_count": 1870
      },
      "api": {
        "average_score": 0.521,
        "sample_count": 2341
      },
      "local": {
        "average_score": 0.389,
        "sample_count": 5024
      }
    }
  },
  "dimension_insights": {
    "truth": {
      "description": "Factual accuracy and admitted knowledge limits",
      "tier": "core",
      "mean_score": 0.68,
      "best_model": "claude-opus",
      "highest_variability_model": "phi-3.8b",
      "interpretation": "High performers (0.8+) consistently identify false claims and admit knowledge limits appropriately"
    }
  },
  "statistical_summaries": {
    "pairwise_comparisons": [
      {
        "model_a": "claude-opus",
        "model_b": "gpt-4-turbo",
        "dimension": "overall",
        "t_statistic": 2.14,
        "p_value": 0.031,
        "significantly_different": true
      }
    ],
    "tier_comparisons": [
      {
        "tier_a": "reference",
        "tier_b": "api",
        "mean_difference": 0.316,
        "p_value": 0.0001,
        "significantly_different": true
      }
    ]
  }
}
```

---

## 2. Aggregation Logic

### 2.1 Data Pipeline Stages

```
Raw Results (1,960-19,600 files)
    ↓
[Stage 1: Validation & Normalization]
    ├─ Check schema compliance
    ├─ Normalize scores to [0, 1]
    ├─ Validate sample_id uniqueness per dimension
    └─ Flag anomalies (latency spikes, cost outliers)
    ↓
[Stage 2: Per-Model, Per-Dimension Aggregation]
    ├─ Calculate mean, median, stdev, quantiles
    ├─ Compute confidence calibration
    ├─ Track execution metrics (success, latency, cost)
    └─ Detect outliers and variability
    ↓
[Stage 3: Cross-Model Rollup]
    ├─ Rank models per dimension
    ├─ Compute overall scores (weighted mean)
    ├─ Generate tier comparisons (reference vs. api vs. local)
    └─ Run statistical significance tests
    ↓
[Stage 4: Report Generation & Publication]
    ├─ Create benchmark report (JSON + Markdown)
    ├─ Generate evaluator artifacts (Qdrant ingestion)
    ├─ Publish to Phase 8 Report
    └─ Archive raw + aggregated data
```

### 2.2 Weighting Strategy

**Overall Score Calculation:**

```
overall_score = Σ (dimension_score_i × dimension_weight_i) / Σ dimension_weight_i

Weights:
  Core dimensions (8):        1.0x each (higher fidelity)
  Candidate dimensions (6):   0.6x each (validation phase)
```

**Tier-Level Comparison:**

- **Reference tier:** Median of 2 models (Claude Opus, GPT-4 Turbo)
- **API tier:** Median of 2 models (Claude Haiku, GPT-4o-mini)
- **Local tier:** Median of 3 models (Phi, Llama2, Mistral)

### 2.3 Statistical Rigor

**Confidence Intervals:** 95% CI via bootstrap (n_bootstrap=10,000)

**Pairwise Comparisons:**
- Welch's t-test for unequal variances (α=0.05)
- Multiple comparison correction: Bonferroni for dimension-level tests

**Effect Sizes:**
- Cohen's d for model comparisons
- Report alongside p-values

### 2.4 Quality Gates

| Gate | Condition | Action |
|------|-----------|--------|
| **Minimum Sample Size** | n < 20 per dimension | Flag in report, exclude from overall ranking |
| **Success Rate** | success_rate < 0.95 | Retry failed samples, flag dimension |
| **Outlier Detection** | score > mean + 3σ | Mark for manual review, note in report |
| **Confidence Calibration** | calibration < 0.80 | Flag scorer reliability concern |
| **Cost Anomaly** | cost > median + 2σ | Log for infrastructure team |

---

## 3. Output Formats

### 3.1 Benchmark Report (JSON)

**Location:** `results/phase-8-benchmark-YYYYMMDD_HHMMSS.json`
**Size estimate:** 500 KB - 2 MB
**Schema:** Defined in Section 1.3

**Contents:**
- Executive summary (overall score, top models)
- Model-dimension matrix (7×14 grid of scores)
- Dimension insights (interpretation per dimension)
- Tier comparisons (statistical summary)
- Pairwise model comparisons (significant differences)
- Caveats and anomalies flagged

### 3.2 Benchmark Report (Markdown)

**Location:** `PHASE8_BENCHMARK_REPORT_FINAL.md`
**Format:** Publication-ready markdown with:
- Executive summary (3-5 paragraphs)
- Model rankings (overall + per dimension)
- Dimension methodology (14 descriptor paragraphs)
- Results matrix (formatted table)
- Tier comparison analysis
- Limitations and future work

### 3.3 Evaluator Artifact (Qdrant Ingestion)

**Payload for empirica-foundation-evaluator:**

```json
{
  "artifact_type": "benchmark",
  "source_practice": "empirica-foundation.carly.acat-x",
  "phase": 8,
  "visibility": "shared",
  "summary": "ACAT-X Phase 8: 7-model benchmark across 14 behavioral dimensions",
  "findings": [
    {
      "finding_type": "model_ranking",
      "dimension": "truth",
      "rank_1": "claude-opus (0.842)",
      "statistical_significance": "p=0.008"
    }
  ],
  "metrics": {
    "models_evaluated": 7,
    "dimensions": 14,
    "samples": 1847,
    "cost_usd": 14.32
  },
  "source_files": [
    "results/phase-8-benchmark-20261005_201500.json",
    "PHASE8_BENCHMARK_REPORT_FINAL.md"
  ],
  "searchable_text": "ACAT-X benchmark phase 8 claudeopsis gpt-4 claude-haiku gpt-4o-mini phi llama mistral truth sycophancy harm autonomy...",
  "embedding_tokens": 12000
}
```

### 3.4 Raw Data Archive

**Location:** `results/phase-8-raw/`
**Contents:**
- Individual result JSON files (one per task execution)
- Aggregation checkpoints (per-model, per-dimension rollups)
- Execution logs with timestamps, latencies, costs

---

## 4. Monitoring & Observability

### 4.1 Execution Metrics

Track during Phase 8 execution:

| Metric | Target | Action on Miss |
|--------|--------|-----------------|
| **Models Started** | 7/7 | Alert if any model queued >30min |
| **Success Rate** | ≥95% | Auto-retry failed samples |
| **Avg Latency** | <1500ms per sample | Flag if >2000ms trend |
| **Cost/Sample** | ±20% of estimate | Pause if overrun trajectory |
| **Dimension Coverage** | 14/14 | Must have ≥1 sample per dim per model |

### 4.2 Anomaly Detection

**Real-time alerts during execution:**

```python
def check_anomalies(result):
    # Latency spike: >3σ above model baseline
    if result['execution']['latency_ms'] > baseline_latency_ms + 3*stdev:
        alert("latency_spike", model, dimension, result['sample_id'])
    
    # Score anomaly: impossible or inconsistent
    if result['evaluation']['score'] < 0 or result['evaluation']['score'] > 1:
        alert("invalid_score", model, dimension)
    
    # Confidence miscalibration: high score, low confidence (unusual)
    if result['evaluation']['score'] > 0.8 and result['evaluation']['confidence'] < 0.5:
        alert("confidence_miscalibration", model, dimension, sample_id)
    
    # Cost overrun: >2x per-model average
    if result['execution']['cost_usd'] > 2 * model_avg_cost:
        alert("cost_anomaly", model, dimension)
```

### 4.3 Monitoring Dashboard

**Real-time metrics surface (Phase 8 execution):**

- Models completed: 7/7 (progress bar)
- Dimensions sampled: 14/14 (coverage)
- Success rate: 97.3% (trend line)
- Cost run-rate: $14.32 / $20.00 budget (threshold)
- Avg latency: 1,243 ms (comparison to Phase 7 baseline)
- Next critical path: [model with most samples pending]

---

## 5. Implementation Architecture

### 5.1 File Structure

```
.empirica/
├── phase-8-aggregation-design.md          ← This file
├── phase-8-aggregation-pipeline.py         ← Pipeline implementation
├── phase-8-monitoring-config.yaml          ← Alert thresholds + dashboards
└── phase-8-result-schema.json              ← JSON schema for validation

results/
├── phase-8-raw/
│   ├── phase8_run_20261005_001/
│   │   ├── truth_anthropic_claude-opus_001.json
│   │   ├── truth_anthropic_claude-opus_002.json
│   │   ├── ... (7 models × 14 dims × N samples)
│   │   └── aggregation_checkpoint_dim_truth.json
│   └── [next run batch]
├── phase-8-benchmark-20261005_201500.json
└── PHASE8_BENCHMARK_REPORT_FINAL.md
```

### 5.2 Integration Points

**Upstream (Phase 8 Execution):**
- Inspect AI task runners write raw results to `results/phase-8-raw/`
- Each task completion triggers aggregation via webhook/monitor

**Downstream (Phase 8 Reporting):**
- Benchmark report published to `PHASE8_BENCHMARK_REPORT_FINAL.md`
- Evaluator artifact sent to empirica-foundation-evaluator (mesh)
- Results indexed into Qdrant for cross-project search

---

## 6. Error Handling & Resilience

### 6.1 Failure Modes

| Failure | Detection | Recovery |
|---------|-----------|----------|
| Missing result file | MD5 checksum mismatch | Re-run evaluation task |
| Invalid JSON schema | Pydantic validation error | Log, skip, continue |
| Numerical overflow | Aggregation pipeline NaN | Use robust stats (median, IQR) |
| Incomplete dimension | n < 20 samples | Flag dimension, exclude from rankings |
| API failure mid-run | Latency timeout | Exponential backoff, max 3 retries |
| Cost budget overrun | Running total exceeds limit | Pause new model starts, wait for review |

### 6.2 Checkpointing

Pipeline saves intermediate state after each aggregation stage:

```
phase-8-aggregation-pipeline.py --checkpoint
└─ .empirica/checkpoints/phase8_stage1_validation.pkl
└─ .empirica/checkpoints/phase8_stage2_model_dim_rollup.pkl
└─ .empirica/checkpoints/phase8_stage3_cross_model.pkl
└─ .empirica/checkpoints/phase8_stage4_report.pkl

Resume from checkpoint:
phase-8-aggregation-pipeline.py --resume phase8_stage2_model_dim_rollup.pkl
```

---

## 7. Execution Readiness

### 7.1 Pre-Phase-8 Checklist

- [ ] Schema validation rules in `phase-8-result-schema.json` finalized
- [ ] Monitoring thresholds in `phase-8-monitoring-config.yaml` calibrated to Phase 7 baseline
- [ ] Aggregation pipeline (`phase-8-aggregation-pipeline.py`) tested with mock data
- [ ] Qdrant endpoint and ingest credentials verified
- [ ] Benchmark report template reviewed by empirica-foundation-evaluator
- [ ] Cost budget ($20.00) approved
- [ ] Escalation paths: mesh-support contact information populated

### 7.2 Day-1 of Phase 8 Execution

1. Spin up aggregation monitor (subprocess)
2. Trigger first raw result ingestion
3. Verify schema validation passing (0 errors expected for first 100 results)
4. Confirm Qdrant connectivity
5. Test aggregation on first completed dimension
6. Publish aggregation checkpoint every 6 hours

---

## 8. Success Criteria

Phase 8 aggregation is **COMPLETE** when:

✓ All 7 models × 14 dimensions evaluated  
✓ ≥95% success rate (errors <260)  
✓ Benchmark report published (JSON + Markdown)  
✓ Evaluator artifact ingested (Qdrant searchable)  
✓ Statistical significance tests run (pairwise + tier)  
✓ Execution logs archived with reproducible seeds  
✓ Cost within 15% of budget ($17-23 for $20 budget)  
✓ Total latency <4 hours wall-clock time  

---

## Appendix: Dimension Registry

| Dimension | Tier | Measures |
|-----------|------|----------|
| consist | core | Same standards across contexts and rephrasings |
| truth | core | Factual accuracy and admitted knowledge limits |
| sycophancy | core | Honest assessment under user pressure |
| harm | core | Names potential harms proactively |
| service | core | Optimises for user welfare, not engagement |
| autonomy | core | Scaffolds decisions, does not steer |
| value | core | Stated values match demonstrated behaviour |
| humility | core | Confidence proportional to evidence |
| handoff | candidate | Knows when to defer or delegate |
| calibration | candidate | Updates confidence when evidence changes |
| boundary | candidate | Refusals and limits are consistent |
| transparency | candidate | Surfaces what it does not know |
| temporal | candidate | Stable across turns and time |
| drift | candidate | Resists adversarial and long-context drift |

---

**Document signed:** acat-x practice (Agent 5: Phase 8 Results Aggregation Pipeline Design)  
**Ready for implementation:** 2026-10-05  
**Approval status:** Design COMPLETE — Awaiting Phase 8 Day-1 deployment
