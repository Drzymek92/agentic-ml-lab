# Session Handoff — agentic_ml_lab

_Cold-start briefing. Overwritten at the end of each session._

## Worked On (2026-07-02)
Reviewed and **refreshed the project for the new machine**, then **published it to GitHub** as a
private repo. New machine is now built and running: Ubuntu 24.04 · Ryzen 7 9700X · RTX 5060 Ti 16GB
(Blackwell, `sm_120`) · NVIDIA driver 595.

## Completed
- **Blackwell/CUDA fix (critical)** — the pinned `torch==2.3.1` + SETUP's `cu124` had no `sm_120`
  kernels and would fail / fall back to CPU on the RTX 5060 Ti. Bumped `torch → 2.7.1` in
  `config/requirements.txt` + `environment.yml`; rewrote `SETUP.md §GPU` to require **cu128** with a
  device-name verify step and a note on GPU-accelerated boosting libs.
- **Linux-first setup** — `SETUP.md` reoriented from Windows to Ubuntu (target-machine banner,
  `source .venv/bin/activate`, `cp` for secrets, driver-595 prereq note).
- **Doc drift fixed** — `agent/project.md` run command pointed at a non-existent `scripts/main.py`;
  corrected to `python -m scripts.agentic_loop --demo` + new-competition command; recorded the
  Blackwell/cu128 requirement and the known governance test failure under Known Gotchas.
- **`.gitignore`** — added `_TEMPLATE` dir un-ignore rules so the template's `data/`, `models/`,
  `submissions/` placeholder folders survive a clone (needed for clean reconstruction, O1).
- **Published to GitHub** — `git init`, clean initial commit (no secrets/data), pushed to
  **https://github.com/Drzymek92/agentic-ml-lab** (private). Reconstruction steps in `SETUP.md`.

## Blockers / Known issues
- `tests/test_decision_tools.py::test_audit_goal_alignment` **still fails** — pre-existing
  project_init↔governance goal-format mismatch, unrelated to this project's code (background task).

## In Progress / Not Started
- **Reconstruct on the new PC**: `git clone` → `conda env create` → cu128 torch step → verify
  `torch.cuda.is_available()` + `nvidia-smi`. Not yet done on the new machine.
- **design/DECISIONS.md** D10+ not seeded (track choice; env strategy; loop principle; AIDE adoption).
- **Real `executor_fn`** (sandboxed candidate run → CV) — competition-specific, still to write.
- **GPU boosting libs** — xgboost/lightgbm/catboost pinned at CPU-safe versions; bump + re-pin if
  `device="cuda"` is wanted on the 5060 Ti.

## Next Steps
1. On the new PC: clone the repo and follow `SETUP.md` (esp. §GPU cu128); confirm the GPU is used.
2. Per competition: `python scripts/new_competition.py <slug>`, write its `executor_fn`, then
   `run_search(llm_fn=make_fuelix_llm(), executor_fn=..., context=...)`.
3. Resolve the governance goal-format gap so the full suite goes green.
4. Re-pin the resolved cu128 `torch` version into `config/requirements.txt` after the GPU install.
