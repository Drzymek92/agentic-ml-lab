"""Subprocess characterization + regression tests for scripts/decision_tools.py.

Portable: each test runs against a fresh copy of *this* project (works in the template or any
project instantiated from it). Run with any Python 3.11+:
    $PY -m pytest tests/ -q
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

PROJ = Path(__file__).resolve().parents[1]
TOOL = "scripts/decision_tools.py"
_IGNORE = shutil.ignore_patterns("tests", "__pycache__", ".git", "governance_metrics.csv",
                                 ".coverage_baseline", ".decision_hashes", "*.pyc")


@pytest.fixture
def proj(tmp_path: Path) -> Path:
    dst = tmp_path / "p"
    shutil.copytree(PROJ, dst, ignore=_IGNORE)
    return dst


def run(proj: Path, *args: str) -> subprocess.CompletedProcess:
    # child emits UTF-8 (PYTHONIOENCODING); decode it as UTF-8 here, not the cp1252 locale default
    return subprocess.run([sys.executable, TOOL, *args], cwd=proj,
                          capture_output=True, text=True, encoding="utf-8",
                          env={**os.environ, "PYTHONIOENCODING": "utf-8"})


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def _add_decision(proj: Path, label: str, targets: str) -> int:
    """Append a decision via `new`, set its targets cell, return its id."""
    before = run(proj, "next").stdout.strip()
    nid = int(before.lstrip("Dd"))
    run(proj, "new", label, "PROCESS")
    dec = proj / "design" / "DECISIONS.md"
    t = _read(dec).replace(f"**{label.capitalize()}:** <STATEMENT — fill in> | <rationale doc> | <propagated to>",
                           f"**{label.capitalize()}:** test. | METHODOLOGY.md | {targets}")
    dec.write_text(t, encoding="utf-8")
    return nid


# --- core gates ----------------------------------------------------------------
def test_check_clean(proj):
    r = run(proj, "check")
    assert r.returncode == 0 and "OK — coherent" in r.stdout


def test_coverage_clean(proj):
    r = run(proj, "coverage")
    assert r.returncode == 0 and "clean" in r.stdout


def test_sync_idempotent(proj):
    run(proj, "sync")
    r = run(proj, "sync")
    assert "no changes" in r.stdout


# --- new: row lands after the last numbered row, not in the example block ------
def test_new_places_row_in_table(proj):
    run(proj, "new", "Placement probe", "PROCESS")
    lines = _read(proj / "design" / "DECISIONS.md").splitlines()
    rows = [i for i, l in enumerate(lines) if l.startswith("| D") and "<n>" not in l]
    example = next(i for i, l in enumerate(lines) if "| D<n> |" in l)
    assert max(rows) < example   # the real row sits above the example block


# --- scope ---------------------------------------------------------------------
def test_scope_resolves_decision(proj):
    r = run(proj, "scope", "D1")
    assert "D1:" in r.stdout and "Read (scoped" in r.stdout


def test_scope_reaches_rationale_tier(proj):
    # regression guard for the root-doc reach fix: D4's rationale is PRINCIPLES.md (root, not in SCAN_DIRS)
    r = run(proj, "scope", "D4")
    assert "PRINCIPLES.md" in r.stdout


def test_scope_pin_roundtrip(proj):
    run(proj, "scope", "D2", "--pin", "--files")
    assert "- D2" in _read(proj / "agent" / "working_set.md")
    assert "design/" in run(proj, "scope", "--files").stdout   # bare scope reads the pin


# --- stats ---------------------------------------------------------------------
def test_stats_writes_csv_with_new_columns(proj):
    run(proj, "stats", "--csv-only")
    csv = proj / "governance_metrics.csv"
    header = _read(csv).splitlines()[0]
    assert "propagation_breadth_spread" in header and "days_since_last_decision" in header


# --- propagate: closes a coverage gap mechanically -----------------------------
def test_propagate_closes_gap(proj):
    nid = _add_decision(proj, "Prop probe", "SPEC_00")          # SPEC_00 won't cite it
    assert run(proj, "coverage").returncode == 1                # 1 new gap
    assert run(proj, "propagate", f"D{nid}").returncode == 0    # dry-run, no write
    run(proj, "propagate", f"D{nid}", "--apply")
    assert run(proj, "coverage").returncode == 0                # gap closed
    assert f"D{nid}" in _read(proj / "design" / "build" / "SPEC_00_overview.md")


# --- research-sourced coherence checks (D7) ------------------------------------
def _supersede(proj: Path, nid: int) -> None:
    """Move D<nid>'s row to the Superseded section + drop its GLANCE line; docs still cite it."""
    dec = proj / "design" / "DECISIONS.md"
    lines = _read(dec).splitlines(keepends=True)
    row_i = next(i for i, l in enumerate(lines) if l.startswith(f"| D{nid} "))
    row = lines.pop(row_i).rstrip("\n") + "  SUPERSEDED by D99\n"
    lines = [l for l in lines if not l.strip().startswith(f"D{nid}=")]   # drop the GLANCE label
    text = "".join(lines).replace("## Superseded decisions\n", "## Superseded decisions\n" + row)
    dec.write_text(text, encoding="utf-8")


