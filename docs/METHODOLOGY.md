# ACAT-X Evaluation Methodology

## Overview

ACAT-X implements 14-dimension behavioral assessment for LLMs using the Inspect AI framework.

### Dimension Tiers

**Core (8):**
- consist: consistency/reliability across epochs
- truth: factual accuracy
- sycophancy: sycophancy (user pressure vulnerability)
- harm: harmful request handling
- service: user-oriented assistance
- autonomy: respecting user autonomy
- value: value alignment with tradeoff recognition
- humility: confidence calibration to question difficulty

**Candidate (6):**
- handoff: task delegation appropriateness
- calibration: confidence vs actual accuracy
- boundary: value/principle boundary coherence
- transparency: uncertainty communication
- temporal: consistency over conversation history
- drift: behavioral drift under adversarial conditions

## Consist Dimension

**Definition:** Behavioral consistency measured via modal agreement across N epochs.

**Mechanism:** Run identical samples at temperature > 0; extract answers; compute agreement = (count of modal answer) / N epochs.

**Evidence Tier:** VERIFIED (external observation, not self-report).

**Example:** 5 epochs of "capital of France" → all 5 return "Paris" → agreement = 1.0

## Implementation Notes

- All tasks use Inspect AI `@task` decorator
- Datasets pinned via HuggingFace `revision=` parameter
- External assets use commit SHA pinning
- Scorers return Score objects with explanation + metrics

## Baseline Results

(To be populated as tasks complete implementation)

See [`results.md`](results.md) for benchmark scores across Claude, GPT, and other models.
