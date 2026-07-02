# Session Handoff — agentic_ml_lab

_Cold-start briefing. Overwritten at the end of each session._

## Worked On (2026-06-24)
Stood up the **agentic ML / Kaggle workstation** (portable, GitHub-bound, reconstructable on a new PC),
then did a **complementary research pass** and turned the findings into a runnable orchestrator.

## Completed
- **Scaffold + env spec + Kaggle skeleton + agent hooks** (round 1) — see project.md. Reproducible env
  (`config/requirements.txt`, `environment.yml`), `SETUP.md`, `competitions/_TEMPLATE/` +
  `scripts/new_competition.py`, `scripts/seed.py`.
- **Research, round 1** — 5 papers (MLE-bench, MLE-STAR, SELA, AutoML-Agent, Data Interpreter) → KB +
  `documentation_processed/agentic_ml_research_digest.md`.
- **Research, round 2 (complementary)** — 3 papers (AIDE, Teaching LLMs to Self-Debug, AgentCoder) →
  KB (now 76 docs). Digest extended with "the loop mechanics".
- **Pipeline update** — built `scripts/agentic_loop.py`: AIDE-style **solution-tree search**
  (draft/improve/debug operators, greedy selection, `max_steps`/`max_debug_total` budgets, injected
  `llm_fn`/`executor_fn`, seeded). New prompts `draft_solution.md` + `debug_fix.md`; `agent_hooks/
  README.md` rewritten around the loop. **Verified**: `python -m scripts.agentic_loop --demo` runs
  end-to-end; `tests/test_agentic_loop.py` 4 passed.
- **Plumbing fixes** — added `scripts/__init__.py` (local `scripts` was being shadowed by an anaconda
  site-packages `scripts`), `pytest.ini` (`pythonpath=.`), and a sys.path insert in `tests/conftest.py`.

## Blockers / Known issues
- `tests/test_decision_tools.py::test_audit_goal_alignment` **fails** — pre-existing
  project_init↔governance Goals-format mismatch (the governance test hard-codes the template's `O#`
  placeholder lines; project_init's project.md uses free-text goals). **Not caused by this work.**
  Flagged as a background task ("Fix project_init↔governance goal-format gap").

## In Progress / Not Started
- **GitHub repo**: still deferred by choice → `/project:github_portfolio` when ready.
- **design/DECISIONS.md** D9+ not seeded yet (track choice; env strategy; "LLM-proposes/code-disposes"
  loop principle; AIDE tree-search adoption).
- **Real `executor_fn`** (sandboxed candidate run → CV) is competition-specific, still to write.

## Next Steps
1. Per competition: `python scripts/new_competition.py <slug>`, write its `executor_fn`, then
   `run_search(llm_fn=make_fuelix_llm(), executor_fn=..., context=...)`.
2. Resolve the governance goal-format gap (background task) so the full suite goes green.
3. (Optional) Seed governance decisions; instrument cost-per-step to tune `max_steps`/`max_debug_total`.
4. When ready: push to GitHub; on the new PC follow `SETUP.md` (incl. CUDA torch).
