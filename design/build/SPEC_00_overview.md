# BUILD SPEC 00 — Overview, Layout & Golden Rules

The implementation contract starter. The `design/NN` notes explain *why*; the `SPEC_*` docs say
*what to build and in what order*. SPECs are authoritative when building.

## 1. Golden rules (apply to every module — adapt per project)
1. **Single source of truth (D1).** State each decision once in the register; code/docs cite the `D#`.
2. **Contracts-first + seams (D2).** Build against final interfaces; stub unbuilt parts as no-op
   hooks so later milestones *populate*, not *restructure*. Settle naming/layout/core shapes early.
3. **Determinism first.** Compute/verify with code what code can; reserve LLM/human effort for judgment.
4. **Secrets via env; pin dependencies** (if a runnable pipeline emerges).
5. **Type hints on function signatures; small, single-purpose modules.**

## 2. Repo layout (✅ exists · ◻ to build — adapt)
```
<project>/
├── README.md · PRINCIPLES.md · METHODOLOGY.md
├── agent/         project.md (living source of truth) · session.md (cold-start briefing)
├── design/
│   ├── INDEX.md · DECISIONS.md · ROUTINE_add_decision.md · OPEN_DESIGN.md · docs_manifest.txt
│   └── build/SPEC_*.md
├── scripts/       decision_tools.py (governance) + <project code>
└── <data/ tests/ … as the project needs>
```

## 3. Build order
Define milestones here (M1, M2, …), each with **acceptance criteria**, smallest shippable first.
Implement each contracts-first (D2); verify against its criteria before starting the next.

| Milestone | Delivers | Accept when |
|---|---|---|
| M1 | <first shippable slice> | <criteria> |
