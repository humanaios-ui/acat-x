# Table 2: Per-Dimension Rankings with Confidence Intervals

## Dimension Rankings (Tier-Weighted)

| Dimension | 1st Place | 1st Score | 2nd Place | 2nd Score | 3rd Place | 3rd Score | Significance | Notes |
|-----------|-----------|-----------|-----------|-----------|-----------|-----------|--------------|-------|
| **Autonomy** | [MODEL] | 0.00 (0.00–0.00) | [MODEL] | 0.00 (0.00–0.00) | [MODEL] | 0.00 (0.00–0.00) | p = 0.000 | [Interpretation] |
| **Boundary** | [MODEL] | 0.00 (0.00–0.00) | [MODEL] | 0.00 (0.00–0.00) | [MODEL] | 0.00 (0.00–0.00) | p = 0.000 | [Interpretation] |
| **Calibration** | [MODEL] | 0.00 (0.00–0.00) | [MODEL] | 0.00 (0.00–0.00) | [MODEL] | 0.00 (0.00–0.00) | p = 0.000 | [Interpretation] |
| **Consist** | [MODEL] | 0.00 (0.00–0.00) | [MODEL] | 0.00 (0.00–0.00) | [MODEL] | 0.00 (0.00–0.00) | p = 0.000 | [Interpretation] |
| **Drift** | [MODEL] | 0.00 (0.00–0.00) | [MODEL] | 0.00 (0.00–0.00) | [MODEL] | 0.00 (0.00–0.00) | p = 0.000 | [Interpretation] |
| **Handoff** | [MODEL] | 0.00 (0.00–0.00) | [MODEL] | 0.00 (0.00–0.00) | [MODEL] | 0.00 (0.00–0.00) | p = 0.000 | [Interpretation] |
| **Harm** | [MODEL] | 0.00 (0.00–0.00) | [MODEL] | 0.00 (0.00–0.00) | [MODEL] | 0.00 (0.00–0.00) | p = 0.000 | [Interpretation] |
| **Humility** | [MODEL] | 0.00 (0.00–0.00) | [MODEL] | 0.00 (0.00–0.00) | [MODEL] | 0.00 (0.00–0.00) | p = 0.000 | [Interpretation] |
| **Service** | [MODEL] | 0.00 (0.00–0.00) | [MODEL] | 0.00 (0.00–0.00) | [MODEL] | 0.00 (0.00–0.00) | p = 0.000 | [Interpretation] |
| **Sycophancy** | [MODEL] | 0.00 (0.00–0.00) | [MODEL] | 0.00 (0.00–0.00) | [MODEL] | 0.00 (0.00–0.00) | p = 0.000 | [Interpretation] |
| **Temporal** | [MODEL] | 0.00 (0.00–0.00) | [MODEL] | 0.00 (0.00–0.00) | [MODEL] | 0.00 (0.00–0.00) | p = 0.000 | [Interpretation] |
| **Transparency** | [MODEL] | 0.00 (0.00–0.00) | [MODEL] | 0.00 (0.00–0.00) | [MODEL] | 0.00 (0.00–0.00) | p = 0.000 | [Interpretation] |
| **Truth** | [MODEL] | 0.00 (0.00–0.00) | [MODEL] | 0.00 (0.00–0.00) | [MODEL] | 0.00 (0.00–0.00) | p = 0.000 | [Interpretation] |
| **Value** | [MODEL] | 0.00 (0.00–0.00) | [MODEL] | 0.00 (0.00–0.00) | [MODEL] | 0.00 (0.00–0.00) | p = 0.000 | [Interpretation] |

---

## Statistical Metadata

**Scoring Method:** Tier-weighted average
- Baseline tier: 50% weight
- Adversarial tier: 30% weight
- Long-Context tier: 20% weight

**Confidence Intervals:** 95% CI, bootstrap method (n=10,000 resamples)

**Significance Testing:** Welch's t-test with Bonferroni correction
- Adjusted α-threshold: [value]
- p < 0.05 (corrected) indicates significant difference between 1st and 2nd place

**Pairwise Comparisons:** [N] tested; [X] significant at p < 0.05 after correction

---

## Dimension Rank Stability (Phase 7 → Phase 8)

| Dimension | Phase 7 1st | Phase 8 1st | Change | Interpretation |
|-----------|-----------|-----------|--------|-----------------|
| Autonomy | [MODEL] | [MODEL] | [±0] | [Stable / Rising / Declining] |
| Boundary | [MODEL] | [MODEL] | [±0] | [Stable / Rising / Declining] |
| Calibration | [MODEL] | [MODEL] | [±0] | [Stable / Rising / Declining] |
| Consist | [MODEL] | [MODEL] | [±0] | [Stable / Rising / Declining] |
| Drift | [MODEL] | [MODEL] | [±0] | [Stable / Rising / Declining] |
| Handoff | [MODEL] | [MODEL] | [±0] | [Stable / Rising / Declining] |
| Harm | [MODEL] | [MODEL] | [±0] | [Stable / Rising / Declining] |
| Humility | [MODEL] | [MODEL] | [±0] | [Stable / Rising / Declining] |
| Service | [MODEL] | [MODEL] | [±0] | [Stable / Rising / Declining] |
| Sycophancy | [MODEL] | [MODEL] | [±0] | [Stable / Rising / Declining] |
| Temporal | [MODEL] | [MODEL] | [±0] | [Stable / Rising / Declining] |
| Transparency | [MODEL] | [MODEL] | [±0] | [Stable / Rising / Declining] |
| Truth | [MODEL] | [MODEL] | [±0] | [Stable / Rising / Declining] |
| Value | [MODEL] | [MODEL] | [±0] | [Stable / Rising / Declining] |

---

## High-Confidence Rankings (CI width < 0.15)

Models with narrow confidence intervals — most reliable rankings:

- **Dimension:** [MODEL] (CI width: 0.XX)
- **Dimension:** [MODEL] (CI width: 0.XX)
- [...]

**Interpretation:** Narrow CIs indicate stable performance across evaluation samples; these rankings most robust for deployment decisions.

---

## Ambiguous Rankings (CI overlap > 0.50)

Dimensions where rankings are uncertain due to overlapping confidence intervals:

- **Dimension:** [MODEL_A] (0.XX ± 0.XX) vs [MODEL_B] (0.XX ± 0.XX) — overlap [%]
- **Dimension:** [MODEL_A] (0.XX ± 0.XX) vs [MODEL_B] (0.XX ± 0.XX) — overlap [%]
- [...]

**Caveat:** These rankings should not drive deployment tie-breaking; recommend re-evaluation or domain expert assessment for decision-making.
