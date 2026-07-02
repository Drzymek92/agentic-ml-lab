# Open Design — Priorities & Architectural Gaps  (LIVING)

Tracks **what still needs deciding/designing** — distinct from `DECISIONS.md` (settled), the SPEC
milestones (build sequencing), and the rationale notes (settled reasoning).

**How to use:** when a gap is resolved, record the decision in `DECISIONS.md` (get a `D#`), then
**move the gap to "Recently closed" with that `D#`** and propagate per the routine. Add new gaps as
they surface. Keep IDs stable (`G#`, `P#`). This is the standing answer to "what's unresolved and
what's next."

_Last reviewed: <date> (<N> decisions locked)._

---

## Priority design points (ordered — each unblocks a stage/milestone)
| P# | Design point | Resolves gaps | Unblocks |
|----|--------------|---------------|----------|
| P1 | <the next thing to design/decide> | <G#> | <stage/milestone> |

> Rule of thumb: design just-in-time, one priority ahead of what you're building.

## Architectural gaps (open unknowns)
- **G1 — <gap>.** <why it matters> *Path:* <how to resolve> *Rel:* <D#> · <milestone>.

## Candidate ideas — research-sourced, awaiting confirmation (2026-06-23)
Mined from the `governance-design-decision-management` research set (resources KB). The high-value,
low-noise, deterministic ones were implemented under **D7**; these need a scoping decision before
building. Confirm/approve one to promote it to a `G#` + `D#`.

- **C1 — Reverse-traceability / untracked trace-link recovery** (from *SoK: Software Artifacts
  Traceability*). Surface docs that **cite a `D#` but aren't in that decision's declared targets**
  (the inverse of `coverage`). High value, but **noisy as-is**: the generated GLANCE blocks in
  INDEX/project.md list every `D#`, so a naive scan false-positives. *Path:* exclude GLANCE-marker
  regions + non-target docs (session/working_set/ROUTINE_add/OPEN_DESIGN), then flag only substantive
  design docs. *Decision needed:* hard `check` gate vs advisory. *Rel:* extends D1/D7.
- **C2 — Architecture-erosion composite index** (from *Understanding Software Architecture Erosion*).
  One rolled-up "erosion" signal in `stats`/`tune` combining superseded-rate + edited-after-create
  rate + baseline growth, with a threshold flag. *Path:* add a derived column to `governance_metrics.csv`
  + a `tune` finding. *Decision needed:* the weighting/threshold. *Rel:* extends ROADMAP autotracking.
- **C3 — Dated, reasoned technical-debt register** (from *Technical Debt: A Systematic Mapping Study*).
  Promote `.coverage_baseline` from bare `D#:path` lines to TD items carrying **date + reason**, and
  add a **debt-age** signal to `tune` (old accepted gaps = accruing interest). *Path:* extend the
  baseline format + `cmd_tune`; keep back-compat parsing. *Rel:* extends D7 debt-visibility.
- **C4 — LLM-assisted design-rationale drafting** (from *Using LLMs in Generating Design Rationale*).
  When `check` flags an empty rationale (D7), optionally **draft** a rationale via FuelIX for the human
  to edit. *Tension:* `decision_tools.py` is deliberately **stdlib-only / no harness coupling** — this
  would break that. *Decision needed:* keep tooling pure and do this in the agent workflow instead, or
  add an opt-in seam. *Rel:* extends D7.

## Recently closed
_(move resolved gaps here with the closing `D#` and date)_
- _none yet._
