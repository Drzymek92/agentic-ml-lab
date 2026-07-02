# References — research grounding for the governance model

<!-- applies D8 -->
This doc grounds the template's principles/decisions in peer-reviewed software-engineering research
(**applies D8**: ground the methodology, and aim governance at *conformance*, not just citation
presence). Sources are catalogued in the shared `resources/` KB under
`research/governance-design-decision-management/` — pull full text via
`/project:librarian "<topic>"` or `resources_kb query`.

| Source (year) | Grounds | What it validates / suggests |
|---|---|---|
| Meyer, *Applying "Design by Contract"* (1992) | **D2** contracts-first | Pre/post-conditions + invariants as interface contracts — the canonical basis for "settle contracts early, populate later." |
| Naumchev & Meyer, *Seamless Object-Oriented Requirements* (2019) | **D1** single source of truth | One continuous model from requirements→code with no representational gap — the anti-drift core; a decision stated once and propagated. |
| *SoK: Systematizing Software Artifacts Traceability* (2026) | `coverage` / propagation map | Names **"traceability debt"** (manual links are neglected, error-prone) — our `coverage` gate + propagation map are the automation the field reports as missing; adopt a goal-driven, role-centric view of links. |
| *CASCADE: Detecting Inconsistencies between Code & Documentation* (FSE) | **D8** conformance | Detects doc↔code drift by generating tests from docs — the model for the next tier: verify a cited D# is still *honored*, not just present. |
| Li et al., *Understanding Software Architecture Erosion* (2022) | **D8** conformance | "Divergence between intended and implemented" = the drift we fight; remedy = conformance checking / architecture monitoring (frame `check` as a lightweight conformance checker). |
| Li, Avgeriou & Liang, *A Systematic Mapping Study on Technical Debt & its Management* (2015) | `stats` / `tune` | 8 TDM activities (identification, **measurement, prioritization**, monitoring, prevention…) — confirms the `stats`/`tune` autotracking direction; measurement + prioritization are the levers. |
| Zhou et al., *Using LLMs in Generating Design Rationale* (2025) | **D4**, **D7** rationale | Design rationale is chronically under-documented (our register fixes it); LLM-generated rationale is often misleading → keep **propose-first** human vetting (D4) and rationale-completeness checks (D7). |
| *Software Architecture Decision-Making Practices & Challenges* (2016) | whole model | Empirical industrial study of how teams actually make/record decisions — grounds the register-first discipline against real practice + its challenges. |
| *Knowledge Management in Software Engineering: A Systematic Review* (2018) | whole model | KM framing for capturing/propagating design knowledge — the register + INDEX + scope feed are a concrete KM system. |

## Direction set by D8 → first slice built by D9 (the conformance tier)
`coverage` proves **presence** (a declared target literally cites the `D#`). The research above
(CASCADE, architecture erosion) points at **conformance**: detect when a target has *drifted* from
the decision it cites. The concrete, stdlib-deterministic first slice is now **built under D9**: the
periodic `audit` stamps a per-decision content hash and flags **stale citations** when a decision
changed since its last stamp (its citing docs may no longer honor it → re-review). This realises the
"architecture monitoring / conformance checking" remedy the erosion literature (Li et al. 2022)
prescribes, and the periodic-review cadence the technical-debt mapping study (Li, Avgeriou & Liang
2015) frames as *measurement + prioritization*. It stays deterministic (no NLP) and propose-first
(D4); the LLM-tier CASCADE-style check remains future work in [`../ROADMAP.md`](../ROADMAP.md).
