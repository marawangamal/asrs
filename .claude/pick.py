#!/usr/bin/env python3
"""Pick next card(s) to review. Prints relative card path(s) to stdout, one per line.

Usage: python3 .claude/pick.py [deck_filter] [--count N]

Vault root is the script's parent directory. Decks are any directory containing
an index.md (searched recursively). Pass a deck filter as either the deck name
(e.g. "algos") or its relative path (e.g. "code/algos"). Pass --count N to print
the top N due cards instead of just one.
"""
from __future__ import annotations

import argparse
import math
import random
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

GRADE_MULTIPLIER = {"again": 0.5, "hard": 1.0, "good": 2.5, "easy": 5.0}
HEADER_RE = re.compile(
    r"^##\s+(?P<ts>\S+)\s+—\s+(?P<path>\S+)\s+—\s+(?P<grade>again|hard|good|easy)\s*$"
)
SKIP_DIRS = {"__pycache__", "node_modules", ".venv", ".git"}
MAX_DEPTH = 4


def find_decks(root: Path) -> list[Path]:
    """Find all dirs containing index.md, recursively. Don't descend into a deck."""
    decks: list[Path] = []

    def walk(path: Path, depth: int) -> None:
        if depth > MAX_DEPTH:
            return
        if path != root and (path / "index.md").is_file():
            decks.append(path)
            return
        for child in sorted(path.iterdir()):
            if child.is_dir() and child.name not in SKIP_DIRS and not child.name.startswith("."):
                walk(child, depth + 1)

    walk(root, 0)
    return decks


def parse_inactive(index_path: Path) -> set[str]:
    """Parse the `inactive:` list from a deck's index.md. Returns card filenames."""
    if not index_path.is_file():
        return set()
    inactive: set[str] = set()
    in_block = False
    for raw in index_path.read_text().splitlines():
        stripped = raw.strip()
        if not in_block:
            if stripped.startswith("inactive:"):
                in_block = True
                rest = stripped[len("inactive:"):].strip()
                if rest:
                    for item in rest.split(","):
                        item = item.strip()
                        if item:
                            inactive.add(item)
            continue
        if stripped.startswith("- "):
            inactive.add(stripped[2:].strip())
        elif stripped == "" or stripped.startswith("#"):
            continue
        else:
            in_block = False
    return inactive


def find_cards(deck: Path) -> list[Path]:
    inactive = parse_inactive(deck / "index.md")
    return sorted(
        p for p in deck.iterdir()
        if p.is_file() and p.suffix == ".md" and p.name != "index.md" and p.name not in inactive
    )


def parse_history(history_path: Path) -> dict[str, tuple[datetime, str]]:
    """Return {relative_card_path: (last_timestamp, last_grade)}."""
    latest: dict[str, tuple[datetime, str]] = {}
    if not history_path.is_file():
        return latest
    for line in history_path.read_text().splitlines():
        m = HEADER_RE.match(line)
        if not m:
            continue
        try:
            ts = datetime.fromisoformat(m["ts"])
        except ValueError:
            continue
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        path = m["path"]
        grade = m["grade"]
        prev = latest.get(path)
        if prev is None or ts > prev[0]:
            latest[path] = (ts, grade)
    return latest


def score(now: datetime, last: tuple[datetime, str] | None) -> float:
    if last is None:
        return math.inf
    ts, grade = last
    days = (now - ts).total_seconds() / 86400.0
    return days / GRADE_MULTIPLIER[grade]


def deck_matches(deck: Path, filter_str: str, root: Path) -> bool:
    rel = deck.relative_to(root).as_posix()
    norm = filter_str.strip("/")
    return rel == norm or deck.name == norm


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("deck", nargs="?", default=None,
                        help="Deck name or relative path filter (e.g. 'algos' or 'code/algos').")
    parser.add_argument("--count", type=int, default=1,
                        help="Number of cards to print (top-N by staleness). Default 1.")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    history = parse_history(root / "history.md")
    now = datetime.now(timezone.utc)

    decks = find_decks(root)
    if args.deck:
        decks = [d for d in decks if deck_matches(d, args.deck, root)]
        if not decks:
            print(f"No deck matching {args.deck!r}.", file=sys.stderr)
            return 1

    candidates: list[tuple[float, str]] = []
    for deck in decks:
        for card in find_cards(deck):
            rel = card.relative_to(root).as_posix()
            candidates.append((score(now, history.get(rel)), rel))

    if not candidates:
        print("No cards found.", file=sys.stderr)
        return 1

    # Shuffle first so ties break randomly, then stable-sort by score desc.
    random.shuffle(candidates)
    candidates.sort(key=lambda x: x[0], reverse=True)
    for _, path in candidates[: max(1, args.count)]:
        print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
