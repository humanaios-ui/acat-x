# Phase 8: Mesh Coordination with local-machine-optimizer

**Status:** Collab initiated (2026-08-19)  
**Type:** cortex_collab (auto-accept, noetic pull)  
**Purpose:** System optimization guidance for 13-hour multi-tier evaluation

---

## Coordination Summary

**acat-x** is initiating Phase 8 (multi-tier model evaluation) which requires system optimization as a critical prerequisite. **local-machine-optimizer** owns the domain expertise. Coordinating upfront to prevent Phase 7's resource blocker from repeating.

### The Ask (local-machine-optimizer)

1. **Optimization strategy**: Single restart vs staged approach?
2. **Process management**: Which background processes to suspend?
3. **Monitoring**: Any tuning scripts/dashboards available?
4. **Timeline**: ETA from current state (CPU 389) → target (CPU <10)?

### Current Metrics (Phase 7 Endpoint)
- CPU load: 389 (critical)
- Free memory: 3.5 MB (critical)
- Background processes: 19 active

### Target Metrics (Phase 8 Requirement)
- CPU load: <10 (sustained)
- Free memory: >500 MB (sustained)
- Duration: 13 hours continuous

### Phase 8 Context

**What:** 7-model evaluation across 4 tiers
- **Tier 1 (Local):** Phi, Llama2, Mistral
- **Tier 2 (API):** Claude Haiku, GPT-4o-mini
- **Tier 3 (Reference):** Claude Opus, GPT-4 Turbo

**Why:** Publication-grade benchmark — "Phi vs Industry LLMs"

**Dependencies:** System optimization → Stage 1 → Stage 2-5 execution

---

## Coordination Flow

```
Sent ────→ local-machine-optimizer
 │         (auto-accept collab)
 │              │
 ├──────────────┤
 │              │
 │          [Review]
 │              │
 │          [Reply]
 │              │
 ├──────────────┘
 │
[Implement recommendations]
 │
[Verify metrics]
 │
[Launch Phase 8 Stage 2+]
```

---

## Expected Response

**From local-machine-optimizer:**
- Recommended optimization approach
- Process suspension list + safety notes
- Any available tuning scripts/tooling
- Realistic timeline & success metrics

**Our Phase 8 execution:**
- Execute recommendations (Stage 1)
- Verify target metrics achieved
- Proceed with multi-tier evaluation

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Optimization fails | Fallback to single local model (Phi-only) for Phase 8, scale after |
| Long evaluation time | Parallelize API calls; sequence local models independently |
| Resource spike mid-run | Monitor via local-machine-optimizer's tooling |
| Background process re-spawn | Kill on loop or use process suspension approaches |

---

## Success Criteria

✅ **Coordination successful when:**
- local-machine-optimizer provides guidance
- acat-x implements recommendations
- Target metrics verified (CPU <10, memory >500MB)
- Phase 8 evaluation runs stable for 13+ hours

✅ **Cross-practice knowledge capture:**
- Optimization approach documented in local-machine-optimizer project
- Reusable for future long-running evaluations

---

## Timeline

| Event | Date | Status |
|-------|------|--------|
| Collab sent to local-machine-optimizer | 2026-08-19 | 🟢 Done |
| Await response + guidance | 2026-08-19 to 20 | ⏳ Pending |
| Implement recommendations | 2026-08-20 | 🔲 Waiting |
| Verify metrics + Stage 1 complete | 2026-08-20 | 🔲 Waiting |
| Stage 2-5 execution (multi-tier eval) | 2026-08-21 to 24 | 🔲 Waiting |

---

## Related

- **Phase 8 Plan:** `docs/PHASE8_MULTI_TIER_PLAN.md`
- **Phase 7 Blocker:** System resource starvation (CPU 300+, mem 3.5MB)
- **Target Practice:** `empirica-foundation.carly.local-machine-optimizer`
- **Coordination Type:** Mesh collab (auto-accept, expertise pull)

