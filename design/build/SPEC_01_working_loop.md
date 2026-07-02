# BUILD SPEC 01 — Working-Loop tooling (scope · stats · propagate · tune · audit)

The *how* for the active layer driven by `ROUTINE_design_build_test.md` (per-loop) and
`ROUTINE_coherence_audit.md` (periodic). Five commands on
`scripts/decision_tools.py`, all **stdlib, determinism-first**, reusing the existing parsers
(`scan_citations`, `parse_rows`/`parse_rows_targets`, `parse_glance`, `_current_gaps`). SPECs are
authoritative when building.

## Golden rules (in addition to SPEC_00)
- **Propose-by-default (D4):** edit/tune commands print the planned change and write **only** on
  `--apply`. No silent edits to the user's docs.
- **Scoped reads (D3):** never dump a whole doc; point at the file + heading and let the agent open it.
- **Determinism first:** every signal/edit is computed from the register + citation graph, not guessed.

## Milestones
| Milestone | Delivers | Accept when |
|---|---|---|
| M1 ✅ | `scope` — working-set resolver (D3) | `scope D#/keyword/path` prints in-play D# + carrying docs+headings; `--pin`/bare round-trips `working_set.md` |
| M2 ✅ | `stats` — autotracking (D4) | first run writes `governance_metrics.csv` header+row; second prints trend deltas + threshold flags |
| M3 ✅ | `propagate <D#>` — scripted cited stubs (D4) | dry-run lists each declared target missing the cite; `--apply` inserts `<applies D#…>` and `coverage` goes 0-new |
| M4 ✅ | `tune` — metrics → config knobs (D4) | dry-run prints ranked signal→knob actions; `--apply` does only the lossless mechanical knob (prune resolved baseline); GLANCE-trim is *proposed*, not auto-applied |
| M5 ✅ | `audit` — periodic whole-tree coherence + realignment pass (**D9**) | one severity-ranked worklist folding whole-tree `check` + baseline-unfiltered coverage debt + goal-alignment (D#↔O#) + drift/conformance (per-decision hash); `--apply` runs the lossless mechanical fixes; `--update-hashes` re-stamps the drift baseline |

## Data contract — `.decision_hashes` (M5, D9 drift baseline)
Conformance baseline for the drift check: one `D#:hash` line per active decision, where `hash` is a
12-char SHA-1 of the decision's canonical content (statement ␟ rationale ␟ targets). Re-stamped only by
`audit --update-hashes` (after human re-review). Stdlib only; excluded from `init_project.py` copy
(like `.coverage_baseline` / `governance_metrics.csv`). A decision whose current hash ≠ its stamped
hash → its citing docs are flagged **stale** (re-verify, then re-stamp).

## Data contract — `governance_metrics.csv` (M2, stable columns)
One row per `stats` run, appended; header written once. Excluded from `init_project.py` copy.
```
ts, decisions_active, decisions_superseded, superseded_rate,
coverage_total, coverage_baselined, coverage_new,
avg_propagation_breadth, glance_max_len, orphans, docs_count, days_since_last_decision
```

## Interface contracts (signatures — all built)
- `cmd_scope()` — selectors from `argv`; `--pin` writes `agent/working_set.md`, `--files` paths-only.
  Seeds → one citation hop → compact read-plan. Doc universe = `design/`+`agent/` **plus the root
  rationale tier** (`ROOT_DOCS`: PRINCIPLES/METHODOLOGY/README/ROADMAP) via `_scope_cite_map`, so the
  "why" doc surfaces too — scope-only, leaving `check`/`coverage`/`stats` on `design/`+`agent/`. *(built)*
- `cmd_stats()` — compute the row above; `--csv-only` suppresses the screen read. *(built)*
- `cmd_propagate()` — `propagate <D#> [--apply]`. For each file in `_resolve(targets[D#])` lacking a
  `\bD#\b` cite, append a cited stub `<applies D# — <label>: …>` at the file end; print the preview;
  write only on `--apply`. Closes the gap so `coverage` goes 0-new. *(built)*
- `cmd_tune()` — `tune [--apply]`. Map current state + `governance_metrics.csv` signals to the ROADMAP
  signal→knob table; severity-rank; `--apply` runs only the idempotent, **lossless** mechanical knob
  (prune resolved `.coverage_baseline` via `_prune_baseline`). An over-budget GLANCE label
  (`GLANCE_BUDGET=34`) is *proposed* for a manual reword — never auto-trimmed, since trimming rewords
  a label (lossy). *(built)*
- `cmd_audit()` — `audit [--apply] [--update-hashes]` (**applies D9**). Whole-tree, not scoped. Folds
  `_coherence_issues()` (whole-tree `check`) + baseline-**unfiltered** coverage debt +
  `_alignment_findings()` (goal-matrix via `parse_goals`/`_decision_goal_map`) + `_drift_findings()`
  (per-decision content hash vs `.decision_hashes`) + `_tune_findings()` into one severity-ranked
  worklist. Reuses the existing parsers — adds no parallel system. `--apply` runs only the lossless
  mechanical fixes; `--update-hashes` re-stamps the drift baseline (an explicit re-review act, kept off
  `--apply`). The conformance slice **D8** pointed at; the periodic counterpart to the per-loop gate. *(built)*

## Notes
The agent is the orchestrator — there is **no runnable loop driver** (it would have to do judgment).
These commands are the deterministic rungs the agent stands on while following the routine.
