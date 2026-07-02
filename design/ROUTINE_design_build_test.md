# Routine — the Design → Build → Test loop (orchestration)

The **inner loop** the agent runs while moving a project through the methodology stages
(`../METHODOLOGY.md`). It nests inside stages 1–4 and calls the decision routine
(`ROUTINE_add_decision.md`) whenever a choice is made. Goal: **minimize tokens, maximize coherence,
pinpoint decisions** — by working from a scoped context, scripting the mechanical edits, and gating
every iteration on `check`/`coverage`.

```
 ┌── PLAN ──────────────┐   ┌── BUILD ─────────────┐   ┌── TEST ──────────────┐
 │ scope → pinpoint D#  │ → │ edit ONLY in scope   │ → │ check + coverage gate │ ─┐
 │ new (if deciding)    │   │ propagate (cited)    │   │ stats (record loop)   │  │
 │ name contracts (D2)  │   │ batch in one pass    │   │ refresh working_set   │  │
 └──────────────────────┘   └──────────────────────┘   └───────────────────────┘  │
        ▲────────────────────────── next iteration ───────────────────────────────┘
```

Run scripts from the project root (`$PY scripts\decision_tools.py <cmd>`).

## PLAN — pinpoint what's in play (scoped context feed, D3)
1. State the goal in one line.
2. **`scope <selectors>`** — resolve the working set: the decisions in play (statements inline) and
   *only* the docs that carry them, each with the heading to jump to. Read **just those** — not the
   whole design tree. This is the token-saver (D3). Selectors: a `D#`, a `P#`/`G#`, a doc/path
   fragment, or a keyword. Pin the set with `--pin` (→ `agent/working_set.md`); bare `scope` re-reads it.
3. If the goal **requires a decision**, run **`new "<label>" <CATEGORY>`** and follow
   `ROUTINE_add_decision.md`. If it only *applies* existing decisions, skip — don't mint noise.
4. Name the **contracts** to stand up first (data shapes, signatures, file layout) so later steps
   *populate, not restructure* (contracts-first, D2).

## BUILD — edit only within the working set
5. Make the change against the contracts; touch only files in the scoped set.
6. **`propagate <D#>`** scripts the mechanical citation edits into a decision's declared targets
   (propose-by-default; `--apply` to write, D4). Do the *semantic* edits by hand.
7. **Batch** all edits in one pass (parallel), append-don't-splice, read each target once
   (Principles 3 & 5). Add one line to `docs_manifest.txt` if a doc/code file was created.

## TEST — gate the iteration on coherence (D5)
8. **`sync` → `check` → `coverage`** — the per-iteration gate: `check` prints **OK**, `coverage` is
   **0 new**. These keep the *docs* coherent the way tests keep the *code* coherent. (If the project
   has a runnable pipeline, run its tests here too.)
9. **`stats`** — append a metrics row (autotracking) so churn/coverage-gap/breadth trends accrue;
   `tune` later turns those into config-knob tweaks.
10. Refresh `agent/working_set.md` (next iteration's scope) and, at session end, `agent/session.md`.

## Why this stays cheap and coherent
- **Token economy:** every iteration reads the *scoped* set, never the whole repo (D3, Principle 7).
- **Coherence:** the `check`/`coverage` gate runs every loop, not just at the end (D5).
- **Decision pinpointing:** `scope`/`new` make the `D#`s in play explicit before any edit (D3).
- **Anti-rework:** contracts-first (D2) + just-in-time depth means later loops populate seams rather
  than restructure.
