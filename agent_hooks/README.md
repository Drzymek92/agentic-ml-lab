# agent_hooks — reusable agentic-ML loop pieces

Prompt templates + helpers for running **agentic ML iterations** (feature ideation, model search,
error triage) over a Kaggle competition. They call the LLM through the standard FuelIX connection
(`scripts/llm_client.py`) — never a vendor SDK directly.

## Core principle: LLM proposes, code disposes
Determinism-first (the repo-wide rule) applies hard here:

- The **LLM proposes** hypotheses, feature transforms, model configs, code edits.
- **Deterministic scripts execute and score** them — CV, metrics, leaderboard numbers come from
  `scikit-learn` / the boosters on **seeded** runs, *never* from the model's mouth.
- The agent loop then feeds the *measured* result back for the next proposal.

This keeps every iteration reproducible and stops the LLM hallucinating scores. An agent that reports
a CV number it didn't compute is a bug, not a result.

## The loop — solution-tree search
The orchestrator is [`scripts/agentic_loop.py`](../scripts/agentic_loop.py). Following the pattern the
research converges on (AIDE 2025; SELA 2024; Chen et al. self-debug 2023; AgentCoder 2023), it grows a
**tree of candidate solutions** (each node = a complete Python script) under a fixed step budget:

```
seed_everything(seed); load experiment.yaml (CV scheme, metric)
  -> draft   : LLM writes a complete solution        (prompts/draft_solution.md)
  -> execute : run it; read the printed CV_SCORE      (deterministic — the only score that counts)
  -> select  : greedy — fix a buggy node, else improve the current best
       - debug   : repair a failed node, feeding the real traceback back  (prompts/debug_fix.md)
       - improve : refine the best valid node                             (prompts/model_search.md)
  -> repeat until the step budget is spent; emit the best node's submission
```
Budget controls (the test-time-compute knob): `max_steps` (total iterations) and `max_debug_total`
(cap on fixes, so a dead branch can't burn the whole budget). The LLM (`llm_fn`) and the candidate
**executor** (`executor_fn`) are injected — run `python -m scripts.agentic_loop --demo` for a stubbed
end-to-end run; wire `make_fuelix_llm()` + a competition executor for real.

## Contents
- `prompts/draft_solution.md` — write a complete runnable solution from the data summary (draft op).
- `prompts/debug_fix.md` — repair a failed script from its execution traceback (debug op / self-debug).
- `prompts/model_search.md` — propose model families + hyperparameter ranges (improve op / Optuna).
- `prompts/feature_ideas.md` — propose candidate feature transforms from a columns summary.
- `prompts/error_triage.md` — diagnose a CV/LB gap or underperformance from logs + CV output.

Each prompt is parameterized with `{{placeholders}}` filled from `experiment.yaml` + data summaries.
Keep prompts short; compress long context via `scripts/prompt_compressor.py` before sending.
