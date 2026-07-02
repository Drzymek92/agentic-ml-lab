import sys
from pathlib import Path

import pytest
import pandas as pd
from unittest.mock import MagicMock

# Make `scripts` importable when running pytest from the project root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# ── paths ────────────────────────────────────────────────
@pytest.fixture
def fixtures_dir() -> Path:
    return Path(__file__).parent / "fixtures"

# ── env vars ─────────────────────────────────────────────
@pytest.fixture(autouse=True)
def mock_env(monkeypatch):
    monkeypatch.setenv("GDRIVE_SA_KEY_PATH", "fake/path/key.json")
    monkeypatch.setenv("GDRIVE_FOLDER_ID", "fake_folder_id")

# ── gdrive client ─────────────────────────────────────────
@pytest.fixture
def mock_gdrive():
    return MagicMock()

# ── sample dataframe ──────────────────────────────────────
@pytest.fixture
def sample_df() -> pd.DataFrame:
    return pd.DataFrame({
        "id": [1, 2, 3],
        "value": [10.0, 20.0, 30.0],
    })
