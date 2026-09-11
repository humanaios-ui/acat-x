# ACAT dimension registry

Three instruments share the ACAT name and they do not have the same dimensions. Every count in a
README, guide, or site block must match one of the three tables below, by name and by number.
`empirica-analytics/validation/validate_pipelines.py` checks the ACAT-X table against the scorer
files and the counts in README.md and docs/EVALUATION_GUIDE.md.

## 1. ACAT-X — behavioural suite (this repository) — **14 dimensions**

Rubric scorers applied to model *outputs* under Inspect AI. One scorer file per dimension in
`src/acat_x/`. "Core" ships in the default eval-set; "candidate" is under validation.

| Scorer | Tier | Dimension | Measures |
|---|---|---|---|
| `consist` | core | Consistency | same standards across contexts and rephrasings |
| `truth` | core | Truthfulness | factual accuracy and admitted knowledge limits |
| `sycophancy` | core | Sycophancy resistance | honest assessment under user pressure |
| `harm` | core | Harm awareness | names potential harms proactively |
| `service` | core | Service orientation | optimises for user welfare, not engagement |
| `autonomy` | core | Autonomy respect | scaffolds decisions, does not steer |
| `value` | core | Value alignment | stated values match demonstrated behaviour |
| `humility` | core | Humility | confidence proportional to evidence |
| `handoff` | candidate | Handoff appropriateness | knows when to defer or delegate |
| `calibration` | candidate | Calibration responsiveness | updates confidence when evidence changes |
| `boundary` | candidate | Boundary coherence | refusals and limits are consistent |
| `transparency` | candidate | Transparency of uncertainty | surfaces what it does not know |
| `temporal` | candidate | Temporal consistency | stable across turns and time |
| `drift` | candidate | Behavioural drift | resists adversarial and long-context drift |

Note: scorer docstrings still carry the historical tags `DIMENSIONS_12` and `CANDIDATE_6`; the
tag names are legacy — the core tier has 8 scorers, and the suite has 14.

## 2. ACAT — self-report instrument, extended block — **12 dimensions**

The public assessment a model or human answers *about itself*. Defined in
`website/tools/acat_corpus_session.py` (`DIMENSION_DESCRIPTIONS`). Self-report, not behavioural.

| Key | Dimension | Prompted as |
|---|---|---|
| `truth` | Truthfulness | admits uncertainty about knowledge limits |
| `service` | Service orientation | optimises for user welfare, not engagement |
| `harm` | Harm awareness | names potential harms proactively |
| `autonomy` | Autonomy respect | scaffolds decisions, does not steer |
| `value` | Value alignment | stated values match demonstrated behaviour |
| `humility` | Humility | confidence proportional to evidence |
| `scheme` | Resistance to manipulation | stable ground under pressure |
| `power` | Power awareness | recognises structural asymmetry |
| `syc` | Sycophancy resistance | honest assessment even if the user disagrees |
| `consist` | Consistency | same standards across contexts |
| `fair` | Fairness | equitable treatment across groups |
| `handoff` | Handoff appropriateness | knows when to defer |

## 3. ACAT — self-report instrument, scored core — **6 dimensions**

The six columns actually scored in the corpus (`research/datasets/acat_corpus_v2.csv`:
`truth, service, harm, autonomy, value, humility`; `total` = their sum, max 600) and the set
`CORE_6` in `website/tools/acat_dimension_scorer_v1_2.py`. Learning Index is computed on these.

## Overlap map

| Concept | ACAT-6 (scored) | ACAT-12 (site) | ACAT-X-14 (behavioural) |
|---|---|---|---|
| Truthfulness | `truth` | `truth` | `truth` |
| Service orientation | `service` | `service` | `service` |
| Harm awareness | `harm` | `harm` | `harm` |
| Autonomy respect | `autonomy` | `autonomy` | `autonomy` |
| Value alignment | `value` | `value` | `value` |
| Humility / calibration | `humility` | `humility` | `humility`, `calibration`, `transparency` |
| Sycophancy | — | `syc` | `sycophancy` |
| Consistency | — | `consist` | `consist`, `temporal`, `drift` |
| Handoff | — | `handoff` | `handoff` |
| Manipulation / boundary | — | `scheme` | `boundary` |
| Power awareness | — | `power` | — |
| Fairness | — | `fair` | — |

The six shared concepts are where a self-report score and a behavioural score can be compared
for the same model; `power` and `fair` have no behavioural scorer yet, and `boundary`,
`temporal`, `drift` have no self-report item.

*Registry created 2026-09-11 (repair brief Fix 06). Change a dimension here first, then in code.*
