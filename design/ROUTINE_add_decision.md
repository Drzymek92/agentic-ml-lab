# Routine — Add / Change a Decision

The optimized workflow for "decision → required edits → output". Goal: do **only the semantic work**
by hand; let `scripts/decision_tools.py` do the mechanical, error-prone parts. Keep edits surgical
and output compact.

Run scripts from the project root with Python 3.11+:
```
$PY = "C:\Users\michal.drzymaa\AppData\Local\anaconda3\python.exe"
& $PY scripts\decision_tools.py <new|sync|check|coverage|docs|list|next>
```

## Steps
1. **Decide the category** (SCOPE / ARCHITECTURE / INTERFACE / DOMAIN / PROCESS) — it picks the
   propagation targets via the register's *Propagation map*.
2. **Scaffold it** — `decision_tools.py new "<short label>" <CATEGORY>` appends the next `D#` row +
   GLANCE line and **prints the propagation targets**. Then fill the row's statement, rationale link,
   and *Propagated to* cell. (`--dry` to preview.) Reversal? edit the row in place, or move it to
   **## Superseded** as `SUPERSEDED by D#` + add a new row. IDs are permanent.
3. **Write the semantic edits only** — for each target: rationale → the relevant `design/NN` note
   (*why*); contract/behavior → the relevant `SPEC` section (*how*). Each edit **applies the decision
   and cites the `D#`** — never restates it. Don't hand-edit glance lines, counts, or INDEX tables.
4. **`decision_tools.py sync`** — regenerates the at-a-glance line/count (from GLANCE) **and the
   INDEX doc/code tables** (from `docs_manifest.txt`). If the decision adds a doc/code file, add
   **one line to `docs_manifest.txt`** — don't hand-edit the INDEX tables.
5. **`check` then `coverage`** — `check` must print **OK**; `coverage` must be **clean / 0 new** (it
   verifies each decision's *declared* targets literally cite it; a `NEW propagation gap` means you
   forgot to cite the `D#` in a declared target). Pre-existing accepted gaps live in `.coverage_baseline`.
6. **`agent/session.md`** — one short block: the new `D#`(s) + what was propagated.

## Efficiency rules (keep the loop cheap)
- **Batch all propagation edits in ONE message** (parallel `Edit` calls).
- **Append, don't splice:** add a short cited line at a section's end rather than rewriting prose.
- **Read each target once.** Don't re-Read a file you just edited to "verify" — Edit errors on failure.
- **Compact output:** the decision + id, a small `D# | decision | propagated to` table, the gate
  result line, the single most important consequence + next action.

## What the script guarantees (so you don't re-verify by hand)
- glance lines & counts in INDEX/project.md match the register (`sync`);
- IDs sequential & unique; no dangling/typo `D#` cites; every active decision cited ≥1 place (`check`);
- no doc still *applies* a **superseded** decision, every active decision carries a real rationale, and
  accepted-baseline gaps are surfaced as visible governance debt — the research-sourced checks (**D7**);
- every decision's declared targets actually cite it (`coverage`, baseline-filtered);
- INDEX tables match `docs_manifest.txt` + orphan warning if a doc/SPEC isn't listed (`sync`/`docs`).

## Promotion note
This is **project-local** tooling. If multiple projects adopt it, consider promoting to a global
`/project:` skill via `skill-creator` (adds it to the shared framework + `agent_sync` scope).
