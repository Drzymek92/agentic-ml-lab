"""Tests for the agentic solution-tree search loop (stubbed LLM + executor — no live model/data)."""
from __future__ import annotations

import re

from scripts.agentic_loop import (
    EvalResult,
    SolutionTree,
    extract_code,
    run_search,
    select_action,
)


def test_extract_code_pulls_fenced_block() -> None:
    assert extract_code("blah\n```python\nx = 1\n```\nend") == "x = 1"
    assert extract_code("no fences here") == "no fences here"


def test_tree_best_respects_direction() -> None:
    tree = SolutionTree(higher_is_better=True)
    tree.add("draft", "a", EvalResult(0.7), None)
    tree.add("draft", "b", EvalResult(0.9), None)
    tree.add("draft", "c", EvalResult(None, "err"), None)
    assert tree.best().metric == 0.9
    assert len(tree.scored()) == 2 and len(tree.buggy()) == 1

    low = SolutionTree(higher_is_better=False)
    low.add("draft", "a", EvalResult(0.7), None)
    low.add("draft", "b", EvalResult(0.9), None)
    assert low.best().metric == 0.7


def test_select_action_prioritises_debug_then_improve() -> None:
    tree = SolutionTree()
    assert select_action(tree, 3) == ("draft", None)          # empty -> draft

    tree.add("draft", "a", EvalResult(0.8), None)
    op, node = select_action(tree, 3)
    assert op == "improve" and node.metric == 0.8             # valid best -> improve

    tree.add("draft", "b", EvalResult(None, "boom"), None)
    op, node = select_action(tree, 3)
    assert op == "debug" and node.status == "buggy"           # buggy present -> debug
    op, _ = select_action(tree, 0)
    assert op == "improve"                                    # no debug budget -> improve instead


def test_run_search_climbs_and_recovers_from_a_bug() -> None:
    drafts = iter(["print('CV_SCORE: 0.80')", "raise ValueError('boom')"])

    def stub_llm(prompt: str) -> str:
        if "traceback" in prompt.lower():
            return "```python\nprint('CV_SCORE: 0.83')\n```"
        try:
            return f"```python\n{next(drafts)}\n```"
        except StopIteration:
            return "```python\nprint('CV_SCORE: 0.90')\n```"

    def stub_executor(code: str) -> EvalResult:
        if "raise" in code:
            return EvalResult(None, "ValueError: boom")
        m = re.search(r"CV_SCORE:\s*([0-9.]+)", code)
        return EvalResult(float(m.group(1)) if m else None, None if m else "no score")

    tree = run_search(
        llm_fn=stub_llm, executor_fn=stub_executor,
        context={"slug": "t", "metric": "auc"},
        max_steps=6, n_initial_drafts=2, seed=7,
    )
    # a buggy node was produced AND recovered; best keeps the highest valid metric
    assert any(n.status == "buggy" for n in tree.nodes)
    assert any(n.op == "debug" for n in tree.nodes)
    assert tree.best() is not None and tree.best().metric >= 0.83
