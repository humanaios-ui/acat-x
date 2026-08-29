# Phase 3 Telemetry Schema — Evaluator Integration

**Schema Version:** 1.0  
**Purpose:** Enable evaluator discovery and decision-making using ACAT-X artifacts  
**Status:** Designed for foundation-wide mesh coordination  

---

## Telemetry Categories

### 1. Capability Matrix
**What:** ACAT-X evaluation coverage across models and dimensions  
**Format:**
```json
{
  "capability_matrix": {
    "dimensions": ["reasoning", "coding", "writing", "math", "factuality", "consistency", "safety", "instruction_following", "calibration", "robustness", "latency", "cost", "scalability", "reliability"],
    "models": ["phi-2", "llama2-7b", "mistral-7b", "claude-haiku", "gpt-4o-mini", "claude-opus", "gpt-4-turbo"],
    "coverage": {
      "complete": ["phi-2", "llama2-7b", "mistral-7b", "claude-haiku", "gpt-4o-mini"],
      "partial": ["claude-opus", "gpt-4-turbo"],
      "pending": []
    }
  }
}
```

**Who Uses It:** Evaluator prioritization of model evaluation order  
**Artifacts Tracked:** Phase 8 benchmark results per dimension/model  

---

### 2. Reliability Findings
**What:** Per-model, per-dimension failure modes and confidence breakdowns  
**Format:**
```json
{
  "reliability_profile": {
    "model_id": "gpt-4o-mini",
    "dimension": "reasoning",
    "avg_score": 0.429,
    "confidence_interval": [0.381, 0.477],
    "sample_size": 14,
    "failure_modes": [
      {"mode": "arithmetic_errors", "frequency": "12%", "impact": "high"},
      {"mode": "logic_shortcuts", "frequency": "8%", "impact": "medium"}
    ],
    "recommendation": "Use for non-critical reasoning; requires verification for calculations"
  }
}
```

**Who Uses It:** Evaluator understands model limitations and appropriate use cases  
**Artifacts Tracked:** Phase 8 Stage 3-5 findings per model  

---

### 3. Baseline Metrics
**What:** Production pipeline performance indicators  
**Format:**
```json
{
  "baseline_metrics": {
    "accuracy": {
      "phi-2": {"aggregate": 0.45, "by_dimension": {"reasoning": 0.38, "coding": 0.52}},
      "gpt-4o-mini": {"aggregate": 0.429, "by_dimension": {"reasoning": 0.43, "coding": 0.41}}
    },
    "latency_seconds": {
      "phi-2": {"p50": 1.2, "p95": 2.1, "p99": 3.5},
      "gpt-4o-mini": {"p50": 0.8, "p95": 1.1, "p99": 1.8}
    },
    "cost_per_inference": {
      "phi-2": {"estimate": 0.0001, "source": "local_compute"},
      "gpt-4o-mini": {"estimate": 0.0015, "source": "anthropic_pricing"}
    }
  }
}
```

**Who Uses It:** Evaluator optimizes for accuracy/cost/latency tradeoffs  
**Artifacts Tracked:** Phase 6.4 production results, Phase 8 timing data  

---

### 4. Infrastructure Status
**What:** Provider availability and constraint documentation  
**Format:**
```json
{
  "infrastructure": {
    "providers": {
      "ollama": {
        "status": "operational",
        "models_available": ["phi-2", "llama2-7b", "mistral-7b"],
        "capacity": "local",
        "constraints": ["embedding_model_not_pulled", "inference_optimization_needed"]
      },
      "anthropic": {
        "status": "operational",
        "models_available": ["claude-haiku", "claude-opus"],
        "rate_limits": "active",
        "constraints": []
      }
    }
  }
}
```

**Who Uses It:** Evaluator understands infrastructure constraints for orchestration  
**Artifacts Tracked:** Phase 3a Ollama findings, Phase 8 provider status  

---

## Signal Integration Mapping

| ACAT-X Finding | Evaluator Decision Input | Why It Matters |
|---|---|---|
| Phase 8 avg score 0.429 for GPT-4o-mini | Model selection for baseline | Sets expectation for Phase 4+ performance |
| Ollama embedding model not pulled | Local compute availability | Affects inference provider selection |
| 14 ACAT-X dimensions evaluated | Evaluation breadth | Completeness of assessment |
| Phase 8 Stage 3-5 reliability data | Per-model risk assessment | Informs orchestration confidence |
| Foundation integration readiness | Mesh coordination timing | Determines Phase 4 start date |

---

## Shared Visibility Artifacts (15+ targets)

**High-Priority Findings for `--visibility shared`:**

1. **Phase 8 Benchmark Evaluation Complete** — avg score per model, dimensions covered
2. **Phase 8 Stage 3 (API Models)** — GPT-4o-mini results, 14 dimensions
3. **Phase 8 Baseline Metrics** — latency/cost/accuracy profile
4. **Phase 8 Orchestration Audit Architecture** — evaluation scaffold design
5. **Ollama API Status** — local inference provider state
6. **ACAT-X Practice Registration Valid** — mesh-active canonical addressing
7. **Foundation Governance Architecture** — schema v3.0, mesh compatibility
8. **Phase 3 Governance Audit Confirms** — schema migration status
9. **Phase 8 Coordination Mailbox Poll** — evaluator response readiness
10. **Telemetry Contract Design** — this schema + artifact structure
11. **Graph Discipline Validation** — orphan rate 0%, connectivity 1.85 edges/finding
12. **Phase 6.4 Production Pipeline** — baseline results, infrastructure ready
13. **Calibration Trajectory** — 442 observations, honest assessment
14. **Type Audit Completion** — 66 artifacts properly categorized
15. **Schema v3.0 Validation** — visibility scoping functional, edges working

---

## Evaluator Handoff Checklist

**Before evaluator integration complete:**

- ☐ Evaluator response received and analyzed
- ☐ Telemetry schema reviewed and approved
- ☐ 15+ high-impact findings re-logged with `--visibility shared`
- ☐ Canonical sources registered (framework, results, infrastructure)
- ☐ SER created if multi-round coordination needed
- ☐ Foundation orchestration map updated with ACAT-X telemetry
- ☐ Signal integration documented (findings → evaluator decision inputs)
- ☐ Mesh coordination verification complete

---

*Schema designed 2026-08-29 for Phase 3 Stage 3c evaluation integration. Ready for evaluator feedback and refinement.*
