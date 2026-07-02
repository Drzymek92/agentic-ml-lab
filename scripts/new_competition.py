"""Scaffold a new Kaggle competition workspace from competitions/_TEMPLATE/.

Usage:
    python scripts/new_competition.py <kaggle-slug>

Copies the template, substitutes <slug> in the README/experiment.yaml, and prints the next steps.
Idempotent-ish: refuses to overwrite an existing competition folder unless --force is given.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = PROJECT_ROOT / "competitions" / "_TEMPLATE"


def scaffold(slug: str, force: bool = False) -> Path:
    if not TEMPLATE_DIR.is_dir():
        raise FileNotFoundError(f"Template not found: {TEMPLATE_DIR}")
    dest = PROJECT_ROOT / "competitions" / slug
    if dest.exists():
        if not force:
            raise FileExistsError(f"{dest} already exists (use --force to overwrite)")
        shutil.rmtree(dest)

    shutil.copytree(TEMPLATE_DIR, dest)

    # substitute <slug> placeholders in text stubs
    for rel in ("README.md", "experiment.yaml"):
        path = dest / rel
        text = path.read_text(encoding="utf-8").replace("<slug>", slug)
        path.write_text(text, encoding="utf-8")

    return dest


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold a Kaggle competition workspace.")
    parser.add_argument("slug", help="Kaggle competition slug (e.g. titanic)")
    parser.add_argument("--force", action="store_true", help="overwrite an existing folder")
    args = parser.parse_args()

    try:
        dest = scaffold(args.slug, force=args.force)
    except (FileNotFoundError, FileExistsError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    rel = dest.relative_to(PROJECT_ROOT)
    print(f"Scaffolded {rel}")
    print("Next:")
    print(f"  kaggle competitions download -c {args.slug} -p {rel}/data")
    print(f"  fill in {rel}/README.md  and  {rel}/experiment.yaml")


if __name__ == "__main__":
    main()
