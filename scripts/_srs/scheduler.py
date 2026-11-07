"""Thin wrapper around py-fsrs (`fsrs` PyPI package).

Encapsulates the library so future schedulers can slot in via STATE_TYPE.
Persists the full fsrs Card dict as the state_vector JSON. The fsrs Card has
its own integer `card_id` field — we set it to 0 on serialize since our DB
uses a separate content-hash card_id as the primary key.

`grade_int` is the canonical FSRS 1..4 (Again, Hard, Good, Easy).
"""
from __future__ import annotations

import json
from datetime import datetime, timezone

from fsrs import Card, Rating, Scheduler

STATE_TYPE = "fsrs-6.3.1"
GRADE_NAME_TO_INT = {"again": 1, "hard": 2, "good": 3, "easy": 4}
GRADE_INT_TO_NAME = {v: k for k, v in GRADE_NAME_TO_INT.items()}

_scheduler = Scheduler()


def _card_from_state(state_json: str | None) -> Card:
    if state_json is None:
        return Card()
    d = json.loads(state_json)
    d.setdefault("card_id", 0)
    return Card.from_dict(d)


def _card_to_state(card: Card) -> str:
    d = card.to_dict()
    d["card_id"] = 0  # ours is a content hash; theirs is noise
    return json.dumps(d, separators=(",", ":"))


def transition(prev_state_json: str | None, grade_int: int, now: datetime) -> str:
    """Apply a review and return the new state_vector JSON."""
    card = _card_from_state(prev_state_json)
    new_card, _log = _scheduler.review_card(card, Rating(grade_int), review_datetime=now)
    return _card_to_state(new_card)


def predict_due(state_json: str | None) -> datetime:
    """Return when this card is next due (UTC)."""
    if state_json is None:
        return datetime.fromtimestamp(0, tz=timezone.utc)
    card = _card_from_state(state_json)
    return card.due if card.due else datetime.fromtimestamp(0, tz=timezone.utc)
