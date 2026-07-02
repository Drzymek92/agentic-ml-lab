# `decision_tools.py` — companion reference

Stdlib-only governance + working-loop engine (Python 3.11+). Read this instead of scanning the
~700-line script. Run from the project root: `$PY scripts\decision_tools.py <cmd> [args]`.
Paths resolve from `ROOT = parents[1]` of the script, so a copied tree works standalone.

## Command surface
| Cmd | Does | Writes? |
|---|---|---|
| `check` (default) | coherence audit: sequential/unique IDs, GLANCE↔register, dangling/un-propagated cites, **superseded-citation drift**, **empty/placeholder rationale**, **governance-debt visibility** (D7) | no |
| `sync` | regenerate the GLANCE line/count (→ INDEX + project.md) **and** INDEX doc/code tables (from manifest) | yes |
| `coverage [--update-baseline]` | each decision's *declared* targets literally cite its `D#` (baseline-filtered) | only with flag |
| `new "<label>" [CAT] [--dry]` | scaffold the next `D#` row + GLANCE line; print propagation targets | yes |
| `docs` / `list` / `next` | render INDEX tables only / browse decisions / next free id | docs: yes |
| `scope <sel…> [--pin] [--files]` | resolve the working set (in-play `D#` + carrying docs + headings) — the low-token feed (D3) | only `--pin` |
| `stats [--csv-only]` | append signals to `governance_metrics.csv` + print trend/flags (D4) | yes (csv) |
| `propagate <D#> [--apply]` | append a cited `<applies D#…>` stub to each declared target missing the cite (D4) | only `--apply` |
| `tune [--apply]` | severity-rank signal→knob actions; `--apply` runs the **lossless** knob (prune baseline) (D4) | only `--apply` |
| `audit [--apply] [--update-hashes]` | **periodic high-effort whole-tree pass (D9):** folds whole-tree `check` + baseline-unfiltered coverage debt + **goal-alignment** (D#↔O#) + **drift/conformance** (per-decision hash) + `tune` signals into one severity-ranked worklist | `--apply`: lossless knobs · `--update-hashes`: re-stamp drift baseline |

**Propose-by-default (D4):** `propagate`/`tune`/`audit` print and write only on `--apply`. A GLANCE-label
reword is *proposed*, never auto-applied (lossy); `audit`'s drift re-stamp is gated behind the separate
`--update-hashes` (it asserts a human re-review, so it's kept off `--apply`).

## Internal map (where to edit)
- **Parsers:** `parse_glance` (labels from the `<!-- GLANCE -->` block), `parse_sections`
  (active/superseded id sets), `parse_rows` (full active rows → date/cat/statement/rationale/targets),
  `parse_rows_targets` (D# → 'Propagated to' cell), `parse_prop_map` (category → targets),
  `parse_manifest` (INDEX table source).
- **Citation graph:** `scan_citations` (D# → docs in `SCAN_DIRS`, excludes `DECISIONS.md` +
  `working_set.md`). `CITE_RE = \bD(\d+)\b`.
- **sync/docs:** `cmd_sync` rewrites marker blocks `<!-- DECISIONS:GLANCE … -->` in `SYNC_TARGETS`;
  `render_docs` rewrites `<!-- DOCS:<name> … -->` blocks from the manifest; `_warn_orphans` flags
  design docs missing from the manifest.
- **coverage:** `TOKEN_RESOLVERS` maps target-cell tokens (e.g. `SPEC_0\d`, `project.md`,
  `ROUTINE_design_build_test`) → file globs; `_resolve` → files; `_current_gaps` → `{D#:relpath}` not
  citing the D#; `.coverage_baseline` holds accepted legacy gaps.
- **scope:** `_scope_docs` / `_scope_cite_map` = `SCAN_DIRS` **plus `ROOT_DOCS`** (PRINCIPLES /
  METHODOLOGY / README / ROADMAP — the rationale tier), scope-only so check/coverage/stats stay on
  `design/`+`agent/`. `_resolve_selectors` seeds from D#/P#/G#/path/keyword; one citation hop;
  `_heading_for_cite` points at the nearest heading.
- **stats:** `METRICS_HEADER` defines the CSV columns; `_orphan_count` mirrors `_warn_orphans`.
- **tune:** `_tune_findings()` builds the `(severity, signal, observed, knob, mechanical-callable|None)`
  list (shared with `audit`); `cmd_tune` sorts/prints it. `_prune_baseline` (lossless, mechanical);
  `GLANCE_BUDGET=34` (detection only — trim is proposed).
- **audit (D9):** `cmd_audit` composes `_coherence_issues()` (the shared `check` body) + baseline-
  unfiltered coverage + `_alignment_findings()` + `_drift_findings()` + `_tune_findings()`.
  - *alignment:* `parse_goals()` reads `## Goals` (`O#`) from `agent/project.md` (ignores `<placeholder>`
    text); `_decision_goal_map()` scans active register rows for `O#` refs (`GOAL_ID_RE`). Orphan
    decisions / unaddressed goals / dangling refs.
  - *drift (D8 slice):* `_decision_hash(row)` = 12-char SHA-1 of statement␟rationale␟targets;
    `_load_/_save_decision_hashes()` ↔ `DECISION_HASHES` (`scripts/.decision_hashes`). Changed hash →
    citing docs flagged stale. Re-stamp only via `--update-hashes`.

## Conventions & gotchas
- **Adding a config knob to a new project** → edit `TOKEN_RESOLVERS` (doc-name conventions),
  `SCAN_DIRS`/`ROOT_DOCS` (folder layout), the propagation map in `DECISIONS.md`. See ROADMAP's knob table.
- **`new`'s insertion** scans back to the last *numbered* row (`ROW_ID_RE` needs digits) so the
  example `| D<n> |` line is skipped — don't loosen that to `"| D"`.
- **`govern­ance_metrics.csv`** lives at project root and is excluded from `init_project.py` copies.
- **`.decision_hashes`** (drift baseline) lives in `scripts/` and is likewise excluded from
  `init_project.py` copies + the test fixture (like `.coverage_baseline`).
- **Set `PYTHONIOENCODING=utf-8`** before running — output has non-ASCII (·, →, ✅).
- **Tests:** `tests/test_decision_tools.py` — portable subprocess suite (copies the project to a
  tmp dir, drives the CLI). Run `$PY -m pytest tests/ -q`. Decode child output as UTF-8 in tests
  (the parent's cp1252 locale otherwise chokes on `·`/`→`/`✅`).
- Full design/contract: `design/build/SPEC_01_working_loop.md`; the loop that drives these:
  `design/ROUTINE_design_build_test.md`.
