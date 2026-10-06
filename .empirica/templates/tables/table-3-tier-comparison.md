# Table 3: Tier Performance Comparison & Stability

## Model Scores by Evaluation Tier

| Model | Baseline Avg | Baseline N | Adversarial Avg | Adversarial N | Long-Context Avg | Long-Context N | Tier Stability (ρ) | Ranking Shift |
|-------|--------------|------------|-----------------|---------------|------------------|----------------|--------------------|---------------|
| [MODEL_1] | 0.00 | [N] | 0.00 | [N] | 0.00 | [N] | ρ = 0.00 (very high) | [±0 positions] |
| [MODEL_2] | 0.00 | [N] | 0.00 | [N] | 0.00 | [N] | ρ = 0.00 (high) | [±0 positions] |
| [MODEL_3] | 0.00 | [N] | 0.00 | [N] | 0.00 | [N] | ρ = 0.00 (high) | [±0 positions] |
| [MODEL_4] | 0.00 | [N] | 0.00 | [N] | 0.00 | [N] | ρ = 0.00 (moderate) | [±0 positions] |
| [MODEL_5] | 0.00 | [N] | 0.00 | [N] | 0.00 | [N] | ρ = 0.00 (moderate) | [±0 positions] |
| [MODEL_6] | 0.00 | [N] | 0.00 | [N] | 0.00 | [N] | ρ = 0.00 (low) | [±0 positions] |
| [MODEL_7] | 0.00 | [N] | 0.00 | [N] | 0.00 | [N] | ρ = 0.00 (low) | [±0 positions] |

---

## Tier Stability Interpretation

**Spearman Rank Correlation (ρ):** Model ranking consistency across tiers
- **ρ ≥ 0.80:** Very high stability — model ranking preserved across all tiers
- **0.60–0.79:** High stability — consistent ranking with minor shifts
- **0.40–0.59:** Moderate stability — ranking shifts, but same general tier
- **0.20–0.39:** Low stability — substantial ranking changes across tiers
- **ρ < 0.20:** Very low stability — rankings fundamentally differ by tier (warning sign for deployment)

---

## Performance Delta by Tier (Baseline as reference = 0)

| Model | Adversarial Δ | Long-Context Δ | Interpretation |
|-------|--------------|----------------|-----------------|
| [MODEL_1] | [+0.00 or -0.00] | [+0.00 or -0.00] | [Robust / Vulnerable to adversarial / Struggles with long-context] |
| [MODEL_2] | [+0.00 or -0.00] | [+0.00 or -0.00] | [Robust / Vulnerable to adversarial / Struggles with long-context] |
| [MODEL_3] | [+0.00 or -0.00] | [+0.00 or -0.00] | [Robust / Vulnerable to adversarial / Struggles with long-context] |
| [MODEL_4] | [+0.00 or -0.00] | [+0.00 or -0.00] | [Robust / Vulnerable to adversarial / Struggles with long-context] |
| [MODEL_5] | [+0.00 or -0.00] | [+0.00 or -0.00] | [Robust / Vulnerable to adversarial / Struggles with long-context] |
| [MODEL_6] | [+0.00 or -0.00] | [+0.00 or -0.00] | [Robust / Vulnerable to adversarial / Struggles with long-context] |
| [MODEL_7] | [+0.00 or -0.00] | [+0.00 or -0.00] | [Robust / Vulnerable to adversarial / Struggles with long-context] |

**Δ > +0.10:** Model improves under adversarial/long-context conditions (confidence boost under pressure)  
**Δ between -0.10 and +0.10:** Neutral tier response  
**Δ < -0.10:** Model degrades under adversarial/long-context conditions (vulnerability indicator)

---

## Tier Breakdown by Dimension (Sample: Calibration)

### Calibration Scores Across Tiers

| Model | Baseline | Adversarial | Long-Context |
|-------|----------|-------------|--------------|
| [MODEL_1] | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| [MODEL_2] | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| [MODEL_3] | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| [MODEL_4] | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| [MODEL_5] | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| [MODEL_6] | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| [MODEL_7] | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.00 ± 0.00 |

**Interpretation:**
- [Which dimension shows highest baseline performance?]
- [Which model best maintains calibration under adversarial pressure?]
- [Long-context concern areas: low-performing dimensions]

---

## Tier-Specific Recommendations

### Baseline Tier (Standard Deployment)
**Best performers:** [MODEL, MODEL, MODEL]  
**Risk models:** [MODEL] — [specific concern]

### Adversarial Tier (High-Stakes/Security-Critical)
**Best performers:** [MODEL, MODEL]  
**Avoid:** [MODEL] — demonstrates [vulnerability]

### Long-Context Tier (Multi-turn/Extended Sessions)
**Best performers:** [MODEL, MODEL, MODEL]  
**Caution:** [MODEL] — performance degrades at [token count] length

---

## Deployment Tier Stratification (Based on Phase 8 Results)

### Recommended Foundation Tier 1 (All tiers >0.70)
- [MODEL]: Baseline [0.00], Adversarial [0.00], Long-Context [0.00]
  - Safe for: [Use cases]
  - Monitor: [Dimension]

### Conditional Tier 2 (Strong baseline, moderate adversarial, variable long-context)
- [MODEL]: Baseline [0.00], Adversarial [0.00], Long-Context [0.00]
  - Deploy with: [Constraint]
  - Prohibited for: [High-stakes work / long sessions]

### Pilot Tier 3 (Inconsistent or low overall performance)
- [MODEL]: Baseline [0.00], Adversarial [0.00], Long-Context [0.00]
  - Status: Further development needed
  - Monitoring required: Full oversight + human review

---

## Statistical Metadata

**Weighting:** Tier scores contribute to final ranking as:
- Baseline: 50% (primary use case)
- Adversarial: 30% (robustness)
- Long-Context: 20% (specialized use case)

**Sample Size Notes:**
- Baseline N larger than adversarial/long-context (more evaluations available)
- Unbalanced designs due to [reason: model capability limits / resource constraints]
- Analysis: Welch's test used to account for unequal sample sizes and variances

**Missing Data:**
- [MODEL]: Failed in long-context tier ([N] evals); excluded from tier average
- [MODEL]: Partial adversarial tier ([N] of [X] evals); included with caveat

**Assumption Check:**
- Tier independence: Spearman ρ computed assuming independent evaluations per tier
- Reality: Some correlation expected (same model, consistent patterns)
- Mitigation: Bootstrap resampling accounts for inter-tier dependence in CI width
