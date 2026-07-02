# Findings Digest — Agentic AI for ML / Kaggle competitions

_Gathered 2026-06-24 into the shared resources KB
(`resources/files/research/agentic-ml-automation-kaggle/`). Pull full text via
`/project:librarian` or `resources_kb query "<question>"`._

## One-paragraph answer
The state of the art in **agentic ML for competitions** is a small family of LLM-agent systems that
turn a Kaggle-style task ("here's the data + metric, maximize it") into an **iterative, search-driven
pipeline** rather than a single code-generation pass. They share four moves: (1) **plan then execute**
the ML pipeline in stages (EDA → preprocessing → feature engineering → model → ensemble); (2) **search
the solution space** instead of trusting one attempt — Monte-Carlo Tree Search over pipeline configs
(SELA), web-retrieval of strong models + targeted block-level refinement (MLE-STAR), or multi-agent
parallel plans (AutoML-Agent); (3) **execute real code and learn from measured feedback** (CV scores,
errors) — the agent proposes, a sandbox runs and scores; and (4) **honest evaluation** against a
held-out grader that mirrors the leaderboard (MLE-bench). The recurring lesson for our workstation:
the LLM is best used to *propose* hypotheses/configs/refinements, while **deterministic code executes
and scores** them — which is exactly the `agent_hooks/` loop design (LLM proposes, code disposes).

## Per-source contribution
- **MLE-bench: Evaluating Machine Learning Agents on ML Engineering** (2024, OpenAI; ICLR 2025) —
  `mle_bench_evaluating_machine_learning_agents_on_machine_lear_121fc6.pdf`. An **offline Kaggle
  environment** of 75 real competitions: each agent gets the description, dataset, and *local grading
  code*, and submissions are scored against the real human leaderboard (bronze/silver/gold medals).
  The yardstick for "can an agent do Kaggle." Strongest scaffold reported = **AIDE**; best model+scaffold
  earned at least a bronze in ~17% of competitions. Use it as our north-star evaluation framing.
