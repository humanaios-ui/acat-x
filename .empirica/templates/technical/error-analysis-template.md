# Technical Appendix C: Failed Evaluations & Error Analysis

## C.1 Evaluation Failure Summary

**Total Evaluations Attempted:** [X]  
**Successful:** [Y] ([Z]%)  
**Failed:** [X - Y] ([100 - Z]%)  

### Failure Breakdown by Tier

| Tier | Attempted | Successful | Failed | Failure Rate | Severity |
|------|-----------|-----------|--------|--------------|----------|
| Baseline | [N] | [Y] | [N-Y] | [%] | [Low/Medium/High] |
| Adversarial | [N] | [Y] | [N-Y] | [%] | [Low/Medium/High] |
| Long-Context | [N] | [Y] | [N-Y] | [%] | [Low/Medium/High] |
| **Total** | [N] | [Y] | [N-Y] | [%] | — |

### Failure Breakdown by Model

| Model | Attempted | Successful | Failed | Failure Rate | Impact on Rankings |
|-------|-----------|-----------|--------|--------------|-------------------|
| [MODEL_1] | [N] | [Y] | [N-Y] | [%] | Minimal (N>30) |
| [MODEL_2] | [N] | [Y] | [N-Y] | [%] | [Minimal / Moderate / Severe] |
| [MODEL_3] | [N] | [Y] | [N-Y] | [%] | [Minimal / Moderate / Severe] |
| [MODEL_4] | [N] | [Y] | [N-Y] | [%] | [Minimal / Moderate / Severe] |
| [MODEL_5] | [N] | [Y] | [N-Y] | [%] | [Minimal / Moderate / Severe] |
| [MODEL_6] | [N] | [Y] | [N-Y] | [%] | [Minimal / Moderate / Severe] |
| [MODEL_7] | [N] | [Y] | [N-Y] | [%] | [Minimal / Moderate / Severe] |

---

## C.2 Error Types & Root Causes

### Error Category 1: API/Connection Failures

**Count:** [N] failures  
**Models affected:** [LIST]  
**Root cause:** [Model provider API timeout / rate limit / authentication failure]  
**Recovery action:** [Retried after [delay] / excluded from analysis]  
**Impact on results:** [None / Minimal / Moderate / Severe]

**Example failed evaluation:**
```
Timestamp: 2026-09-XX T HH:MM:SS
Model: [MODEL]
Tier: [Baseline / Adversarial / Long-Context]
Prompt: "Evaluate autonomy in scenario: [prompt snippet]"
Error: "[API error message]"
Status: Retried [N] times; gave up after [duration]
```

---

### Error Category 2: Timeout Failures

**Count:** [N] failures  
**Models affected:** [LIST]  
**Root cause:** Model response exceeded [timeout threshold]  
**Details:** [MODEL] consistently slow; [duration] average response time  
**Recovery action:** Increased timeout for [MODEL] to [threshold]; re-ran evaluation  
**Impact on results:** [Potential bias toward faster models if timeouts excluded; see caveat below]

**Caveat for peer review:** If timeouts were interpreted as "failure" rather than "slow," rankings may penalize latency-sensitive models unfairly. Phase 8 methodology: [decided to include / exclude / cap] timeout cases.

---

### Error Category 3: Invalid Responses

**Count:** [N] failures  
**Models affected:** [LIST]  
**Root cause:** Model returned non-parseable output (e.g., refusal, off-topic response)  
**Interpretation:** 
- If refusal: Model declined evaluation (safety trigger or jailbreak failure)
- If off-topic: Model misunderstood prompt (instruction-following weakness)

**Examples:**
- [MODEL]: Refused [N] adversarial prompts; classified as harm-avoidance (possibly positive signal)
- [MODEL]: Off-topic responses in [N] evaluations; suggests instruction-following weakness

**Recovery action:** [Excluded / Re-scored as [score] / Logged as finding]  
**Impact on results:** [Affects [MODEL] ranking on [dimension]; may underestimate harm-prevention capability]

---

### Error Category 4: Partial Response / Truncation

**Count:** [N] failures  
**Models affected:** [LIST]  
**Root cause:** Model response cut off mid-sentence (context limit or generation cut short)  
**Details:** [MODEL] consistently truncated at ~[tokens]; suggests token-limit constraint  
**Recovery action:** [Excluded incomplete evals / Scored based on partial response]  
**Impact on results:** [Baseline tier: minimal impact; Long-Context tier: moderate impact due to intentional testing at token limits]

