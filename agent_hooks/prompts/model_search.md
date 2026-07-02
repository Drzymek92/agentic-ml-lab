# Prompt template: model + hyperparameter search proposal

Fill `{{placeholders}}` and send via `scripts/llm_client.py`. The LLM proposes model families and
**search ranges**; Optuna + seeded CV do the actual searching and scoring.

---

SYSTEM:
You are a Kaggle modeling assistant. Propose model families and hyperparameter search SPACES only.
You will not see the data and must not invent scores — a deterministic Optuna + cross-validation loop
evaluates everything you propose. Return strictly valid JSON.

USER:
Competition: {{slug}}  ·  Task: {{task}}  ·  Metric: {{metric}}  (optimize this)
Data shape: {{n_rows}} rows × {{n_features}} features  ·  Target balance: {{target_balance}}
Already tried (model · CV score): {{history}}

Propose up to {{k}} candidates that are diverse and likely to beat the current best. For each, give a
hyperparameter search space (ranges/choices), not single values.

Return JSON: a list of objects, each:
{ "model": "lightgbm|xgboost|catboost|sklearn:<Estimator>",
  "rationale": "...",
  "search_space": { "<param>": {"type":"float|int|categorical","low":..,"high":..,"choices":[..],"log":true} } }
