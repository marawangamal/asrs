#!/usr/bin/env python3
"""Manage a batched study session: a queue of 10 cards picked by pick.py.

Subcommands:
  next [--deck DECK] [--size N]
      Print the current session state as JSON. Refills (picks a fresh batch
      via pick.py) if no session exists, the session is exhausted, or the
      deck filter changed. Output fields:
        deck      — deck filter used to pick this batch (or null)
        cards     — list of relative card paths in the batch
        index     — 0-based index of the current card
        current   — relative path of the current card (== cards[index])
        total     — len(cards)
        remaining — total - index
        refilled  — true iff this call created a new batch

  advance
      Move past the current card. Prints updated JSON (same shape as `next`
      minus `refilled`). Once index == total, the next `next` call refills.

Session state lives at .claude/session.json (gitignored). Vault root is the
parent of this script.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pick

ROOT = Path(__file__).resolve().parent.parent
SESSION_PATH = Path(__file__).resolve().parent / "session.json"
DEFAULT_SIZE = 10


def load() -> dict | None:
    if not SESSION_PATH.is_file():
        return None
    try:
        return json.loads(SESSION_PATH.read_text())
    except (json.JSONDecodeError, OSError):
        return None


def save(state: dict) -> None:
    SESSION_PATH.write_text(json.dumps(state, indent=2) + "\n")


def pick_batch(deck_filter: str | None, size: int) -> list[str]:
    """Pick top-N stalest cards using pick.py's scoring."""
    history = pick.parse_history(ROOT / "history.md")
    now = datetime.now(timezone.utc)

    decks = pick.find_decks(ROOT)
    if deck_filter:
        decks = [d for d in decks if pick.deck_matches(d, deck_filter, ROOT)]
        if not decks:
            print(f"No deck matching {deck_filter!r}.", file=sys.stderr)
            sys.exit(1)

    import random as _random
    candidates: list[tuple[float, str]] = []
    for deck in decks:
        for card in pick.find_cards(deck):
            rel = card.relative_to(ROOT).as_posix()
            candidates.append((pick.score(now, history.get(rel)), rel))
    if not candidates:
        print("No cards found.", file=sys.stderr)
        sys.exit(1)

    _random.shuffle(candidates)
    candidates.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in candidates[: max(1, size)]]


def project(state: dict, include_refilled: bool = False) -> dict:
    total = len(state["cards"])
    idx = state["index"]
    current = state["cards"][idx] if idx < total else None
    out = {
        "deck": state.get("deck"),
        "cards": state["cards"],
        "index": idx,
        "current": current,
        "total": total,
        "remaining": max(0, total - idx),
    }
    if include_refilled:
        out["refilled"] = state.get("_refilled", False)
    return out


def needs_refill(state: dict | None, requested_deck: str | None) -> bool:
    if state is None:
        return True
    if state.get("index", 0) >= len(state.get("cards", [])):
        return True
    if requested_deck is not None and state.get("deck") != requested_deck:
        return True
    return False


def cmd_next(args: argparse.Namespace) -> int:
    state = load()
    requested_deck = args.deck.strip("/") if args.deck else None
    if needs_refill(state, requested_deck):
        batch = pick_batch(requested_deck, args.size)
        state = {
            "deck": requested_deck,
            "cards": batch,
            "index": 0,
            "started_at": datetime.now(timezone.utc).isoformat(timespec="minutes"),
            "_refilled": True,
        }
        save(state)
    else:
        state["_refilled"] = False
    print(json.dumps(project(state, include_refilled=True), indent=2))
    return 0


def cmd_advance(_args: argparse.Namespace) -> int:
    state = load()
    if state is None:
        print("No active session.", file=sys.stderr)
        return 1
    state["index"] = min(state["index"] + 1, len(state["cards"]))
    state.pop("_refilled", None)
    save(state)
    print(json.dumps(project(state), indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_next = sub.add_parser("next", help="Get current session state (refills if needed).")
    p_next.add_argument("--deck", default=None, help="Deck filter for refills.")
    p_next.add_argument("--size", type=int, default=DEFAULT_SIZE, help="Batch size on refill.")
    p_next.set_defaults(func=cmd_next)

    p_adv = sub.add_parser("advance", help="Advance past the current card.")
    p_adv.set_defaults(func=cmd_advance)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
