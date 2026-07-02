# Changelog

_Entries added here as logic is clarified or changed. Newest first._

## 2026-06-24 — updated — research round 2 + pipeline orchestrator
- Complementary research: gathered AIDE, Teaching LLMs to Self-Debug, AgentCoder into the resources KB
  (the loop-mechanics gap). Digest extended in `agentic_ml_research_digest.md`.
- Built `scripts/agentic_loop.py` — AIDE-style solution-tree search (draft/improve/debug operators,
  greedy selection, `max_steps`/`max_debug_total` budgets, injected llm+executor, seeded). Added
  prompts `draft_solution.md` + `debug_fix.md`; rewrote `agent_hooks/README.md` around the tree loop.
  Verified: `python -m scripts.agentic_loop --demo` + `tests/test_agentic_loop.py` (4 passed).
- Added `scripts/__init__.py` (was missing from scaffold — local `scripts` was shadowed by an anaconda
  site-packages `scripts`) and `pytest.ini` (`pythonpath=.`); conftest now inserts the project root.
- KNOWN: `tests/test_decision_tools.py::test_audit_goal_alignment` fails on this scaffold — a
  pre-existing project_init↔governance Goals-format mismatch (governance test hard-codes the template's
  `O#` placeholder lines, which project_init's project.md doesn't use). Flagged for a separate fix.

## 2026-06-24 — created — research/agentic-ml-automation-kaggle
- Gathered 5 sources on "agentic AI for ML / Kaggle competitions" into the shared resources KB
  (MLE-bench, MLE-STAR, SELA, AutoML-Agent, Data Interpreter). Synthesis in
  `documentation_processed/agentic_ml_research_digest.md`; full text reusable via `resources_kb query`.
- Scoped to the KB gap: general LLM-agent theory + ML production-readiness were already indexed, so the
  search targeted agentic ML *automation* specifically.
