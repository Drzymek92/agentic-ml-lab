"""Agentic ML solution-tree search — the orchestration loop for a competition.

Implements the pattern the research converges on (AIDE 2025; SELA 2024; Chen et al. self-debug 2023;
AgentCoder 2023): the **LLM proposes complete solutions, deterministic code executes and scores
them**, and the loop searches a *tree* of solutions under a fixed step budget (the test-time-compute
control). Each node is a Python script; three operators grow the tree:

  - draft   : write a new solution from scratch (seed / diversify the tree)
  - improve : refine the best *valid* node toward a higher validation metric
  - debug   : repair a *buggy* node, feeding the real execution traceback back (self-debug)

Selection is greedy (AIDE): debug buggy nodes first, else improve the current best. The LLM and the
executor are **injected** so this file is importable and testable without a live model or dataset
(see `tests/test_agentic_loop.py` and the `--demo` mode).

Determinism-first: the loop is seeded; scores come only from `executor_fn`, never from the LLM.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.logger import get_logger
from scripts.seed import seed_everything

logger = get_logger("agentic_loop")

PROMPTS_DIR = Path(__file__).resolve().parents[1] / "agent_hooks" / "prompts"


# --- contracts (injected) ---------------------------------------------------
@dataclass
class EvalResult:
    """Outcome of executing a candidate script. `metric` is None when it failed to run."""
    metric: Optional[float]
    error: Optional[str] = None

    @property
    def ok(self) -> bool:
        return self.metric is not None and self.error is None


# llm_fn: prompt -> generated script text
LLMFn = Callable[[str], str]
# executor_fn: script text -> EvalResult (runs it, reads the printed CV)
ExecutorFn = Callable[[str], EvalResult]


# --- solution tree ----------------------------------------------------------
@dataclass
class Node:
    id: int
    op: str                       # draft | improve | debug
    code: str
    parent: Optional[int] = None
    metric: Optional[float] = None
    error: Optional[str] = None

    @property
    def status(self) -> str:
        if self.error is not None:
            return "buggy"
        if self.metric is not None:
            return "scored"
        return "empty"


@dataclass
class SolutionTree:
    higher_is_better: bool = True
    nodes: list[Node] = field(default_factory=list)

    def add(self, op: str, code: str, res: EvalResult, parent: Optional[int]) -> Node:
        node = Node(id=len(self.nodes), op=op, code=code, parent=parent,
                    metric=res.metric, error=res.error)
        self.nodes.append(node)
        return node

    def scored(self) -> list[Node]:
        return [n for n in self.nodes if n.status == "scored"]

    def buggy(self) -> list[Node]:
        return [n for n in self.nodes if n.status == "buggy"]

    def open_buggy(self) -> list[Node]:
        """Buggy nodes not yet debugged (no child). Each fix is a new child, AIDE-style, so a node
        is debugged at most once; an unresolved fix surfaces as a *new* open-buggy node (the chain)."""
        parents = {n.parent for n in self.nodes if n.parent is not None}
        return [n for n in self.buggy() if n.id not in parents]

    def best(self) -> Optional[Node]:
        scored = self.scored()
        if not scored:
            return None
        return max(scored, key=lambda n: n.metric if self.higher_is_better else -n.metric)


# --- prompt rendering -------------------------------------------------------
def render(template: str, **kw: object) -> str:
    """Fill a `{{placeholder}}` prompt template from agent_hooks/prompts/ (best-effort)."""
    path = PROMPTS_DIR / template
    text = path.read_text(encoding="utf-8") if path.exists() else template
    for key, val in kw.items():
        text = text.replace("{{" + key + "}}", str(val))
    return text


def extract_code(text: str) -> str:
    """Pull the first fenced code block from an LLM reply; fall back to the whole text."""
    m = re.search(r"```(?:python)?\s*(.*?)```", text, re.DOTALL)
    return (m.group(1) if m else text).strip()


# --- the loop ---------------------------------------------------------------
def select_action(tree: SolutionTree, debug_budget_left: int) -> tuple[str, Optional[Node]]:
    """Greedy policy: fix an un-debugged buggy node first (if budget remains), else improve the best."""
    if not tree.nodes:
        return "draft", None
    open_buggy = tree.open_buggy()
    if open_buggy and debug_budget_left > 0:
        return "debug", open_buggy[-1]      # most recent un-debugged failure
    best = tree.best()
    if best is not None:
        return "improve", best
    return "draft", None                    # only dead branches left, no budget → draft anew


def run_search(
    *,
    llm_fn: LLMFn,
    executor_fn: ExecutorFn,
    context: dict[str, object],
    max_steps: int = 12,
    n_initial_drafts: int = 2,
    max_debug_total: int = 6,
    higher_is_better: bool = True,
    seed: int = 42,
) -> SolutionTree:
    """Run the solution-tree search under a fixed step budget. Returns the populated tree.

    `max_steps` is the test-time-compute budget (total LLM+exec iterations); `max_debug_total` caps
    how many of those may be spent on fixes, so a dead branch can't exhaust the whole budget.
    """
    seed_everything(seed)
    tree = SolutionTree(higher_is_better=higher_is_better)
    debug_used = 0

    for step in range(max_steps):
        if step < n_initial_drafts or not tree.nodes:
            op, parent = "draft", None
        else:
            op, parent = select_action(tree, max_debug_total - debug_used)

        if op == "draft":
            prompt = render("draft_solution.md", **context)
        elif op == "improve":
            prompt = render("model_search.md", history=_history(tree), **context)
            prompt += f"\n\n--- current best solution (improve it) ---\n{parent.code}"
        else:  # debug
            prompt = render("debug_fix.md", code=parent.code, error=parent.error, **context)
            debug_used += 1

        code = extract_code(llm_fn(prompt))
        res = executor_fn(code)
        node = tree.add(op, code, res, parent.id if parent else None)
        best = tree.best()
        logger.info(
            "step %d/%d op=%s node=%d metric=%s status=%s best=%s",
            step + 1, max_steps, op, node.id,
            f"{res.metric:.5f}" if res.ok else "—", node.status,
            f"{best.metric:.5f}@{best.id}" if best else "none",
        )

    best = tree.best()
    if best is None:
        logger.warning("Search finished with no valid solution (%d nodes).", len(tree.nodes))
    else:
        logger.info("Best: node %d, %s=%.5f (%d nodes total).",
                    best.id, context.get("metric", "metric"), best.metric, len(tree.nodes))
    return tree


def _history(tree: SolutionTree) -> str:
    return "; ".join(f"node{n.id}:{n.op}={n.metric:.4f}" for n in tree.scored()) or "none yet"


# --- wiring helpers ---------------------------------------------------------
def make_fuelix_llm() -> LLMFn:
    """LLMFn backed by the standard FuelIX connection (scripts/llm_client.py)."""
    from scripts.llm_client import call_llm  # populated via the llm_connection skill

    def _fn(prompt: str) -> str:
        return call_llm(prompt)

    return _fn


def _demo() -> None:
    """Self-contained demo: stub LLM + stub executor prove the loop runs deterministically."""
    drafts = iter([
        "print('CV_SCORE: 0.80')",
        "raise ValueError('boom')",            # a buggy candidate -> triggers debug
        "print('CV_SCORE: 0.85')",
    ])

    def stub_llm(prompt: str) -> str:
        if "debugging" in prompt.lower() or "traceback" in prompt.lower():
            return "```python\nprint('CV_SCORE: 0.83')\n```"      # the fix
        try:
            return f"```python\n{next(drafts)}\n```"
        except StopIteration:
            return "```python\nprint('CV_SCORE: 0.88')\n```"      # 'improve' keeps climbing

    def stub_executor(code: str) -> EvalResult:
        if "raise" in code:
            return EvalResult(metric=None, error="ValueError: boom")
        m = re.search(r"CV_SCORE:\s*([0-9.]+)", code)
        return EvalResult(metric=float(m.group(1)) if m else None,
                          error=None if m else "no CV_SCORE printed")

    tree = run_search(
        llm_fn=stub_llm, executor_fn=stub_executor,
        context={"slug": "demo", "task": "classification", "metric": "auc"},
        max_steps=6, n_initial_drafts=2,
    )
    best = tree.best()
    print(f"\nDemo done. Best node {best.id} auc={best.metric} over {len(tree.nodes)} nodes.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Agentic ML solution-tree search.")
    parser.add_argument("--demo", action="store_true", help="run the stubbed demo (no LLM/data needed)")
    args = parser.parse_args()
    if args.demo:
        _demo()
    else:
        print("Wire llm_fn=make_fuelix_llm() and a competition executor_fn, then call run_search(). "
              "See --demo and agent_hooks/README.md.")


if __name__ == "__main__":
    main()
