# Routine — Retrofit Governance onto an Existing Project

The optimized subroutine for "this project has standardized structure but **no governance** → give
it the decision/design OS without rewriting it." Goal: let the **script** do the mechanical overlay
(determinism-first), and spend human judgment only on **seeding the register from what's already
documented**. Works for either track (formal `projects/` or freeform `other_projects/`).

Run scripts with Python 3.11+ (this machine: the anaconda interpreter):
```
$PY = "C:\Users\michal.drzymaa\AppData\Local\anaconda3\python.exe"
& $PY other_projects\governance_template\scripts\init_project.py --retrofit <project_path> [--desc "..."]
```

## Steps

1. **Run the overlay (mechanical, zero judgment).** `init_project.py --retrofit <project_path>`
   copies *only* the governance layer (`PRINCIPLES`/`METHODOLOGY`, the whole `design/` register +
   routines, `scripts/decision_tools.py`, `tests/test_decision_tools.py`, `agent/working_set.md`),
   **never clobbering** a file the project already has. It appends a Governance section (with the
   GLANCE markers) to the existing `agent/project.md`, a pointer to the existing `README.md`, and
   runs `sync`. Preview first with `--dry-run`. It refuses if `design/DECISIONS.md` already exists.

2. **Seed the register from existing docs (the judgment half — the smoothing).** The overlay ships
   the template's own `D1`–`D8` (decisions about the methodology). Now capture *this project's* real
   decisions as new `D#` rows — the next IDs after the template's `D8` — by **mining what's already
   written** rather than inventing:
   - **Sources, in order:** `ARCHITECTURE.md` (explicit design calls), `agent/project.md`
     (*Open Questions* that were resolved, *Known Gotchas*, *Policy Overrides*, *File Structure
     Notes*), and any `documentation_processed/_changelog.md` clarifications.
   - For each genuine, still-live decision: `decision_tools.py new "<short label>" <CATEGORY>`
     (SCOPE / ARCHITECTURE / INTERFACE / DOMAIN / PROCESS), then fill the row's statement +
     rationale + *Propagated to* cell, citing the `D#` in the doc that already explains it.
   - **Bulk option (FuelIX):** for a doc-heavy project, draft candidate rows by delegating the
     *extraction* to FuelIX (`skills/helpers/fuelix.py --task bulk`) — "list the discrete design
     decisions in this file as label + one-line rationale" — then **human-review** before recording.
     Extraction is fuzzy (LLM-appropriate); recording + citing stays deterministic and reviewed.
   - Don't over-capture. A handful of load-bearing decisions beats forcing every paragraph into a `D#`.

3. **Gate it.** `sync` → `check` → `coverage`. `check` must print **OK**; `coverage` must be
   **clean / 0 new**. Legitimately pre-existing, not-yet-cited gaps go into `scripts/.coverage_baseline`
   as accepted governance debt (visible, not hidden) rather than forcing busy-work citations.

4. **`agent/session.md`** — one short block: governance retrofitted, the `D#`s seeded, gaps baselined.

## Efficiency rules (keep it cheap)
- **One overlay run, then batch the seeding** — record all the new `D#` rows, then one round of propagation
  `Edit`s, then a single `sync`/`check`/`coverage`.
- **Cite, don't restate:** apply each decision where it already lives (append a cited line), never
  copy the decision text into multiple docs — the register is the single source of truth (**D1**).
- **Mine, don't invent:** every seeded `D#` should trace to something the project already documented.

## What the script guarantees (so you don't re-verify by hand)
- The overlay never overwrites an existing file (skips + reports any collision).
- The existing `project.md`/`README.md` get the governance pointers idempotently (re-runnable).
- `sync` populates the GLANCE blocks + INDEX tables; `check`/`coverage` enforce coherence thereafter.

## Promotion note
This subroutine is exposed in the framework via `/project:project_init` (governance is default-on for
medium+ complexity projects, opt-in otherwise) and is the standard way to bring an older project up to
the governance bar. See `skills/project_init.md`.