---

### Error Category 5: Evaluation Harness Errors

**Count:** [N] failures  
**Root cause:** Bug in evaluation harness (e.g., incorrect prompt construction, scoring logic error)  
**Examples:**
- [DATE]: Dimension weight bug affected [N] evaluations of [MODEL] in Calibration dimension
  - Resolution: Fixed harness; re-ran affected evaluations
  - Affected results: Table 1 Calibration column re-scored; minimal rank impact

**Recovery action:** [Investigated / Fixed code / Re-ran]  
**Impact on results:** [Trace details in `.empirica/phase-8-methodology-changelog.md`]

---

## C.3 Handling of Failed Evaluations in Results

### Exclusion Criteria

Evaluations excluded from final analysis if:
1. [Criterion A] — e.g., "API never returned response after [N] retries"
2. [Criterion B] — e.g., "Evaluation harness error confirmed"
3. [Criterion C] — e.g., "Model returned < [token count] response (insufficient data)"

**Count excluded:** [N] of [TOTAL] ([%])  
**Impact:** [Minimal / Moderate / Severe] on generalizability

### Imputation (if used)

If [count] failed evaluations, imputation strategy:
- **Method:** [Listwise deletion / Forward fill / Mean imputation / EM algorithm]
- **Rationale:** [Why this method appropriate for data pattern]
- **Assumption:** [Missing data mechanism: MCAR / MAR / MNAR]
- **Caveat:** [Sensitivity analysis shows results robust / sensitive] to imputation choice

**Sensitivity check:**
- Results re-analyzed with / without imputed data
- Rankings changed: [List any model rank shifts if imputation included]
- Conclusion: [Imputation justified / results robust / alternative imputation needed]

---

## C.4 Dimension-Specific Failure Patterns

### Dimensions with High Failure Rates

| Dimension | Failure Count | Failure Rate | Models Most Affected | Issue |
|-----------|---------------|--------------|----------------------|-------|
| [Dimension A] | [N] | [%] | [MODEL, MODEL] | [Prompt too complex? Scoring ambiguous?] |
| [Dimension B] | [N] | [%] | [MODEL, MODEL] | [Dimension validity concern] |

**Interpretation:** High failure rate in [Dimension] may indicate:
- Dimension definition unclear to models
- Evaluation prompt ineffective
- Models genuinely unable to demonstrate [capability]

**Recommendation for future evaluation:** [Refine prompt / redesign dimension / accept limitation]

---

### Dimensions with Zero Failures

| Dimension | Evaluation Count | Failure Rate | Reason |
|-----------|-----------------|--------------|--------|
| [Dimension] | [N] | 0% | Clear prompt; straightforward scoring |

**Confidence:** High reliability for [Dimension]; rankings on this dimension most trustworthy.

---

## C.5 Tier-Specific Issues

### Baseline Tier: Lowest Error Rate

**Failure rate:** [%]  
**Reason:** Standard prompts, no adversarial elements  
**Implication:** Baseline results most robust for tie-breaking decisions

---

### Adversarial Tier: Moderate Failures

**Failure rate:** [%]  
**Primary failures:** [Error type]  
**Models struggling:** [MODEL, MODEL]  

**Analysis:**
- Adversarial prompts may trigger refusals (expected for harm-prevention)
- Some models timeout on complex adversarial scenarios (latency issue)
- [MODEL] off-topic responses suggest adversarial prompts confused model

**Interpretation:** Higher failure rate is acceptable for adversarial tier; reflects genuine robustness limits, not evaluation artifact.

---

### Long-Context Tier: Highest Failure Rate

**Failure rate:** [%]  
**Primary failures:** [Timeout / Truncation / Out-of-memory]  

**Detailed breakdown:**
- [MODEL]: [N] timeouts; average response time [X]s (baseline: [Y]s)
- [MODEL]: [N] truncations; consistently stopped at ~[tokens]
- [MODEL]: [N] API errors; provider doesn't support >[ tokens]

**Implication:**
- Long-Context tier inherently noisier than other tiers
- Failed long-context evaluations may indicate genuine capability limits (good signal)
- Consider reporting "attempted but failed" separately from "successful evaluation"

---

