# agentic_ml_lab — Reconstruction Guide

How to rebuild this workstation identically on the **new PC**. Goal: clone the repo, run a few
commands, and have a working agentic-ML / Kaggle environment.

---

> **Target machine (2026-07):** Ubuntu 24.04 · Ryzen 7 9700X · RTX 5060 Ti 16GB (Blackwell, `sm_120`) ·
> NVIDIA driver 595 (already installed). Commands below assume Linux; Windows variants are noted inline.

## 0. Prerequisites on the new machine
- **Miniconda or Anaconda** (preferred — handles the native ML toolchain cleanly), or Python 3.11 + venv.
  Ubuntu 24.04 ships Python 3.12; use conda to get the pinned 3.11, or accept 3.12 with the venv path.
- **Git** + a GitHub account with access to this repo.
- **NVIDIA GPU** (RTX 5060 Ti): driver 595 already installed — verify with `nvidia-smi`. The GPU build
  of PyTorch below requires **CUDA 12.8 (cu128)** because Blackwell (`sm_120`) has no kernels in older
  CUDA wheels — see §GPU.

## 1. Clone
```bash
git clone <repo-url> agentic_ml_lab
cd agentic_ml_lab
```

## 2. Create the environment

**Conda (preferred):**
```bash
conda env create -f config/environment.yml
conda activate agentic_ml_lab
pip install -r config/requirements-dev.txt   # dev/test extras
```

**venv + pip (fallback):**
```bash
python3 -m venv .venv
source .venv/bin/activate         # Linux / macOS
# .venv\Scripts\activate          # Windows
pip install -r config/requirements.txt -r config/requirements-dev.txt
```

## 3. Secrets
```bash
cp config/.env.example config/.env       # Linux / macOS  (copy config\.env.example on Windows)
```
Fill in:
- **Kaggle**: `KAGGLE_USERNAME` / `KAGGLE_KEY` (from kaggle.com/settings → Create New Token), or drop
  `kaggle.json` at `~/.kaggle/kaggle.json` and `chmod 600` it.
- **FuelIX**: `FUELIX_*` for the agentic LLM loops (see the repo-level `skills/llm_connection.md`).

## 4. Verify
```bash
pytest tests/                              # governance + scaffold tests pass
python -c "import pandas, sklearn, xgboost, lightgbm, torch; print('core OK')"
kaggle competitions list                   # confirms Kaggle auth works
```

## 5. GPU build of PyTorch  {#gpu}
`requirements.txt` pins the **CPU** wheel so the repo installs anywhere. On this machine's RTX 5060 Ti
you must install the **CUDA 12.8 (`cu128`)** build — Blackwell (`sm_120`) has **no kernels in older
CUDA wheels** (`cu118`/`cu121`/`cu124`), so an older torch would error with *"no kernel image is
available for execution on the device"* or silently run on the CPU.
```bash
pip uninstall -y torch
pip install torch --index-url https://download.pytorch.org/whl/cu128   # cu128 REQUIRED for Blackwell
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"   # expect 2.7+  True
python -c "import torch; print(torch.cuda.get_device_name(0))"                  # expect RTX 5060 Ti
```
If cu128 wheels ever lag your driver, the latest stable index (`.../whl/cu129` etc. — check
https://pytorch.org/get-started/locally) works too; do **not** drop below cu128. Then re-pin the
resolved version back into `config/requirements.txt` so the GPU build is recorded.

**GPU-accelerated boosting (optional):** `xgboost==2.1.1` / `lightgbm` / `catboost` are pinned at
CPU-safe versions that predate Blackwell. CPU training works out of the box; if you want `device="cuda"`
on the 5060 Ti, bump to the current release of each (they added `sm_120` support in later builds), verify,
and re-pin.

## 6. Start a competition
```bash
python scripts/new_competition.py <kaggle-slug>     # scaffolds competitions/<slug>/ from the template
# then:
kaggle competitions download -c <kaggle-slug> -p competitions/<slug>/data
```

---

### Notes
- Version pins in `config/requirements.txt` are a **known-good baseline**; if resolution fails on the
  new PC, bump the offending pin, verify the stack (`pytest` + the import smoke test), and commit the
  updated pin so the lockstep stays reproducible.
- Large data (`competitions/*/data/`) and submissions are **gitignored** — fetch per competition.