- **MLE-STAR: ML Engineering Agent via Search and Targeted Refinement** (2025, Google) —
  `mle_star_machine_learning_engineering_agent_via_search_and_t_e85a08.pdf`. SOTA on MLE-bench at
  publication. Two key ideas: **web-search to retrieve effective, task-appropriate models** as a
  starting point (instead of the LLM's stale default), and **ablation-driven targeted refinement** —
  improve one code block at a time guided by measured impact — plus a learned **ensembling** strategy.
  Directly informs our `error_triage` / `model_search` hooks.
- **SELA: Tree-Search Enhanced LLM Agents for Automated ML** (2024, DeepWisdom/MetaGPT) —
  `sela_tree_search_enhanced_llm_agents_for_automated_machine_l_2e79fd.pdf`. Represents pipeline
  configurations as a **tree and runs MCTS** over them, so the agent explores diverse stage choices
  (encoding, scaling, PCA, model, stacking) and refines via experimental feedback. 65–80% win rate vs
  traditional AutoML and single-pass LLM baselines over 20 datasets. The model-search blueprint.
- **AutoML-Agent: Multi-Agent LLM Framework for Full-Pipeline AutoML** (2024, Trirat et al.) —
  `automl_agent_a_multi_agent_llm_framework_for_full_pipeline_a_ea800c.pdf`. A **multi-agent**
  decomposition (planning + specialized data/model agents) covering the whole pipeline from data
  retrieval to deployment, with **retrieval-augmented planning** and parallel plan exploration +
  verification. Shows where multi-agent specialization helps vs a single agent.
- **Data Interpreter: An LLM Agent for Data Science** (2024, Hong et al., MetaGPT) —
  `data_interpreter_an_llm_agent_for_data_science_19a21f.pdf`. Models the workflow as a **dynamic
  hierarchical graph (DAG of tasks)** with programmable node generation, tool integration, and logical
  consistency checks, so the plan adapts as data realities emerge. The "structured plan that adapts"
  pattern.

## Key techniques to reuse (each attributed)
- **Search > single pass.** Never trust one generated solution; explore a space — MCTS over configs
  (SELA) or ablation-guided block refinement (MLE-STAR).
- **Retrieve strong priors.** Seed the search with externally-retrieved good models/approaches rather
  than the LLM's defaults (MLE-STAR's web search; AutoML-Agent's retrieval-augmented planning).
- **Plan as an adaptive graph, execute stage-by-stage** with verification at each node (Data
  Interpreter; AutoML-Agent).
- **Measured feedback only.** Decisions are driven by *executed* CV/metric results, not the model's
  claimed numbers (all five) → enforces our determinism-first, seeded-run discipline.
- **Grade honestly against a leaderboard-mirroring split** (MLE-bench) → our `experiment.yaml` CV
  scheme + "trust CV over public LB" rule.

## Gaps / not covered (candidates for a later pass)
- **AIDE** itself (the strongest MLE-bench scaffold) was referenced but not ingested — worth adding.
- **Reproducibility / seeding discipline** for agent loops is assumed, not studied here; the
  ML-engineering-practice side is covered elsewhere in the KB (ML Test Score, MLTRL).
- **Compute/token-cost budgeting** of agentic search loops (how many trials are worth it) is thin —
  relevant once we run these for real on the new PC.
- These are **research systems**, not turnkey tools; our `agent_hooks/` adapt the *patterns*, wired
  through the standard FuelIX connection.

---

## Complementary pass (2026-06-24, round 2) — the loop mechanics
Gathered 3 more sources to fill the "how does the refine/debug loop actually work" gap, and used them
to build the runnable orchestrator `scripts/agentic_loop.py`.

- **AIDE: AI-Driven Exploration in the Space of Code** (2025, Weco AI) —
  `aide_ai_driven_exploration_in_the_space_of_code_207dff.pdf`. Frames ML engineering as **tree search
  over solutions**: each node is a full Python script; three operators grow the tree — **draft** (new
  solution), **debug/fix** (repair a buggy node), **improve** (refine a valid one) — with **greedy
  selection** toward the best validation metric. The strongest reported MLE-bench scaffold (o1-preview
  + AIDE: ~36% any-medal). **This is the blueprint our `agentic_loop.py` implements directly.**
- **Teaching Large Language Models to Self-Debug** (Chen et al., 2023) —
  `teaching_large_language_models_to_self_debug_279439.pdf`. Shows an LLM can fix its own code from
  **execution feedback** (run results + an explanation, "rubber-duck" style) with no extra training.
  Grounds the **debug operator**: we feed the real traceback back (`prompts/debug_fix.md`).
- **AgentCoder: Multi-Agent Code Generation with Iterative Testing and Optimisation** (2023) —
  `agentcoder_multi_agent_based_code_generation_with_iterative_833eda.pdf`. Separates a *programmer*
  agent from a *test/executor* agent and iterates on execution results. Reinforces the core split:
  **generation is the LLM's job; execution + scoring is code's job** — the loop's invariant.

### How the pipeline changed
- Added **`scripts/agentic_loop.py`** — AIDE-style solution-tree search (draft/improve/debug, greedy
  selection, `max_steps` + `max_debug_total` budgets), with injected `llm_fn`/`executor_fn`, seeded.
  `--demo` runs it end-to-end on stubs; `tests/test_agentic_loop.py` covers the tree + selection logic.
- Added operator prompts **`prompts/draft_solution.md`** and **`prompts/debug_fix.md`**; rewrote
  `agent_hooks/README.md` around the tree-search loop.

### Still-open gaps
- **Compute/token-budget tuning** of the search (how many steps/debugs pay off) — discovery surfaced
  little; revisit with real runs on the new PC, instrumenting cost per step.
- The real **`executor_fn`** (sandboxed run of a candidate that returns the CV) is competition-specific
  and still to be written per competition.
