# Competition: <slug>

> Scaffolded from `competitions/_TEMPLATE/`. Replace `<slug>` and fill the sections below.

## Problem
- **Task**: <classification / regression / ranking / ...>
- **Metric**: <e.g. AUC, RMSE, LogLoss>  (the leaderboard metric — optimize THIS)
- **Link**: https://www.kaggle.com/competitions/<slug>

## Data
- Files: <train.csv, test.csv, ...>  (downloaded into `data/`, gitignored)
- Target column: <name>
- Key gotchas: <leakage risks, group structure, time ordering, ...>

## Plan
1. EDA — `notebooks/01_eda.ipynb`
2. Baseline — simple model + honest CV split, establish a score floor
3. Features — `features/`
4. Models / tuning — `models/`, Optuna
5. Submit — `submissions/submission.csv`

## CV strategy
<How the validation split mirrors the leaderboard — e.g. StratifiedKFold(5), GroupKFold, time split.
Trust CV over public LB. Seed every split (see scripts/seed.py / experiment.yaml).>

## Log
| Date | Change | CV | Public LB |
|---|---|---|---|
|  |  |  |  |
