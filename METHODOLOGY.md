# Methodology — moving a project through stages without rewriting

The lifecycle this template supports. Each stage produces durable artifacts the next stage *builds
on* rather than replaces. Governance (decisions + propagation + coverage) runs **across all stages**.

```
 concept ──► rationale ──► build spec ──► implement ──► verify
 (project.md) (design/NN)  (design/build/  (milestones,   (acceptance
              the WHY      SPEC_* the HOW)  contracts-first) per milestone)
        └──────────────── decision governance (D#) runs across all ───────────────┘
```

## Stages

**0 · Concept** — `agent/project.md`: purpose, vision, scope, constraints. The first real decisions
(scope, track) get recorded as `D#`.

**1 · Rationale (the *why*)** — `design/NN_*.md` notes capture *why* the design is shaped this way.
Each meaningful choice → a `D#` in `DECISIONS.md`, cited from the note. Open questions go to
`OPEN_DESIGN.md` as gaps (G#).

**2 · Build spec (the *how*)** — `design/build/SPEC_*.md`: golden rules, data contracts (shapes),
module specs (signatures), and **milestones with acceptance criteria**. SPECs are authoritative when
building; rationale notes are read only when a decision is unclear.

**3 · Implement** — build milestone by milestone, **contracts-first + seams (D2)**: stand up the
final interfaces with no-op hooks for later parts, so subsequent milestones populate rather than
restructure. This is where "reducing rewriting" is won or lost.

**4 · Verify** — each milestone has acceptance criteria; check them. `check` + `coverage` keep the
*docs* coherent the same way tests keep the *code* coherent.

## The coherence loop (every decision, any stage)
1. `decision_tools.py new "<label>" <CATEGORY>` → scaffolds the register row + GLANCE + prints targets.
2. Fill the statement; write the *semantic* edits in the targets (each **cites the `D#`**).
3. If a doc/code file was added, add one line to `docs_manifest.txt`.
4. `sync` (regenerate glance/counts/INDEX tables) → `check` (coherence) → `coverage` (declared
   targets cite it) → note in `session.md`. See `design/ROUTINE_add_decision.md`.

## The inner loop (within any stage)
Stages 1–4 are run as a tight **design→build→test loop (D5)**: `scope` to pinpoint the decisions in
play and feed **only** their docs into context (**scoped context, D3**) → build against contracts →
gate on `check`/`coverage` (+ tests) every iteration → `stats` to track. The full protocol is
[`design/ROUTINE_design_build_test.md`](design/ROUTINE_design_build_test.md); it calls the
add-decision routine whenever a choice is made.

## The periodic audit (across stages)
The inner loop keeps **each touched scope** coherent; it can't see whole-tree drift or whether the
work still serves the project's goals. On a **cadence** — stage transitions, every ~N decisions, or
session start — run the high-effort **realignment audit (D9)**: `audit` sweeps the whole tree for
coherence + coverage debt, traces every decision to the goal it advances (the goal-alignment matrix),
and flags **stale citations** where a decision drifted from its docs (the conformance slice **D8**
pointed at). It's the periodic counterpart to the per-loop gate — see
[`design/ROUTINE_coherence_audit.md`](design/ROUTINE_coherence_audit.md).

## Anti-rework practices (why stages don't collapse backward)
- **Settle cross-cutting shapes early**: naming, package/layout, the core data contracts, the
  resolution/parameter formulas. Changing these late is the most expensive rewrite.
- **Just-in-time depth**: fully specify only the stage you're about to build; keep later stages as
  `OPEN_DESIGN` priorities until their turn.
- **One reasoning pass per decision**: decide, record, propagate in a batch — don't re-litigate.

## Track fit
This is the **freeform/design** governance layer. If the project grows a runnable pipeline, scaffold
that with `/project:project_init` and keep using this template's register + tooling alongside it.
