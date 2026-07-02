# Project: agentic_ml_lab

## Purpose
A portable, reproducible workstation for running **agentic ML workflows on Kaggle competitions**.
It bundles (a) a pinned ML/data-science environment, (b) a standard competition-project skeleton, (c)
a research knowledge base on agentic ML, and (d) reusable agent/automation hooks — so the whole setup
can be committed to GitHub here and reconstructed identically on a new PC currently being built.

## Goals
_Stable `O#` ids so the realignment audit (D9) can trace each decision back to the goal it advances._
- O1: **Reconstruct cleanly on the new machine** from a single env spec + setup script (no manual fiddling).
- O2: **Drop-in Kaggle competitions**: a `competitions/<slug>/` skeleton ready for data, EDA, features,
  models, and submissions, with reproducible (seeded) runs.
- O3: **Grounded research base**: curated academic sources on agentic ML / AutoML agents / ML-engineering
  best practice, ingested into the shared `resources/` KB + a synthesized digest committed as docs.
- O4: **Reusable agent loops**: prompt templates + helpers for agentic feature-engineering / model-search
  iterations that run via the standard FuelIX connection — determinism-first, seeded, reproducible.

## Status
Active

## Key Commands
- Run (demo of the agentic loop): `python -m scripts.agentic_loop --demo`
- New competition: `python scripts/new_competition.py <kaggle-slug>`
- Test: `pytest tests/`
- Lint: `ruff check .` (ruff not installed on current machine — runs on the new PC)
- Format: `black .`
- Bootstrap env: see `config/environment.yml` / `config/requirements.txt` and `SETUP.md`

## Stack
- Python 3.11+
- pandas, numpy, scipy
- scikit-learn
- pyarrow (parquet I/O)
- matplotlib, seaborn (EDA)
- jupyterlab (notebooks)
- xgboost, lightgbm, catboost (gradient boosting — Kaggle staples)
- optuna (hyperparameter search)
- torch (deep learning; GPU on the new PC)
- kaggle (competition data + submission CLI/API)
- langchain-openai (FuelIX LLM gateway — agentic loops)
- python-dotenv, pyyaml
- pytest
- (versions pinned in `config/requirements.txt`)

## Data Sources
- Input: Kaggle competition datasets (downloaded via the `kaggle` API into `competitions/<slug>/data/`)
- Format: CSV / Parquet / images, per competition
- Volume: varies per competition (MBs to tens of GBs); large data is gitignored, fetched on demand

## Output / Deliverable
- Report type: Kaggle submission files (`submission.csv`) + experiment logs/metrics; research digest docs
- GDrive destination folder: NA (GitHub is the primary store for this project)
- Delivery schedule: NA (ad-hoc, per competition)

## Scripts
| Script | Purpose |
|---|---|
| `main.py` | Pipeline entry point (scaffold) |
| `agentic_loop.py` | AIDE-style solution-tree search orchestrator (draft/improve/debug; injected llm+executor; `--demo`) |
| `new_competition.py` | Scaffold `competitions/<slug>/` from the template |
| `seed.py` | Reproducibility helper — seed Python/NumPy/PyTorch from one call |
| `llm_client.py` | FuelIX LLM connection for agentic loops |
| `prompt_compressor.py` | Prompt compression before LLM calls |
| `logger.py` | Shared logger |
| `decision_tools.py` | Governance: sync/check/coverage over design decisions |

## File Structure Notes
- `competitions/<slug>/` — per-competition skeleton (data/ · notebooks/ · features/ · models/ ·
  submissions/ · experiment config). `data/` and `submissions/` are gitignored.
- `agent_hooks/` — reusable agentic-ML prompt templates + helpers (model-search, feature ideas).
- Research lives in the **shared repo-root `resources/` KB**, not inside this project, with a
  synthesized digest committed under `documentation_processed/`.

## External Integrations
- Kaggle API: token via `KAGGLE_USERNAME` / `KAGGLE_KEY` (or `~/.kaggle/kaggle.json`)
- FuelIX LLM gateway: `FUELIX_*` env vars (via `scripts/llm_client.py`)
- GitHub: repo for versioning + reconstruction on the new PC (via `github_portfolio` later)

## Environment Variables Required
See `config/.env.example`

## Policy Overrides
<!-- Waive or replace a general CLAUDE.md practice for THIS project. validator HONORS each row but
     ALWAYS reports it. Safety rules (security, syntax) CANNOT be waived. NA for none. -->
| Practice | Action | Reason |
|---|---|---|
| NA | | |

## Known Gotchas
- **Blackwell GPU / CUDA:** target machine is an RTX 5060 Ti (Blackwell, `sm_120`) on Ubuntu 24.04 with
  driver 595. PyTorch MUST be the **cu128** build (torch ≥ 2.7); older CUDA wheels (cu124 and below) have
  no `sm_120` kernels and fail or silently run on CPU. See `SETUP.md` §GPU. The pinned `torch` is a CPU
  baseline — swap to cu128 on the new PC and re-pin.
- **GPU boosting libs:** the pinned xgboost/lightgbm/catboost are CPU-safe but predate Blackwell; bump
  them if you want `device="cuda"` on the 5060 Ti.
- `tests/test_decision_tools.py::test_audit_goal_alignment` fails — pre-existing project_init↔governance
  goal-format mismatch, unrelated to this project's code (see `agent/session.md`).

## Open Questions
NA


## Governance (design + decision OS)
Governed with the **governance template** — locked design decisions live once in
[`design/DECISIONS.md`](../design/DECISIONS.md) (`D#`) and propagate + audit via
`scripts/decision_tools.py` (`sync` / `check` / `coverage`). Master entry point:
[`design/INDEX.md`](../design/INDEX.md); rules in [`PRINCIPLES.md`](../PRINCIPLES.md),
lifecycle in [`METHODOLOGY.md`](../METHODOLOGY.md). Pin the active scope in
[`agent/working_set.md`](working_set.md).

At a glance (auto-generated — `scripts/decision_tools.py sync`):

<!-- DECISIONS:GLANCE start (generated by scripts/decision_tools.py sync) -->
**D1–D9 active (9).** D1 single source of truth · D2 contracts-first anti-rework · D3 scoped context feed · D4 scripted edits, propose-first · D5 design→build→test loop · D6 freeform-track waivers · D7 research-sourced coherence checks · D8 conformance over presence · D9 periodic realignment audit.
<!-- DECISIONS:GLANCE end -->