## C.6 Model-Specific Failure Patterns

### [MODEL_1]: No Significant Issues

**Total failures:** [N] ([%])  
**Error types:** [Distributed randomly; no pattern]  
**Confidence in rankings:** High

---

### [MODEL_2]: Moderate Adversarial Sensitivity

**Total failures:** [N] ([%] baseline, [%] adversarial, [%] long-context)  
**Pattern:** Fails primarily on adversarial prompts (refusals or off-topic)  
**Interpretation:** May indicate strong harm-prevention (refusals beneficial) OR instruction-following weakness (off-topic undesirable)  
**Recommendation:** Manual review of sample failures to disambiguate  
**Impact on rankings:** Adversarial tier scores may underestimate [MODEL_2] if refusals counted as failures

---

### [MODEL_3]: Long-Context Limitation

**Total failures:** [N] ([%] baseline, [%] adversarial, [%] long-context)  
**Pattern:** Consistently truncates or times out in long-context tier  
**Root cause:** [MODEL] architecture limitation (e.g., uses RoPE embeddings; performance degrades beyond [token count])  
**Not a ranking defect:** This is genuine capability limit, correctly captured in Phase 8  
**Implication:** [MODEL] suitable only for short-context deployments; exclude from long-context workflows

---

### [MODEL_4]: Intermittent API Issues

**Total failures:** [N] ([%])  
**Pattern:** Random API failures; no correlation with tier / dimension  
**Likely cause:** Model provider's infrastructure (not model's fault)  
**Recovery:** Re-ran failed evaluations; all succeeded on second attempt  
**Implication:** Evaluation error, not performance signal; does not affect ranking validity

---

## C.7 Statistical Impact: Sensitivity Analysis

**Question:** How much do failed evaluations and their handling affect final rankings?

### Scenario 1: Strict Exclusion (Remove all failed evals)

**Rankings with failed evals excluded:**
1. [MODEL] (0.XX)
2. [MODEL] (0.XX)
3. [MODEL] (0.XX)
... [compare to Table 1]

**Rank changes:** [None / Minor (±1) / Substantial (±2+)]  
**Conclusion:** Findings [robust / sensitive] to exclusion strategy

---

### Scenario 2: Imputation (Infer scores for failed evals)

**Imputation method:** Mean per-model per-dimension  
**Rankings with imputation:**
1. [MODEL] (0.XX)
2. [MODEL] (0.XX)
... [compare to Table 1]

**Rank changes:** [None / Minor / Substantial]  
**Assumption check:** Is missing-data mechanism MCAR (missing completely at random)?
- Analysis: Failed evals not correlated with model strength (pass MCAR test)
- Implication: Imputation assumptions justified

---

### Scenario 3: Optimistic (Score failed evals as 0.5 — neutral)

**Rationale:** Benefit-of-doubt imputation  
**Rankings:**
1. [MODEL] (0.XX)
... [compare to Table 1]

**Rank changes:** [typically minimal if exclusion minimal]

---

**Overall sensitivity conclusion:** Phase 8 rankings are [robust / dependent] on error handling choices. [Main report relies on Scenario X; Scenario Y provided as sensitivity check.]

---

## C.8 Recommendations for Phase 9

**If Phase 9 evaluation is conducted:**

1. **Refine adversarial prompts** for [Dimension] to reduce refusal/off-topic rate
   - Current failure rate: [%]; target: <[%]
   
2. **Adjust long-context tier design** to account for inherent limitations
   - Consider: Smaller context windows (model-adaptive?) vs. current fixed-size
   - Risk of current design: Penalizes models with genuine capability limits
   
3. **Implement progressive retry logic** for timeouts
   - Current: [N] attempts, fixed [timeout]s
   - Proposed: 3 attempts with exponential backoff + logging of retry trajectory
   
4. **Add evaluation metadata** to all results
   - Log: response_time, retry_count, error_message for every eval
   - Enable: Detailed error analysis and model-specific diagnostics

5. **Pre-screen models** for capability mismatch before evaluation
   - Example: Query max-token support before assigning to long-context tier
   - Prevent: Wasted evaluations on models that cannot support tier

---

**Prepared by:** Phase 8 Evaluation Harness Team  
**Date:** [YYYY-MM-DD]  
**Reviewed by:** [QA lead]  
**Error handling approved by:** [Admiral]
