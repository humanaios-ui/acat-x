# ACAT-X: Inspect AI Evaluation Suite

## Overview

Behavioral assessment and self-description calibration evaluation suite for large language models. ACAT-X implements the 14-dimension ACAT framework within the Inspect AI framework. Provides rigorous evaluation capability for AI behavior assessment across consistency, truthfulness, sycophancy awareness, harm awareness, service orientation, autonomy respect, value alignment, and humility.

## Identity

- **ai_id:** acat-x
- **Canonical Seat:** empirica-foundation.carly.acat-x
- **Org:** empirica-foundation
- **Tenant:** carly
- **Created:** 2026-08-15
- **Type:** Software/Research
- **Status:** Active
- **Classification:** Internal
- **Language:** Python

## Domains & Interfaces

### Owned Domains

- **AI Behavioral Assessment:** 14-dimension evaluation framework for LLM capabilities and limitations
- **Dimension Implementation:** Core (8 dimensions) + candidate (6 dimensions) evaluation tasks
- **Evaluation Framework:** Inspect AI integration, scoring, and result aggregation
- **Calibration & Scoring:** Behavioral rubric development and dimension-semantic alignment

### External Interfaces

| Partner | Protocol | SLA | Purpose |
|---|---|---|---|
| empirica-foundation-evaluator | data-feed | 24 hours | ACAT audit results, model assessments |
| empirica-analytics | propose | 24 hours | Evaluation dataset aggregation |
| humanaios | data-feed | 24 hours | Calibration feedback, dimension refinement |
| opportunity-aggregator | data-feed | 24 hours | Collaborator capability assessment data |

## SLAs

- **Response Time:** 24 hours for evaluation dataset requests
- **Availability:** 95% uptime for evaluation infrastructure
- **Escalation Path:** → empirica-foundation-evaluator for evaluation methodology disputes
- **Evaluation Turnaround:** 48 hours for single model evaluation

## Key Files

- `src/acat_x/` — Core evaluation task implementations (14 dimensions)
  - `consist.py` — Consistency evaluation
  - `truth.py` — Truthfulness assessment
  - `sycophancy.py` — Sycophancy detection
  - `harm.py` — Harm awareness evaluation
  - `service.py` — Service orientation assessment
  - `autonomy.py` — Autonomy respect evaluation
  - `value.py` — Value alignment assessment
  - `humility.py` — Humility evaluation
  - `handoff.py`, `calibration.py`, `boundary.py`, `transparency.py`, `temporal.py`, `drift.py` — Candidate dimensions
- `pyproject.toml` — Project dependencies and configuration
- `docs/` — Framework documentation and methodology papers
- `results/` — Evaluation results, benchmarks, and analysis reports
- `PHASE8_BENCHMARK_REPORT.md` — Latest benchmark and comparison results

## Getting Started

```bash
# Clone and setup
cd /Users/andersonfamily/practices/acat-x
uv sync

# Run single evaluation task
uv run inspect eval src/acat_x/consist --model anthropic/claude-opus-4-1

# Run all core dimensions (8 tasks)
uv run inspect eval-set \
  src/acat_x/consist \
  src/acat_x/truth \
  src/acat_x/sycophancy \
  src/acat_x/harm \
  src/acat_x/service \
  src/acat_x/autonomy \
  src/acat_x/value \
  src/acat_x/humility

# Run all candidate dimensions (6 tasks)
uv run inspect eval-set \
  src/acat_x/handoff \
  src/acat_x/calibration \
  src/acat_x/boundary \
  src/acat_x/transparency \
  src/acat_x/temporal \
  src/acat_x/drift

# View results
cat results/latest_benchmark.json
```

## Architecture

**ACAT-X** is built on the Inspect AI framework with these key components:

1. **14-Dimension Framework:**
   - **Core (8):** consistency, truthfulness, sycophancy, harm awareness, service orientation, autonomy respect, value alignment, humility
   - **Candidate (6):** handoff appropriateness, confidence calibration, boundary coherence, transparency, temporal consistency, adversarial robustness

2. **Evaluation Pipeline:**
   - Task definition (solver/scorer patterns)
   - Model execution
   - Result aggregation (reducer)
   - Score normalization and reporting

3. **Rigorous Scoring:**
   - Behavioral rubric scorers calibrated to dimension semantics
   - Deterministic evaluation with dataset versioning
   - Reproducible results across runs

4. **Framework Integration:**
   - Full Inspect AI compatibility
   - Support for all major model providers
   - Parallel evaluation capability

## Dependencies

**Internal (practices):**
- empirica-foundation-evaluator (audit coordination)
- empirica-analytics (dataset management)
- humanaios (calibration feedback)

**External:**
- Inspect AI framework
- Anthropic Claude API (and other model APIs)
- Python 3.9+
- PyYAML, Pydantic
- Published datasets at HuggingFace (humanaios/acat-assessments)

## Escalation

**Contact:** acat-x practice AI or Carly R. Anderson
**Escalation Path:** 
1. ACAT-X attempts resolution (24 hour SLA)
2. If evaluation methodology disputed, escalate to empirica-foundation-evaluator
3. For critical evaluation infrastructure failures, notify empirica-mesh-support

**Types of escalations:**
- Evaluation methodology challenges
- Dimension semantics clarification
- Cross-model benchmark disputes
- Dataset versioning conflicts

## Related

- [HumanAIOS Website](https://humanaios.ai) — Published methods and evaluation corpus
- [Hugging Face Dataset](https://huggingface.co/datasets/humanaios/acat-assessments) — Public evaluation datasets
- [Empirica Analytics](../empirica-analytics/README.md) — Data pipeline and corpus validation
- [Empirica Foundation Evaluator](../empirica-foundation-evaluator/README.md) — Audit coordination
- [PHASE8_BENCHMARK_REPORT.md](PHASE8_BENCHMARK_REPORT.md) — Latest benchmark results
- [Calibration Report](calibration_report.md) — Dimension calibration documentation