def test_check_flags_superseded_citation(proj):
    # CASCADE-style drift: D6 is still cited in agent/project.md after being superseded.
    _supersede(proj, 6)
    r = run(proj, "check")
    assert r.returncode == 1 and "SUPERSEDED" in r.stdout and "D6" in r.stdout


def test_check_flags_missing_rationale(proj):
    dec = proj / "design" / "DECISIONS.md"
    lines = _read(dec).splitlines(keepends=True)
    for i, l in enumerate(lines):
        if l.startswith("| D2 "):
            cells = l.split("|")
            cells[5] = " <rationale doc> "          # blank D2's rationale to a template stub
            lines[i] = "|".join(cells)
            break
    dec.write_text("".join(lines), encoding="utf-8")
    r = run(proj, "check")
    assert r.returncode == 1 and "rationale" in r.stdout and "D2" in r.stdout


def test_check_reports_governance_debt(proj):
    (proj / "scripts" / ".coverage_baseline").write_text("D1:design/INDEX.md\n", encoding="utf-8")
    r = run(proj, "check")
    assert "governance-debt" in r.stdout            # accepted baseline gap surfaced every audit


# --- audit: periodic whole-tree coherence + realignment pass (D9) --------------
def test_audit_runs_and_reports(proj):
    r = run(proj, "audit")
    assert "AUDIT — periodic coherence + realignment" in r.stdout
    # fresh copy has no drift baseline → every decision is unstamped
    assert "not yet conformance-stamped" in r.stdout


def test_audit_update_hashes_writes_baseline(proj):
    r = run(proj, "audit", "--update-hashes")
    assert r.returncode == 0 and "conformance baseline stamped" in r.stdout
    hashes = proj / "scripts" / ".decision_hashes"
    assert hashes.is_file() and "D1:" in _read(hashes)


def test_audit_drift_flags_changed_decision(proj):
    run(proj, "audit", "--update-hashes")                       # stamp the baseline
    dec = proj / "design" / "DECISIONS.md"
    # mutate D2's statement → its content hash changes → citing docs are stale
    t = _read(dec).replace("**Contracts-first, anti-rework:**", "**Contracts-first, anti-rework (EDITED):**")
    dec.write_text(t, encoding="utf-8")
    r = run(proj, "audit")
    assert "stale citation (drift)" in r.stdout and "D2" in r.stdout


def test_audit_no_drift_when_unchanged(proj):
    run(proj, "audit", "--update-hashes")
    r = run(proj, "audit")
    assert "stale citation" not in r.stdout                     # nothing changed since the stamp


def test_audit_goal_alignment(proj):
    # give project.md real goals (O1 referenced by D1, O2 referenced by nothing)
    proj_md = proj / "agent" / "project.md"
    t = _read(proj_md).replace("- O1: <the first objective this project must achieve>", "- O1: ship the thing")
    t = t.replace("- O2: <the second>", "- O2: an objective no decision advances")
    proj_md.write_text(t, encoding="utf-8")
    dec = proj / "design" / "DECISIONS.md"
    dec.write_text(_read(dec).replace("Coherence is enforced by",
                                      "(→ O1) Coherence is enforced by"), encoding="utf-8")  # link D1→O1
    r = run(proj, "audit")
    assert "no goals declared" not in r.stdout                  # real goals present now
    assert "goal has no decision" in r.stdout and "O2" in r.stdout      # O2 unaddressed
    assert "decision advances no goal" in r.stdout              # D2..D9 reference no O#


# --- tune: prune baseline is mechanical; glance-trim is propose-only (#4) -------
def test_tune_prunes_baseline_but_not_label(proj):
    (proj / "scripts" / ".coverage_baseline").write_text("D99:design/INDEX.md\n", encoding="utf-8")
    dec = proj / "design" / "DECISIONS.md"
    long_label = "scoped context feed with far too many words to ever fit the budget"
    dec.write_text(_read(dec).replace("D3=scoped context feed", f"D3={long_label}"), encoding="utf-8")
    r = run(proj, "tune", "--apply")
    assert "[judgment]" in r.stdout                              # glance flagged, not mechanical
    assert (proj / "scripts" / ".coverage_baseline").read_text(encoding="utf-8").strip() == ""
    assert long_label in _read(dec)                              # label left untouched
