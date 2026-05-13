#!/usr/bin/env python3
"""Manage a batched study session of stale cards.

Subcommands:
  next [--deck DECK] [--size N]
      Print current session as JSON. Refills (top-N stalest cards) if no
      session exists, the current one is exhausted, or --deck differs from
      the stored deck. Output: deck, cards, index, current, total, remaining,
      refilled.

  advance
      Move past the current card. Prints updated session JSON.

Scoring: days_since_last_review / grade_multiplier (again=0.5, hard=1.0,
good=2.5, easy=5.0). Unseen = +inf. Higher = staler = picked first. Ties
break randomly.

Decks: any dir containing index.md (under root, max depth 4). Cards: *.md
in the deck dir, excluding index.md and any name in the deck's `inactive:`
list. History headers: `## <iso-ts> — <path> — <grade>`.

State: .claude/session.json (gitignored). Root: parent of this script.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SESSION_PATH = Path(__file__).resolve().parent / "session.json"
DEFAULT_SIZE = 10
GRADE_MULTIPLIER = {"again": 0.5, "hard": 1.0, "good": 2.5, "easy": 5.0}
HEADER_RE = re.compile(
    r"^##\s+(?P<ts>\S+)\s+—\s+(?P<path>\S+)\s+—\s+(?P<grade>again|hard|good|easy)\s*$"
)
SKIP_DIRS = {"__pycache__", "node_modules", ".venv", ".git"}
MAX_DEPTH = 4


def find_decks(root: Path) -> list[Path]:
    """Dirs containing index.md, depth-limited; don't descend into a deck."""
    decks: list[Path] = []

    def walk(p: Path, depth: int) -> None:
        if depth > MAX_DEPTH:
            return
        if p != root and (p / "index.md").is_file():
            decks.append(p)
            return
        for c in sorted(p.iterdir()):
            if c.is_dir() and c.name not in SKIP_DIRS and not c.name.startswith("."):
                walk(c, depth + 1)

    walk(root, 0)
    return decks


def parse_inactive(index_path: Path) -> set[str]:
    """Parse `inactive:` (inline or YAML-style list) from a deck's index.md."""
    if not index_path.is_file():
        return set()
    inactive: set[str] = set()
    in_block = False
    for raw in index_path.read_text().splitlines():
        s = raw.strip()
        if not in_block:
            if s.startswith("inactive:"):
                in_block = True
                inactive.update(x.strip() for x in s[len("inactive:"):].split(",") if x.strip())
            continue
        if s.startswith("- "):
            inactive.add(s[2:].strip())
        elif s and not s.startswith("#"):
            in_block = False
    return inactive


def find_cards(deck: Path) -> list[Path]:
    inactive = parse_inactive(deck / "index.md")
    return sorted(
        p for p in deck.iterdir()
        if p.is_file() and p.suffix == ".md" and p.name != "index.md" and p.name not in inactive
    )


def parse_history(path: Path) -> dict[str, tuple[datetime, str]]:
    """{relative_card_path: (last_timestamp, last_grade)}."""
    latest: dict[str, tuple[datetime, str]] = {}
    if not path.is_file():
        return latest
    for line in path.read_text().splitlines():
        m = HEADER_RE.match(line)
        if not m:
            continue
        try:
            ts = datetime.fromisoformat(m["ts"])
        except ValueError:
            continue
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        prev = latest.get(m["path"])
        if prev is None or ts > prev[0]:
            latest[m["path"]] = (ts, m["grade"])
    return latest


def score(now: datetime, last: tuple[datetime, str] | None) -> float:
    if last is None:
        return math.inf
    ts, grade = last
    return (now - ts).total_seconds() / 86400.0 / GRADE_MULTIPLIER[grade]


def deck_matches(deck: Path, name: str) -> bool:
    norm = name.strip("/")
    return deck.relative_to(ROOT).as_posix() == norm or deck.name == norm


def pick_batch(deck_filter: str | None, size: int) -> list[str]:
    decks = find_decks(ROOT)
    if deck_filter:
        decks = [d for d in decks if deck_matches(d, deck_filter)]
        if not decks:
            sys.exit(f"No deck matching {deck_filter!r}.")
    history = parse_history(ROOT / "history.md")
    now = datetime.now(timezone.utc)
    scored: list[tuple[float, str]] = []
    for deck in decks:
        for card in find_cards(deck):
            rel = card.relative_to(ROOT).as_posix()
            scored.append((score(now, history.get(rel)), rel))
    if not scored:
        sys.exit("No cards found.")
    random.shuffle(scored)
    scored.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in scored[: max(1, size)]]


def load() -> dict | None:
    try:
        return json.loads(SESSION_PATH.read_text())
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def save(state: dict) -> None:
    SESSION_PATH.write_text(json.dumps(state, indent=2) + "\n")


def project(state: dict, refilled: bool | None = None) -> dict:
    total = len(state["cards"])
    idx = state["index"]
    out = {
        "deck": state.get("deck"),
        "cards": state["cards"],
        "index": idx,
        "current": state["cards"][idx] if idx < total else None,
        "total": total,
        "remaining": max(0, total - idx),
    }
    if refilled is not None:
        out["refilled"] = refilled
    return out


def needs_refill(state: dict | None, deck: str | None) -> bool:
    return (
        state is None
        or state.get("index", 0) >= len(state.get("cards", []))
        or (deck is not None and state.get("deck") != deck)
    )


def cmd_next(args: argparse.Namespace) -> int:
    state = load()
    deck = args.deck.strip("/") if args.deck else None
    refilled = needs_refill(state, deck)
    if refilled:
        state = {
            "deck": deck,
            "cards": pick_batch(deck, args.size),
            "index": 0,
            "started_at": datetime.now(timezone.utc).isoformat(timespec="minutes"),
        }
        save(state)
    print(json.dumps(project(state, refilled=refilled), indent=2))
    return 0


def cmd_advance(_args: argparse.Namespace) -> int:
    state = load()
    if state is None:
        print("No active session.", file=sys.stderr)
        return 1
    state["index"] = min(state["index"] + 1, len(state["cards"]))
    save(state)
    print(json.dumps(project(state), indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("next", help="Get current session state (refills if needed).")
    p.add_argument("--deck", default=None, help="Deck filter for refills.")
    p.add_argument("--size", type=int, default=DEFAULT_SIZE, help="Batch size on refill.")
    p.set_defaults(func=cmd_next)
    sub.add_parser("advance", help="Advance past the current card.").set_defaults(func=cmd_advance)
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
