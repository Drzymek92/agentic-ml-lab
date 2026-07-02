# Routine — Periodic Coherence + Realignment Audit (the high-effort pass)

The **periodic** counterpart to the per-iteration gate. The design→build→test loop
([`ROUTINE_design_build_test.md`](ROUTINE_design_build_test.md)) keeps **each touched scope** coherent
every loop (cheap, continuous). This routine steps back on a **cadence** and sweeps the **whole tree**
for the drift the scoped gate can't see — and re-checks that everything still serves the project's
**overall goal**. It applies **D9** (periodic realignment audit) and implements the conformance tier
**D8** set as direction. One command does the mechanical sweep:
`decision_tools.py audit` (propose-first, D4).

> Why a separate pass? The loop gate (`check`/`coverage`) only ever sees the files you edited this
> iteration. Accumulated, whole-tree problems — a decision that quietly drifted from its citing docs,
> a goal nothing advances anymore, baselined debt accreting — are invisible loop-to-loop. Periodic
> conformance checking is the field's standard remedy for architecture erosion; see
> [`REFERENCES.md`](REFERENCES.md).

Run from the project root with Python 3.11+:
```
$PY = "C:\Users\michal.drzymaa\AppData\Local\anaconda3\python.exe"
& $PY scripts\decision_tools.py audit            # whole-tree worklist (writes nothing)
& $PY scripts\decision_tools.py audit --apply        # + run the lossless mechanical fixes
& $PY scripts\decision_tools.py audit --update-hashes # re-stamp the drift baseline (after re-review)
```

## When to run it (cadence — periodic, not every loop)
Run at a **boundary**, not every iteration. Pick whichever fires first:
- a **METHODOLOGY stage transition** (rationale → build spec → implement → verify);
- **every ~N decisions** (watch `stats`' churn — a burst of decisions = time to re-sweep);
- **session start** when it's been a while (the loop gate covers within-session coherence);
- before a **handoff / milestone sign-off**.

## What `audit` sweeps (one ranked worklist)
Five dimensions, folded into a single severity-ranked list (3 = high):

1. **Whole-tree coherence** — the full `check` audit (IDs, GLANCE↔register, dangling/un-propagated
   cites, superseded-citation drift, rationale completeness) over the entire register + doc tree.
2. **Coverage debt — baseline-unfiltered.** Unlike the loop gate (which hides accepted gaps in
   `.coverage_baseline`), the audit surfaces **all** gaps, including baselined ones, as visible debt
   to schedule down (TD measurement + prioritization).
3. **Goal-alignment matrix (D# ↔ O#)** — re-trace every active decision to the project goal it
   advances. Flags **orphan decisions** (advance no stated goal → scope-creep / unanchored work) and
   **unaddressed goals** (a stated `O#` no decision advances). Needs a `## Goals` section in
   `agent/project.md` (see below); without it the audit just nudges you to add one.
4. **Drift / conformance (D8 slice)** — each decision carries a content hash. If a decision's
   statement/rationale/targets **changed since the last stamp**, its citing docs may no longer honor
   it → flagged as **stale citations** for re-review. Deterministic erosion detection, no NLP.
5. **Debt / churn signals** — the `tune` findings (superseded-rate, propagation-breadth spread,
   manifest orphans, coverage-gap trend).

## How to run it (the human half)
1. **`audit`** — read the worklist top-down (severity-first). Each finding tags `[mechanical]`
   (script can fix) or `[judgment]` (you decide).
2. **Clear judgment findings first** (they're the realignment work):
   - *orphan decision* → link it to the `O#` it serves (add the id to its register row) or retire it;
   - *unaddressed goal* → record a `D#` that advances it, or drop the goal;
   - *stale citation* → re-open each citing doc and confirm it still honors the changed decision; fix
     the prose that drifted. **This is the core anti-erosion step** — don't skip to re-stamping.
   - *coherence break* → run `check` for detail and fix per [`ROUTINE_add_decision.md`](ROUTINE_add_decision.md).
3. **`audit --apply`** — runs only the **lossless mechanical** fixes (prune resolved
   `.coverage_baseline`). Lossy/judgment knobs are never auto-applied (D4).
4. **`audit --update-hashes`** — *only after* you've re-reviewed the stale-citation flags. This
   re-stamps the conformance baseline, clearing the drift signals. Re-stamping asserts "I re-verified
   these" — it is a deliberate act, kept off `--apply` on purpose.
5. **Gate + record** — finish with `sync → check → coverage` (the loop gate) and note the audit in
   `agent/session.md`: what realigned, what debt was paid, what's deferred.

## The `## Goals` (O#) convention — what alignment traces against
For the goal-alignment matrix to work, `agent/project.md` must list the project's objectives with
stable ids, and decisions reference the goal(s) they advance:
```
## Goals
- O1: <the first objective the project must achieve>
- O2: <the second>
```
A decision advances a goal by **mentioning its `O#` in its register row** (e.g. append `(→ O1)` to the
statement). Same single-source-of-truth + cite-the-id discipline as `D#` propagation (D1): goals are
stated once in `project.md`; decisions point at them. `audit` then proves the linkage both ways.
(Goals with `<placeholder>` text are ignored, so a freshly-instantiated template stays quiet until you
fill real objectives in.)

## Why this stays cheap and honest
- **Determinism first:** every signal is computed from the register + citation graph + content
  hashes — nothing guessed (Principles 3).
- **Propose-first (D4):** `audit` writes nothing without `--apply` / `--update-hashes`; the human keeps
  the apply gate, especially on the re-review-then-restamp step.
- **Bounded cost:** it's a *periodic* pass, not a per-loop one — the expensive whole-tree sweep is
  amortized across many cheap iterations.
