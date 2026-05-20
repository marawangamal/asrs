"""Card discovery, section extraction, and content-based card_id hashing.

Reuses deck/card discovery helpers from ../session.py (find_decks, find_cards,
parse_inactive, deck_matches). Adds the question/answer section parser used by
both the picker (for hashing) and the skill (for prompting), plus the stable
content-hash card_id.
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

# Reuse the existing helpers; do not duplicate.
_CLAUDE_DIR = Path(__file__).resolve().parent.parent
if str(_CLAUDE_DIR) not in sys.path:
    sys.path.insert(0, str(_CLAUDE_DIR))
from session import find_decks, find_cards, deck_matches  # noqa: E402

ROOT = _CLAUDE_DIR.parent

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")


def parse_index_headings(index_path: Path) -> tuple[str, str] | None:
    """Return (question_heading, answer_heading) from a deck's index.md, or None."""
    if not index_path.is_file():
        return None
    q = a = None
    for raw in index_path.read_text().splitlines():
        s = raw.strip()
        if s.startswith("question:"):
            q = s[len("question:"):].strip()
        elif s.startswith("answer:"):
            a = s[len("answer:"):].strip()
    if q and a:
        return q, a
    return None


def extract_section(card_text: str, heading: str) -> str | None:
    """Return the section body under `heading`.

    Heading is the exact line minus the trailing newline (e.g. '### Problem').
    Body runs from the line after the heading to the next heading of equal-or-
    higher level (smaller-or-equal hash count), or EOF. Returns None if the
    heading is not found.
    """
    target_level = len(heading) - len(heading.lstrip("#"))
    lines = card_text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == heading:
            start = i + 1
            break
    if start is None:
        return None
    body: list[str] = []
    for line in lines[start:]:
        m = _HEADING_RE.match(line)
        if m and len(m.group(1)) <= target_level:
            break
        body.append(line)
    return "\n".join(body).strip()


def card_id_for(card_path: Path, deck_dir: Path) -> str:
    """sha256[:16] of the card's question + answer sections.

    Falls back to hashing the full file bytes if the deck's question/answer
    headings can't be located in the card (malformed card or missing index).
    """
    headings = parse_index_headings(deck_dir / "index.md")
    text = card_path.read_text()
    if headings is not None:
        q_head, a_head = headings
        q = extract_section(text, q_head)
        a = extract_section(text, a_head)
        if q is not None and a is not None:
            payload = (q + "\n---\n" + a).encode()
            return hashlib.sha256(payload).hexdigest()[:16]
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def discover(deck_filter: str | None = None) -> list[tuple[str, str]]:
    """Walk decks under ROOT and return [(card_id, relative_card_path), ...].

    `deck_filter` accepts the same forms /study does (e.g. 'code/algos',
    'algos', '@code/algos/').
    """
    decks = find_decks(ROOT)
    if deck_filter:
        norm = deck_filter.strip("/").lstrip("@")
        decks = [d for d in decks if deck_matches(d, norm)]
        if not decks:
            raise SystemExit(f"No deck matching {deck_filter!r}.")
    out: list[tuple[str, str]] = []
    for deck in decks:
        for card in find_cards(deck):
            cid = card_id_for(card, deck)
            out.append((cid, card.relative_to(ROOT).as_posix()))
    return out


def deck_of(card_rel: str) -> Path:
    """Return the deck directory for a card path relative to ROOT."""
    p = (ROOT / card_rel).resolve()
    return p.parent
