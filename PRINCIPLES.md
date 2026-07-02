# Principles (what this template enforces)

These are the rules the governance system bakes in. They align with the repo-wide `CLAUDE.md`
(determinism-first, FuelIX delegation, token economy, file-maintenance). The two foundational ones
are recorded as decisions in the register (D1, D2) and cited from `agent/project.md`.

1. **Single source of truth + propagate (D1).** Every decision is *stated* once in
   `design/DECISIONS.md`. Every other doc *applies* it and **cites the `D#`** — never restates it.
   This is what kills drift: there is only one place to change a decision.

2. **Contracts-first, anti-rework (D2).** Build against the *final* contracts (data shapes, function
   signatures, interfaces) with seams/hooks for not-yet-built parts — so later stages *populate*,
   they don't *restructure*. Settle naming, package/layout, and cross-cutting shapes **early**, when
   changing them is one edit instead of a hundred.

3. **Determinism first.** Anything a script can compute or verify — IDs, counts, glance lines, index
   tables, citation coverage — is owned by `decision_tools.py`, not done by hand. Reserve human/LLM
   effort for judgment (the design, the contracts, picking propagation targets). The mechanical
   *edits* and metrics are scripted too (`scope`/`propagate`/`tune`/`stats`), but **propose-first:
   they print by default and write only on `--apply` (D4)** — automation without surrendering the
   apply gate.

4. **Just-in-time design.** Design one priority ahead of the stage you're building (see
   `OPEN_DESIGN.md`). Don't fully specify late stages while early ones are unbuilt — they'll drift.

5. **Propagate in one batch.** When a decision lands, make all its edits in a single pass
   (parallel), append-don't-splice to avoid re-reads, then run `sync` → `check` → `coverage`.

6. **Compact output.** The register + `check`/`coverage` are the audit trail, so summaries stay
   short: the decision + id, a small propagation table, the gate result, the next action.

7. **Token economy.** Offload bulk/mechanical LLM work to the cheap gateway (FuelIX per `CLAUDE.md`);
   keep judgment, code, and orchestration in the main agent. Estimate before unbounded operations.

8. **Living files.** `agent/project.md` is the always-current source of truth; `agent/session.md` is
   overwritten each session as a cold-start briefing (not a changelog — the register is the history).

9. **Conformance over presence (D8).** The goal is to detect when a doc/code target has *drifted*
   from the decision it cites — not merely that it cites it. `coverage` proves presence; the
   **periodic `audit` (D9)** adds the conformance tier — a per-decision content hash flags **stale
   citations** when a decision changed but its docs weren't revisited. This is the software-research
   notion of **architecture erosion** (intended vs. implemented divergence) applied to governance;
   the model and its literature grounding live in [`design/REFERENCES.md`](design/REFERENCES.md).

10. **Periodic realignment, not just per-loop gating (D9).** The per-iteration `check`/`coverage` gate
    keeps each touched scope coherent but is blind to whole-tree drift and goal misalignment. On a
    cadence, the high-effort `audit` sweeps the entire tree, re-traces every decision to the project
    **goal (`O#`)** it advances (flagging scope creep and unaddressed objectives), and runs the drift
    check — emitting a severity-ranked remediation worklist. Periodic conformance checking is the
    field's standard remedy for erosion; propose-first (D4) keeps the apply gate human.
