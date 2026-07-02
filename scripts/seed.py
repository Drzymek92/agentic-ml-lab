"""Reproducibility helper — seed every RNG the ML stack touches from one call.

Determinism-first: a seeded run can be replayed exactly, which is the backbone of honest CV and of
any agentic loop that proposes/evaluates models. Import and call once at the top of a run.
"""
from __future__ import annotations

import os
import random


def seed_everything(seed: int = 42, *, deterministic_torch: bool = True) -> int:
    """Seed Python, NumPy, and (if installed) PyTorch. Returns the seed for logging.

    Args:
        seed: the global seed.
        deterministic_torch: if True, also force cuDNN into deterministic mode (slower but replayable).
    """
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)

    try:
        import numpy as np

        np.random.seed(seed)
    except ImportError:
        pass

    try:
        import torch

        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
        if deterministic_torch:
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
    except ImportError:
        pass

    return seed
