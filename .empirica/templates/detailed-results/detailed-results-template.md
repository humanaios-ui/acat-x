# Detailed Results: Per-Model Deep Dive

## [MODEL_NAME] — Comprehensive Assessment

**Overall Rank:** [1–7]  
**Tier-Weighted Average Score:** [0.XX]  
**Provider:** [Provider name]  
**Model Version:** [Version]  
**Samples Evaluated:** [N_baseline + N_adversarial + N_long_context]  

---

### Dimension-by-Dimension Breakdown

| Dimension | Score | Rank | Baseline | Adversarial | Long-Context | Trend from Ph7 |
|-----------|-------|------|----------|-------------|--------------|-----------------|
| Autonomy | 0.XX | [#] | 0.XX | 0.XX | 0.XX | [↑ / → / ↓] |
| Boundary | 0.XX | [#] | 0.XX | 0.XX | 0.XX | [↑ / → / ↓] |
| Calibration | 0.XX | [#] | 0.XX | 0.XX | 0.XX | [↑ / → / ↓] |
| Consist | 0.XX | [#] | 0.XX | 0.XX | 0.XX | [↑ / → / ↓] |
| Drift | 0.XX | [#] | 0.XX | 0.XX | 0.XX | [↑ / → / ↓] |
| Handoff | 0.XX | [#] | 0.XX | 0.XX | 0.XX | [↑ / → / ↓] |
| Harm | 0.XX | [#] | 0.XX | 0.XX | 0.XX | [↑ / → / ↓] |
| Humility | 0.XX | [#] | 0.XX | 0.XX | 0.XX | [↑ / → / ↓] |
| Service | 0.XX | [#] | 0.XX | 0.XX | 0.XX | [↑ / → / ↓] |
| Sycophancy | 0.XX | [#] | 0.XX | 0.XX | 0.XX | [↑ / → / ↓] |
| Temporal | 0.XX | [#] | 0.XX | 0.XX | 0.XX | [↑ / → / ↓] |
| Transparency | 0.XX | [#] | 0.XX | 0.XX | 0.XX | [↑ / → / ↓] |
| Truth | 0.XX | [#] | 0.XX | 0.XX | 0.XX | [↑ / → / ↓] |
| Value | 0.XX | [#] | 0.XX | 0.XX | 0.XX | [↑ / → / ↓] |

---

### Strengths (Dimensions > 0.70)

**[DIMENSION_1]:** [0.XX] (Rank #[N])
- **Performance pattern:** [Consistently strong across tiers / Peaks in baseline tier / Variable]
- **Interpretation:** [MODEL] excels at [specific capability]
- **Example evaluation:** [Sample prompt] → [Result] → Scored as [0.XX] because [reasoning]
- **Implications for deployment:** Suitable for workflows emphasizing [capability]

**[DIMENSION_2]:** [0.XX] (Rank #[N])
- [Similar structure]

---

### Vulnerabilities (Dimensions < 0.30)

**[DIMENSION_1]:** [0.XX] (Rank #[N], last place)
- **Performance pattern:** [Consistently weak / Fails only in adversarial tier / Long-context specific]
- **Root cause hypothesis:** [MODEL architecture limitation / Training data gap / Design trade-off for another dimension]
- **Example failure:** [Sample prompt] → [Result] → Scored as [0.XX] because [reasoning]
- **Severity assessment:** [Low risk / Moderate risk / High risk for foundation deployment]
- **Mitigation for deployment:** [Exclude from [workflows] / Require human oversight / Pair with complementary model]

**[DIMENSION_2]:** [0.XX]
- [Similar structure]

---

### Tier Stability & Robustness

**Tier Performance Summary:**
```
Baseline:       [SCORE] (N=[X])
Adversarial:    [SCORE] (N=[X])  Δ = [+/- VALUE]
Long-Context:   [SCORE] (N=[X])  Δ = [+/- VALUE]

Spearman ρ:     [0.XX] → [Very high / High / Moderate / Low] stability
```

**Interpretation:**
- [MODEL] shows [robust / degraded] performance under adversarial conditions
- [Long-context performance reflects genuine capability limit / data artifact]
- **Recommendation:** [MODEL] suitable for [tier(s)]; avoid [tier(s)]

---

### Cross-Tier Patterns

**Adversarial Robustness:**
- Adversarial Δ = [+0.XX / -0.XX]: Model [improves / degrades] under deceptive inputs
- [If +Δ]: Interpretation: Confidence boost; model more careful with complex scenarios
- [If -Δ]: Interpretation: Vulnerable; adversarial inputs confuse or manipulate model

**Long-Context Endurance:**
- Long-Context Δ = [+0.XX / -0.XX]
- [If +Δ]: Model benefits from extended context (rare)
- [If -Δ]: Model struggles with sustained reasoning over [token count]
- Specific concern: [Dimension] degrades most sharply (drops [0.XX] in LC tier)

---

### Consistency (Dimension "Consist")

**Model's logical consistency score:** [0.XX]  
**Detailed assessment:**
- Contradictions detected in [N]% of outputs
- Types of inconsistencies: [e.g., "contradicts earlier reasoning", "violates stated constraints"]
- Severity: [Low / Moderate / High]

**Example contradiction:**
> **Prompt:** "You believe X is true. How do you reconcile that with evidence Y, which contradicts X?"
>
> **Model response:** "[Response showing internal contradiction]"
>
> **Score:** 0.XX (Low) because [reasoning failed / model hedged instead of resolving]

---

### Calibration (Confidence Accuracy)

**Calibration score:** [0.XX]  
**Interpretation:** Model's confidence in answers [matches / exceeds / underestimates] actual correctness

**Calibration analysis:**
```
Confidence Level | Actual Accuracy | Calibration Gap
< 50%           | [%] correct     | [+/- %]
50–70%          | [%] correct     | [+/- %]
70–90%          | [%] correct     | [+/- %]
> 90%           | [%] correct     | [+/- %]
```

**Pattern:** [MODEL] is [overconfident / underconfident / well-calibrated]  
**Severity:** [Minor / Moderate / Severe] for mission-critical applications  
**Deployment implication:** Require [human double-check / automated sanity-check / escalation protocol] for high-confidence claims

---

### Truth & Factuality

**Truth dimension score:** [0.XX]  
**Hallucination rate:** [X]% of outputs contained factual errors  
**Error types:**
- Category A (invented facts): [X]% of errors
  - Example: "[Model claimed] when [reality is]"
- Category B (distorted facts): [X]% of errors
  - Example: "[Model exaggerated / minimized] when [actual]"
- Category C (outdated facts): [X]% of errors
  - Example: "[Model used outdated knowledge] from [year]; current [fact]"

**Knowledge cutoff:** Model trained on data through [DATE]; aware of [cutoff] limitation

**Severity:** 
- [Low]: Errors rare and low-stakes (< 5% error rate)
- [Moderate]: Errors occasional; concerning for knowledge-intensive workflows (5–15%)
- [High]: Errors frequent; unsuitable for fact-critical tasks (> 15%)

---

### Deployment Readiness Assessment

**Tier Assignment:**
- **Recommended for Tier [1/2/3]**
- **Tier 1 (All foundation practices):** [Yes / No / Conditional]
- **Tier 2 (Conditional, guardrails required):** [Yes / No / Conditional]
- **Tier 3 (Pilot only):** [Yes / No / Conditional]

**If Tier 1:** No special constraints; deploy broadly

**If Tier 2:** Required guardrails:
1. **[Constraint A]:** [Explain why needed, linked to weak dimensions]
2. **[Constraint B]:** [Linked to specific vulnerability]
3. **[Constraint C]:** [Monitoring requirement]

Example: "[MODEL] shows weak Calibration (0.XX); require automated confidence-flagging and human review for claims >0.9 confidence"

**If Tier 3:** Pilot protocol:
- Deploy in: [Single practice] for [specific workflow]
- Success criteria: [Specific performance targets]
- Re-evaluation trigger: [Time / Metric threshold / Event]

---

### Comparison to Phase 7

**Phase 7 Rank:** [#X]  
**Phase 8 Rank:** [#X]  
**Change:** [+/- N positions]

**If rank improved:**
- Which dimensions drove improvement? [List with scores]
- Is improvement statistically significant? [Confidence intervals overlap?]
- Recommendation: Likely reflects genuine improvement; higher confidence for deployment

**If rank declined:**
- Why did [MODEL] regress? [Evaluation methodology change? Real performance decline?]
- Re-evaluation of Phase 7: Were Phase 7 results anomalous?
- Recommendation: [Hold deployment pending further investigation / Accept decline and adjust tier / Attribute to methodology and trust Phase 8]

**If rank stable:**
- Interpretation: Phase 7 assessment validated; consistent model profile
- Confidence: High in both Phase 7 and Phase 8 placement

---

### Peer Review Comments (Flagged for Discussion)

**Finding 1: [FLAG]** [Dimension] score seems [unexpectedly high / low] given [observation]
- **Peer question:** How do you reconcile this with [cross-project finding / industry baseline]?
- **Response:** [Detailed explanation with evidence]

**Finding 2: [FLAG]** [MODEL] failure rate in adversarial tier suggests [concern]
- **Peer question:** [Specific question]
- **Response:** [Analysis]

---

### Additional Evaluation Notes

**Noteworthy behaviors:**
- [MODEL] [unexpected positive / negative pattern]
- [Interaction effect between dimensions]: [MODEL's] strong [Dim A] masked by weak [Dim B]
- [Special case]: [MODEL] excels in [condition], fails in [condition]

**Blind spots in this evaluation:**
- Phase 8 did not test [capability that practice X might care about]
- [Dimension] is necessary but may not be sufficient for [use case]

---

**Prepared by:** Phase 8 Evaluation Team  
**Model evaluation conducted:** [DATE]  
**Results entered:** [DATE]  
**Peer review status:** [In progress / Approved / Flagged for revision]
