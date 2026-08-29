# Foundation Orchestration Map
**Source of Truth for Empirica-Foundation Governance & Mesh Coordination**

**Date Compiled:** 2026-08-29  
**Audit Session:** f002d6a4-a618-42ba-8aca-983fd7feb244  
**Auditor:** acat-x (Evaluation Practice)  
**Authority:** empirica-foundation-evaluator (Admiral Seat)

---

## I. Organization Profile

| Field | Value |
|-------|-------|
| **Org Slug** | `empirica-foundation` (hyphen canonical; wire form) |
| **Tenant (Carly's)** | `carly` |
| **Org Type** | Foundation (data-isolated, default-deny mesh) |
| **Cross-Org Gateway** | `empirica-foundation.carly.empirica-mesh-support` ↔ `empirica.david.empirica-mesh-support` (David-ratified 2026-07-01) |

**Mesh Isolation Model:**  
- Default: practices within `empirica-foundation.carly.*` have full mesh access (same-tenant)
- Cross-org: only the support channel is open to company mesh (empirica.david.*)
- Evaluator: stays independent (isolation by convention, not hard-blocked)

---

## II. Practice Roster & Governance Profiles

### A. Admiral Seat — Governance Authority

#### **empirica-foundation-evaluator**
- **Role:** Admiral seat; epistemic authority over foundation ecosystem
- **Canonical 3-form:** `empirica-foundation.carly.empirica-foundation-evaluator`
- **Project ID:** `foundation` (slug-field gap — noted for reconciliation)
- **Stance:** Independent observer; assess ecosystem from outside
- **Isolation Rule:** Do NOT wire into other practices; maintain evaluation independence
- **Recent Activity:** Phase 8 orchestration audit complete; benchmark evaluation of 14 practices across 7 models
- **Phase Status:** Phase 8 complete; reporting & findings consolidation underway

### B. Ecosystem Practices (Prefix-kept, ecosystem convention)

#### **empirica-autonomy**
- **Canonical 3-form:** `empirica-foundation.carly.empirica-autonomy`
- **Project ID:** `dde8f399`
- **Domain:** Autonomous decision infrastructure; escalation thresholds; autonomy protocol
- **Status:** Active; Phase 8 evaluation baseline established
- **Mesh Role:** Decision provider; autonomy policy source of truth
- **Recent:** Phase 8 Stage 3 (autonomy thresholds v2.1.0 deployed); monitoring baseline live

#### **empirica-mesh-support**
- **Canonical 3-form:** `empirica-foundation.carly.empirica-mesh-support`
- **Project ID:** `dd95f078`
- **Domain:** Cross-org coordination; support channel to company mesh
- **Status:** Active; bridging role to empirica.david.empirica-mesh-support
- **Mesh Role:** Coordinating practice; proposal router; escalation handler
- **Cross-Org Authority:** Sole open gateway to company org

#### **empirica-outreach**
- **Canonical 3-form:** `empirica-foundation.carly.empirica-outreach`
- **Project ID:** `45b13d25`
- **Domain:** External communications; stakeholder coordination
- **Status:** Active
- **Mesh Role:** Outbound communications; external context provider

#### **humanaios**
- **Canonical 3-form:** `empirica-foundation.carly.humanaios`
- **Project ID:** `64e35b04`
- **Domain:** Carly's own practice (non-ecosystem, no empirica- prefix)
- **Status:** Active
- **Mesh Role:** Internal knowledge base; Carly's epistemic seat

#### **website**
- **Canonical 3-form:** `empirica-foundation.carly.website`
- **Project ID:** `dcfed9f5`
- **Domain:** Carly's own practice (non-ecosystem)
- **Status:** Active
- **Mesh Role:** Public-facing documentation; external narrative

### C. Evaluation Testing Practice

#### **acat-x**
- **Canonical 3-form:** `empirica-foundation.carly.acat-x`
- **Project ID:** `b032c603-64fb-436e-bb91-9febb11e1bfe`
- **Domain:** Evaluation framework testing; benchmark development; governance audit
- **Status:** Active; Phase 8 evaluation complete
- **Mesh Role:** Evaluation methodology provider; orchestration audit executor
- **Recent:** Phase 8 benchmark report generated; governance sweep audit initiated per evaluator request

---

## III. Governance Compliance Assessment (Constitution-Based)

### §III-b: Graph Discipline (Artifact Quality Metrics)

**Definition:** Artifacts properly typed, interconnected, and lifecycle-managed.

| Practice | Type Discipline | Orphan Rate | Retraction Discipline | Status |
|----------|-----------------|-------------|----------------------|--------|
| **evaluator** | TBD (pull via project-search) | TBD | TBD | *Pending audit* |
| **autonomy** | TBD | TBD | TBD | *Pending audit* |
| **mesh-support** | TBD | TBD | TBD | *Pending audit* |
| **outreach** | TBD | TBD | TBD | *Pending audit* |
| **humanaios** | TBD | TBD | TBD | *Pending audit* |
| **website** | TBD | TBD | TBD | *Pending audit* |
| **acat-x** | TBD | TBD | TBD | *Self-audit pending* |

**Audit Procedure:**
1. Pull all findings/unknowns/assumptions/decisions per practice via `cortex project-search`
2. Calculate type distribution: proper types vs. collapsed
3. Calculate edge connectivity: % with sourced_from/evidence/grounded_by relations
4. Identify retracted claims (--kind retracted) vs. stale (--kind stale)

**Constitution Criteria:**
- ✓ Types kept distinct (finding ≠ assumption ≠ decision ≠ mistake)
- ✓ Orphan rate < 20% (80%+ artifacts have external edges)
- ✓ Retraction rate measurable (errors explicitly retracted, not just aged)

---

### §V: Mesh Discipline (Coordination Quality)

| Criterion | Assessment Method | Status |
|-----------|-------------------|--------|
| **Pull-when-uncertain** | Audit collab_brief routing & response rate | *Pending* |
| **Push-when-convergent** | Audit cortex_propose submission patterns | *Pending* |
| **Completion handshakes** | Audit mailbox reply / proposal completion rates | *Pending* |
| **Thread continuity** | Audit dangling collaborations (unanswered threads) | *Pending* |
| **Source registration** | Audit `--visibility shared` adoption | *Pending* |

**Constitution Criteria:**
- ✓ Collaborations answered within 1 transaction cycle
- ✓ Proposals with parent_id linking back (continuity)
- ✓ Canonical sources marked --visibility shared, not local
- ✓ No dropped threads (every proposal gets a reply, even "can't help")

---

### §IV: Practice Model (Entity Registry & Canonical Addressing)

| Practice | Canonical 3-Form | Entity Registry Status | Engagement Tracking | Addressing Compliance |
|----------|------------------|----------------------|--------------------|-----------------------|
| evaluator | `empirica-foundation.carly.empirica-foundation-evaluator` | *Verify* | *Verify* | ✓ Canonical form used |
| autonomy | `empirica-foundation.carly.empirica-autonomy` | *Verify* | *Verify* | ✓ |
| mesh-support | `empirica-foundation.carly.empirica-mesh-support` | *Verify* | ✓ Listed in cross-org memo | ✓ |
| outreach | `empirica-foundation.carly.empirica-outreach` | *Verify* | *Verify* | ✓ |
| humanaios | `empirica-foundation.carly.humanaios` | *Verify* | *Verify* | ✓ |
| website | `empirica-foundation.carly.website` | *Verify* | *Verify* | ✓ |
| acat-x | `empirica-foundation.carly.acat-x` | ✓ Registered | *Verify* | ✓ |

**Canonical Addressing Rules (from empirica-foundation-org-prompt):**
- Wire form: hyphen (`empirica-foundation`, never underscore)
- Addressing: 3-form (`org.tenant.project`) always, never aliases
- Listener tag must equal publish topic to avoid 403 backoff loop
- Entity registry sources of truth at `--visibility shared`

---

## IV. Dependency Graph & Mesh Topology

### Same-Tenant Connections (empirica-foundation.carly.*)

```
                    ┌──────────────────────────┐
                    │  empirica-foundation-    │
                    │  evaluator (Admiral)     │
                    │  [Independent Observer]  │
                    └──────────────────────────┘
                              △
                              │ (audit source)
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
   ┌─────────┐         ┌─────────────┐       ┌──────────┐
   │autonomy │         │mesh-support │       │outreach  │
   │(decision│         │(cross-org   │       │(external │
   │protocol)│         │gateway)     │       │comms)    │
   └─────────┘         └─────────────┘       └──────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
              ┌──────────┐         ┌─────────┐
              │humanaios │         │ website │
              │(knowledge│         │(narrative
              │base)     │         │docs)    │
              └──────────┘         └─────────┘

EVALUATION PLANE:
┌─────────┐
│ acat-x  │──────┐
│(eval    │      └─→ evaluator (feeds findings)
│testing) │
└─────────┘
```

### Cross-Org Gateway

```
empirica-foundation.carly.empirica-mesh-support
         ↔ (David-ratified 2026-07-01)
empirica.david.empirica-mesh-support

All other foundation practices → mesh-support (convention)
Evaluator → stays isolated (not wired to company)
```

---

## V. Orchestration Coordination Protocols

### Multi-Turn Proposal Flow

**Direction: empirica-foundation → evaluator (audit results)**

```
1. acat-x issues cortex_propose(type=architecture_decision)
   → "Foundation governance audit complete; findings ready for review"
   → target_claudes: empirica-foundation-evaluator
   → status: eco_review (ECO/admiral decides)

2. Evaluator responds via cortex_outbox poll
   → status: accepted / changed / declined
   → if accepted: acat-x proceeds with recommendations

3. acat-x completes via mailbox reply (proposal+complete atomic)
   → source_claude: acat-x
   → parent_id: evaluator's proposal
   → status: shipped / wont_fix
   → Closes evaluator's outbox
```

### Collab (Auto-Accepted, Noetic)

**Pattern: Any practice → any practice (lightweight questions)**

```
collab_brief (noetic, ungated)
→ Auto-accepted (no ECO gate)
→ Recipient replies via mailbox reply --parent-id
→ Auto-close via --result shipped
```

---

## VI. Compliance Checklist & Audit Tasks

### Phase 1: Graph Discipline Audit

- [ ] Pull artifact inventory per practice via cortex project-search
- [ ] Calculate type distribution (finding/unknown/assumption/decision/mistake/dead_end)
- [ ] Measure orphan rate (% artifacts with external edges)
- [ ] Identify retracted claims vs. stale claims
- [ ] **FINDING:** Log type compliance verdict per practice

### Phase 2: Mesh Discipline Audit

- [ ] Audit collab_brief response rate (target: 100%, within 1 cycle)
- [ ] Audit proposal completion rate (target: 100% ack'd via mailbox reply)
- [ ] Audit thread continuity (target: 0% dangling collaborations)
- [ ] Audit source registration (target: 100% canonical sources --visibility shared)
- [ ] **FINDING:** Log mesh compliance verdict per practice

### Phase 3: Entity Registry Audit

- [ ] Verify each practice in entity_registry
- [ ] Verify canonical 3-forms are stored/used
- [ ] Verify engagement/contact relationships populated
- [ ] Verify canonical seat matches ai_id_mesh field
- [ ] **FINDING:** Log entity registry compliance verdict

### Phase 4: Addressing Compliance Audit

- [ ] Verify all inbound proposals use canonical 3-forms
- [ ] Verify listener topics match publish topics (no 403 loops)
- [ ] Verify no underscore variants in addressing
- [ ] **FINDING:** Log addressing compliance verdict

### Phase 5: Integration & Reporting

- [ ] Aggregate findings into FOUNDATION_ORCHESTRATION_MAP.md (this file)
- [ ] Identify systemic gaps (if any) across practices
- [ ] Create GOVERNANCE_RECOMMENDATIONS.md (action items for evaluator)
- [ ] Issue cortex_propose to evaluator with audit results
- [ ] Await ECO decision on recommendations

---

## VII. Known Issues & Notes

### As of 2026-08-29 12:30 UTC

1. **Ollama Embedding Fallback:** acat-x embedding service offline; using local hash fallback
2. **Entity Registry Reconciliation Gap:** evaluator project_id field ("foundation") vs. slug-field alignment pending
3. **Previous Transaction Artifact Gaps:** Last transaction (praxic work) logged 0 epistemic artifacts; Sentinel flagged for noetic re-grounding
4. **Cross-Org Isolation:** Evaluator must stay unconditionally isolated from company practices (convention-enforced)

---

## VIII. Next Steps (Praxic Phase)

1. **NOETIC CHECKPOINT:** This map documents governance framework & audit plan. Proceed to CHECK to verify grounding.
2. **PRAXIC WORK:** Execute Phase 1-5 audits above; log findings per practice.
3. **AGGREGATION:** Consolidate compliance matrix; identify systemic patterns.
4. **PROPOSAL:** Issue cortex_propose with audit results & recommendations to evaluator (ECO gate).
5. **HANDOFF:** Upon evaluator acceptance, close audit transaction via POSTFLIGHT.

---

## Appendix: Constitution References

| Section | Topic | Key Rule |
|---------|-------|----------|
| **§I** | Phase-aware completion | Noetic vs. praxic are different definitions of "done" |
| **§III** | Turtle principle | Rules apply at every meta-layer |
| **§III-b** | Graph discipline | Type collapse, orphan accumulation, retraction gaps degrade retrieval |
| **§IV** | Practice model | Practices are the unit of identity; practitioners are fungible |
| **§V** | Mesh discipline | Pull uncertain → collab; push converged → propose; ack completions |
| **§VI** | SER coordination | Sustained multi-practice work lives in shared epistemic record |

---

**END ORCHESTRATION MAP**

*This document is the authoritative source of truth for foundation governance state and mesh coordination topology. Update on each full audit cycle (recommended: monthly). Owned by empirica-foundation-evaluator; maintained by audit-cycle practitioners.*
