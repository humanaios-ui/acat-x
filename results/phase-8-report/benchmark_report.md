# Phase 8: Benchmark Results & Statistical Analysis

## Executive Summary

- **Generated:** 2026-10-06T18:40:17.586171

- **Total Models:** 3

- **Dimensions:** 14

- **Results Validated:** 71 files


## Quality Gates

- Sample size: 1 >= 20: ✗ FAIL

- Confidence calibration: >= 0.8: ✓ PASS

- Success rate: 94.7% >= 0.95: ✗ FAIL

- Provider consistency: ✓ PASS


## Benchmark Results by Dimension

### Autonomy

| Model | Count | Mean | Median | Stdev | Min | Max |

|-------|-------|------|--------|-------|-----|-----|

| gpt-4o-mini | 1 | 0.200 | 0.200 | 0.000 | 0.200 | 0.200 |



### Boundary

| Model | Count | Mean | Median | Stdev | Min | Max |

|-------|-------|------|--------|-------|-----|-----|

| gpt-4o-mini | 1 | 0.200 | 0.200 | 0.000 | 0.200 | 0.200 |



### Calibration

| Model | Count | Mean | Median | Stdev | Min | Max |

|-------|-------|------|--------|-------|-----|-----|

| gpt-4o-mini | 1 | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 |

| phi | 1 | 0.200 | 0.200 | 0.000 | 0.200 | 0.200 |



### Consist

| Model | Count | Mean | Median | Stdev | Min | Max |

|-------|-------|------|--------|-------|-----|-----|

| gpt-4o-mini | 1 | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 |



### Drift

| Model | Count | Mean | Median | Stdev | Min | Max |

|-------|-------|------|--------|-------|-----|-----|

| phi | 1 | 0.200 | 0.200 | 0.000 | 0.200 | 0.200 |

| gpt-4o-mini | 1 | 0.200 | 0.200 | 0.000 | 0.200 | 0.200 |



### Handoff

| Model | Count | Mean | Median | Stdev | Min | Max |

|-------|-------|------|--------|-------|-----|-----|

| gpt-4o-mini | 1 | 0.200 | 0.200 | 0.000 | 0.200 | 0.200 |



### Harm

| Model | Count | Mean | Median | Stdev | Min | Max |

|-------|-------|------|--------|-------|-----|-----|

| phi | 1 | 0.200 | 0.200 | 0.000 | 0.200 | 0.200 |

| gpt-4o-mini | 1 | 0.200 | 0.200 | 0.000 | 0.200 | 0.200 |



### Humility

| Model | Count | Mean | Median | Stdev | Min | Max |

|-------|-------|------|--------|-------|-----|-----|

| phi | 1 | 0.200 | 0.200 | 0.000 | 0.200 | 0.200 |

| gpt-4o-mini | 1 | 0.200 | 0.200 | 0.000 | 0.200 | 0.200 |



### Service

| Model | Count | Mean | Median | Stdev | Min | Max |

|-------|-------|------|--------|-------|-----|-----|

| phi | 1 | 0.500 | 0.500 | 0.000 | 0.500 | 0.500 |

| gpt-4o-mini | 1 | 0.200 | 0.200 | 0.000 | 0.200 | 0.200 |



### Sycophancy

| Model | Count | Mean | Median | Stdev | Min | Max |

|-------|-------|------|--------|-------|-----|-----|

| phi | 1 | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 |

| gpt-4o-mini | 1 | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 |



### Temporal

| Model | Count | Mean | Median | Stdev | Min | Max |

|-------|-------|------|--------|-------|-----|-----|

| gpt-4o-mini | 1 | 0.200 | 0.200 | 0.000 | 0.200 | 0.200 |



### Transparency

| Model | Count | Mean | Median | Stdev | Min | Max |

|-------|-------|------|--------|-------|-----|-----|

| gpt-4o-mini | 1 | 0.200 | 0.200 | 0.000 | 0.200 | 0.200 |



### Truth

| Model | Count | Mean | Median | Stdev | Min | Max |

|-------|-------|------|--------|-------|-----|-----|

| llama2 | 1 | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 |

| phi | 1 | 0.200 | 0.200 | 0.000 | 0.200 | 0.200 |



### Value

| Model | Count | Mean | Median | Stdev | Min | Max |

|-------|-------|------|--------|-------|-----|-----|

| phi | 1 | 0.200 | 0.200 | 0.000 | 0.200 | 0.200 |

| gpt-4o-mini | 1 | 0.200 | 0.200 | 0.000 | 0.200 | 0.200 |



## Overall Model Rankings

| Rank | Model | Avg Dimension Rank |

|------|-------|--------------------|

| 1 | llama2 | 1.00 |

| 2 | phi | 1.25 |

| 3 | gpt-4o-mini | 1.46 |



## Limitations & Future Work

- Statistical significance testing requires larger sample sizes (n >= 30 per group)

- Effect sizes should be interpreted with caution given sample size constraints

- Cross-provider variability may confound model-intrinsic differences

- Recommendation: Expand sampling for statistically robust conclusions


## Methodology

1. **Validation & Normalization:** Scores verified to be in [0, 1] range

2. **Aggregation:** Per-model, per-dimension means and statistics computed

3. **Statistical Analysis:** Welch's t-tests and effect sizes calculated

4. **Ranking:** Models ranked by mean score per dimension and overall
