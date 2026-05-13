#!/usr/bin/env python3
"""FSRS-backed study session picker.

Subcommands:
  next [--deck DECK] [--size N]
      Print current session as JSON. Refills (top-N most-due cards by FSRS) if
      no session exists, the current one is exhausted, or --deck differs from
      the stored deck. Output: deck, cards, index, current, total, remaining,
      refilled.

  grade --card PATH --grade {again,hard,good,easy}
      Apply the FSRS transition for the card at PATH using the canonical 1..4
      grade encoding. Inserts a new studylog row (post-review state) and
      advances the session pointer. Prints updated session JSON.

  debug --card PATH
      Read-only: print current state, predicted due date, and the last 10
      studylog rows for the card. Useful for verifying behavior.

Picker: walks decks (same as session.py), hashes each card's question+answer
to a stable card_id, looks up the latest state in vw_cards, ranks by due date
(unseen = epoch-min). Ties shuffled before stable sort.

State: state.db at the repo root (the FSRS authoritative store).
       .claude/fsrs_session.json (gitignored) holds the current 10-card batch.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

_DIR = Path(__file__).resolve().parent
if str(_DIR) not in sys.path:
    sys.path.insert(0, str(_DIR))

from _srs import cards as cards_mod  # noqa: E402
from _srs import db as db_mod  # noqa: E402
from _srs import scheduler as sched  # noqa: E402

ROOT = _DIR.parent
DB_PATH = ROOT / "state.db"
SESSION_PATH = _DIR / "fsrs_session.json"
DEFAULT_SIZE = 10


def pick_batch(deck_filter: str | None, size: int) -> list[str]:
    pairs = cards_mod.discover(deck_filter)  # [(card_id, rel_path), ...]
    if not pairs:
        sys.exit("No cards found.")
    conn = db_mod.connect(DB_PATH)
    try:
        states = db_mod.list_latest_states(conn)
    finally:
        conn.close()

    epoch_min = datetime.fromtimestamp(0, tz=timezone.utc)
    scored: list[tuple[datetime, str]] = []
    for cid, rel in pairs:
        state = states.get(cid)
        if state is None:
            due = epoch_min
        else:
            sv_json, _state_type, _last = state
            due = sched.predict_due(sv_json)
        scored.append((due, rel))

    random.shuffle(scored)
    scored.sort(key=lambda x: x[0])
    return [rel for _, rel in scored[: max(1, size)]]


def load_session() -> dict | None:
    try:
        return json.loads(SESSION_PATH.read_text())
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def save_session(state: dict) -> None:
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
    state = load_session()
    deck = args.deck.strip("/").lstrip("@") if args.deck else None
    refilled = needs_refill(state, deck)
    if refilled:
        state = {
            "deck": deck,
            "cards": pick_batch(deck, args.size),
            "index": 0,
            "started_at": datetime.now(timezone.utc).isoformat(timespec="minutes"),
        }
        save_session(state)
    print(json.dumps(project(state, refilled=refilled), indent=2))
    return 0


def cmd_grade(args: argparse.Namespace) -> int:
    grade_int = sched.GRADE_NAME_TO_INT.get(args.grade.lower())
    if grade_int is None:
        sys.exit(f"Bad grade {args.grade!r}; expected one of {list(sched.GRADE_NAME_TO_INT)}.")

    card_rel = args.card.strip()
    card_path = ROOT / card_rel
    if not card_path.is_file():
        sys.exit(f"Card not found: {card_rel}")
    deck_dir = card_path.parent
    card_id = cards_mod.card_id_for(card_path, deck_dir)

    now = datetime.now(timezone.utc)
    conn = db_mod.connect(DB_PATH)
    try:
        prev = db_mod.latest_state(conn, card_id)
        prev_sv = prev[0] if prev else None
        new_sv = sched.transition(prev_sv, grade_int, now)
        db_mod.insert_review(
            conn,
            card_id=card_id,
            timestamp=now,
            state_vector_json=new_sv,
            state_type=sched.STATE_TYPE,
            grade=grade_int,
        )
    finally:
        conn.close()

    state = load_session()
    if state is not None:
        state["index"] = min(state["index"] + 1, len(state["cards"]))
        save_session(state)
        print(json.dumps(project(state), indent=2))
    else:
        print(json.dumps({"graded": card_rel, "grade": args.grade, "note": "no active session"}, indent=2))
    return 0


def cmd_debug(args: argparse.Namespace) -> int:
    card_rel = args.card.strip()
    card_path = ROOT / card_rel
    if not card_path.is_file():
        sys.exit(f"Card not found: {card_rel}")
    deck_dir = card_path.parent
    card_id = cards_mod.card_id_for(card_path, deck_dir)

    conn = db_mod.connect(DB_PATH)
    try:
        state = db_mod.latest_state(conn, card_id)
        log_rows = conn.execute(
            "SELECT study_id, timestamp, state_type, grade FROM studylog "
            "WHERE card_id = ? ORDER BY study_id DESC LIMIT 10",
            (card_id,),
        ).fetchall()
    finally:
        conn.close()

    if state is None:
        info = {"card_id": card_id, "card_path": card_rel, "state": None, "due_date": None}
    else:
        sv, st, ts = state
        due = sched.predict_due(sv)
        info = {
            "card_id": card_id,
            "card_path": card_rel,
            "state_type": st,
            "state_vector": json.loads(sv),
            "last_updated": ts.isoformat(timespec="minutes"),
            "due_date": due.isoformat(timespec="minutes"),
        }
    info["studylog"] = [
        {"study_id": sid, "timestamp": ts, "state_type": st, "grade": g}
        for (sid, ts, st, g) in log_rows
    ]
    print(json.dumps(info, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("next", help="Get current session (refills if needed).")
    p.add_argument("--deck", default=None, help="Deck filter for refills.")
    p.add_argument("--size", type=int, default=DEFAULT_SIZE, help="Batch size on refill.")
    p.set_defaults(func=cmd_next)

    p = sub.add_parser("grade", help="Apply FSRS transition + advance session.")
    p.add_argument("--card", required=True, help="Relative card path.")
    p.add_argument("--grade", required=True, help="again|hard|good|easy")
    p.set_defaults(func=cmd_grade)

    p = sub.add_parser("debug", help="Print current state + due date for a card.")
    p.add_argument("--card", required=True, help="Relative card path.")
    p.set_defaults(func=cmd_debug)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
