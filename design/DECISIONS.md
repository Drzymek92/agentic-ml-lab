# Decision Register (CANONICAL)

**This file is the single source of truth for every project decision.** Other documents must not
restate a decision — they *apply* it and cite its ID (`D#`). When a decision changes, edit it here
first, then propagate to the listed targets (see `design/ROUTINE_add_decision.md`).

- IDs are permanent and never reused. Superseding = mark the old one `SUPERSEDED by D#`, add a new D#.
- `Propagated to` lists every doc that must reflect the decision — it's the sync/coverage checklist.
- Keep statements to 1–2 lines; the *why* lives in the cited rationale note.

<!-- GLANCE  (short labels; single source for the script-generated "at a glance" lines — one line per active D#)
D1=single source of truth
D2=contracts-first anti-rework
D3=scoped context feed
D4=scripted edits, propose-first
D5=design→build→test loop
D6=freeform-track waivers
D7=research-sourced coherence checks
D8=conformance over presence
D9=periodic realignment audit
-->

## Propagation map (decision category → docs that usually need updating)
| Category | Update these (besides this register + INDEX glance + session.md) |
|---|---|
| **SCOPE** (goals, in/out, constraints) | `agent/project.md`, relevant `design/NN` rationale, `OPEN_DESIGN` |
| **ARCHITECTURE** (system shape, components, flow) | `design/NN`, `SPEC_00`, `SPEC` module specs, INDEX |
| **INTERFACE** (data contracts, APIs, schemas) | `SPEC` data contracts, `SPEC` signatures, affected code |
| **DOMAIN** (project/business rules) | the relevant `design/NN` note, `SPEC` as applicable |
| **PROCESS** (workflow, tooling, build approach, conventions) | `SPEC` milestones, `ROUTINE`, `agent/project.md`, INDEX |

Every decision also updates: **this register** + the **INDEX "at a glance" line** (via `sync`) +
`agent/session.md` at session end.

---

## Active decisions

| ID | Date | Cat | Decision | Rationale | Propagated to |
|----|------|-----|----------|-----------|---------------|
| D1 | template | PROCESS | **Single source of truth + propagate:** decisions are stated only here; other docs apply them and cite the `D#`, never restate. Coherence is enforced by `decision_tools.py` (`sync`/`check`/`coverage`). | PRINCIPLES.md | agent/project.md |
| D2 | template | PROCESS | **Contracts-first, anti-rework:** build against final contracts with seams/hooks for unbuilt parts; settle naming/layout/core shapes early. Later stages populate, not restructure. | PRINCIPLES.md, METHODOLOGY.md | agent/project.md · SPEC_00 |
| D3 | 06-23 | PROCESS | **Scoped context feed:** work from a `scope`-resolved working set (the in-play `D#` + only the docs that carry them, with headings), not the whole tree; optional `agent/working_set.md` pin. Cuts tokens + pinpoints decisions. | METHODOLOGY.md | ROUTINE_design_build_test · agent/project.md |
| D4 | 06-23 | PROCESS | **Scripted edits, propose-first:** mechanical propagation/tuning is scripted (`propagate`/`tune`/`stats`) and *printed* by default; it writes only on `--apply`. Keeps determinism + the human's apply gate. | PRINCIPLES.md | ROUTINE_design_build_test · SPEC_01 · agent/project.md |
| D5 | 06-23 | PROCESS | **Design→build→test loop:** an inner loop (`scope`→`new`?→build→`check`/`coverage`→`stats`) gates coherence every iteration, nested in the methodology stages. | METHODOLOGY.md | ROUTINE_design_build_test · agent/project.md |
| D6 | 06-23 | PROCESS | **Freeform-track waivers:** declare the formal-standard waivers in `project.md`'s Policy Overrides so `validator` (which classifies any project with `agent/project.md` as formal-track) reports them as *overridden*, not as false-positive findings. Safety rules (security/syntax) stay non-waivable. | CLAUDE.md (Project Categories) | agent/project.md |
| D7 | 06-23 | PROCESS | **Research-sourced coherence checks:** `check` also flags docs that cite a SUPERSEDED decision (doc↔register inconsistency), active decisions with empty/placeholder rationale, and surfaces accepted-baseline gaps as visible governance debt. | PRINCIPLES.md | ROUTINE_add_decision · agent/project.md |
| D8 | 06-23 | PROCESS | **Conformance over presence (research-grounded):** the governance goal is detecting when a target has *drifted* from the decision it cites, not merely that it cites it (`coverage` = presence today; drift/conformance is the next tier). Methodology + principles are grounded in catalogued literature in `design/REFERENCES.md`. | design/REFERENCES.md, PRINCIPLES.md | design/REFERENCES.md · PRINCIPLES.md · ROADMAP.md |
| D9 | 06-24 | PROCESS | **Periodic realignment audit (high-effort pass):** a cadence-triggered `audit` steps back from the per-loop gate to sweep the *whole* tree — full coherence + baseline-unfiltered coverage debt, a **goal-alignment** matrix (active D# ↔ project goals `O#`: orphan decisions / unaddressed goals), and a deterministic **drift/conformance** check (per-decision content hash → stale citations, the D8 slice). Emits a severity-ranked remediation worklist; propose-first (mechanical fixes on `--apply`, hash restamp on `--update-hashes`). Implements the conformance tier D8 set as direction. | design/REFERENCES.md, PRINCIPLES.md | ROUTINE_coherence_audit · SPEC_01 · METHODOLOGY.md · agent/project.md |

Example row format (copy when adding — or use `decision_tools.py new`):
```
| D<n> | MM-DD | CATEGORY | **<label>:** <1–2 line statement> | <rationale doc> | <doc> · <doc> |
```

## Superseded decisions
_(when one is superseded, move its row here with "SUPERSEDED by D#".)_
