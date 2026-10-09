# Retraction Discipline

**Status:** draft, §III-b remediation item 3 (retraction discipline documentation).
**Scope:** how acat-x closes epistemic artifacts: the four resolution kinds, when to use each, and the metric that shows whether we use them.

## Why this exists

Closing a finding and retracting a finding look alike in the graph and mean opposite things. Closing records progress. Retracting records error. A practice that only closes artifacts, and never retracts, reads as though it was never wrong.

Baseline from `empirica profile-status` on 2026-10-09: `correction_record` shows 1 resolution in total (`superseded: 1`) and 0 retractions, against 120 findings and 21 unknowns in the local store.

## The four kinds

`finding-resolve` takes one of four `--kind` values. The vocabulary is closed. Pick the one that matches the reason, not the one that is easiest to type.

| Kind | Use when | Requires | Example |
|---|---|---|---|
| `stale` | The claim was true when written and has since aged out. | `--resolution` | "Endpoint list was accurate before the migration." |
| `superseded` | A newer, named artifact replaces the claim. | `--resolution`, `--superseded-by <id>` | "Replaced by the corrected baseline, finding `ab12cd34`." |
| `retracted` | The claim was **false when written**. A genuine error, not ageing. | `--resolution` (say what was wrong) | "Claimed 0 orphan findings; the store has 38% with no edges." |
| `mistyped` | The item belongs to a different artifact type. | `--resolution` | "A mistake logged as a finding; re-logged as a mistake." |

### The test that separates `stale` from `retracted`

Ask: **was this wrong on the day it was written?**

- Yes → `retracted`, even if nobody noticed for weeks.
- No, it was right and has since expired → `stale`.
- Right when written, and a newer artifact now says more → `superseded`, with the replacement's ID.

If the answer is unclear, do not default to `stale`. Say the uncertainty in `--resolution`, and log an unknown against the artifact.

## Rules

1. **Never use `stale` to hide an error.** A claim that was false when written, marked `stale`, is a misrecord. It makes the error invisible to calibration.
2. **Retraction keeps the original wording.** The claim text is immutable. A wrong claim is retracted, not edited. Correct metadata with `update-artifacts`; retract the claim.
3. **Retractions name the defect.** `--resolution` states what was wrong, in one sentence a reader can check.
4. **Retraction does not require a replacement.** A retracted claim may have no successor. Log a new finding only if something true replaces it.
5. **Batches keep per-item judgment.** `resolve-artifacts` takes `resolution_kind` per item. Do not mark a whole cluster `stale` because the call is bulk.

## Measuring it

`empirica profile-status --output json` reports `correction_record.by_kind`. A practice that uses the vocabulary properly shows `retracted` and `superseded` entries, not only `stale`. The remediation spec sets a target of more than 5% retractions across the foundation graph. This document does not set a per-practice target.

## Examples

Retract a false claim:

```bash
empirica finding-resolve <id> --kind retracted \
  --resolution "Claimed 0 orphan findings; the store has 38% with no edges."
```

Supersede with a named replacement:

```bash
empirica finding-resolve <id> --kind superseded \
  --superseded-by <new-id> \
  --resolution "Replaced by the corrected baseline after the telemetry fix."
```

Age out a claim that was right when written:

```bash
empirica finding-resolve <id> --kind stale \
  --resolution "Endpoint list was accurate before the migration."
```

## Out of scope

The 238 reclassifications and 105 orphan edges in the remediation spec are not covered here. Both need a confirmed ID list before any graph write. The acat-x store has an open unknown for that ID list.
