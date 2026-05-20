# `/study` in detail

## Data flow

```
       ┌────────────────────┐
user → │  /study            │ ← skill in .claude/commands/study.md
       └─────────┬──────────┘
                 │ 1. python3 .claude/fsrs_session.py next [--deck D]
                 ▼
       ┌────────────────────────────────────────────────┐
       │  fsrs_session.py                               │
       │   • walks decks → (card_id, card_path) pairs   │
       │   • reads vw_cards → latest state per card_id  │
       │   • ranks by FSRS-predicted due date           │
       │   • writes batch of 10 to fsrs_session.json    │
       └─────────┬──────────────────────────────────────┘
                 │ JSON
                 ▼
       skill reads `current`, presents the question, waits for answer,
       grades it, appends to history.md
                 │
                 │ 2. python3 .claude/fsrs_session.py grade --card P --grade G
                 ▼
       fsrs_session.py:
         • computes card_id from card content
         • looks up prior state from vw_cards
         • new_state = fsrs.review_card(prev_state, grade, now)
         • INSERTs a new studylog row (post-review snapshot)
         • advances fsrs_session.json index
```

## `state.db` schema

Single physical table — `studylog` (append-only, post-review snapshots) — plus a view that exposes the latest row per card.

```sql
CREATE TABLE studylog (
    study_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id       TEXT NOT NULL,        -- sha256[:16] of question+answer sections
    timestamp     TEXT NOT NULL,        -- ISO-8601 UTC
    state_vector  TEXT NOT NULL,        -- JSON: full fsrs.Card dict (D, S, due, …)
    state_type    TEXT NOT NULL,        -- e.g. 'fsrs-6.3.1'
    grade         INTEGER NOT NULL      -- 1=again, 2=hard, 3=good, 4=easy
);

CREATE VIEW vw_cards AS
SELECT s.card_id, s.state_vector, s.state_type, s.timestamp AS last_updated
FROM studylog s
JOIN (SELECT card_id, MAX(study_id) AS max_id FROM studylog GROUP BY card_id) latest
  ON latest.card_id = s.card_id AND latest.max_id = s.study_id;
```

There is intentionally **no `cards` table** and **no `card_path` column**:
- Current state per card = latest `studylog` row for that `card_id` (via `vw_cards`).
- `card_path` is derived from the filesystem walk at query time. Renames are free; content edits produce a new `card_id` and naturally orphan the old state for audit.

## `card_id`: content hash, not path

`card_id = sha256(question_section + "\n---\n" + answer_section)[:16]`

The hash covers only the question and answer sections — editing the `Source` line, fixing a typo in `Tags`, or renaming the file does **not** churn scheduler state. Editing the question or answer prose does (intentionally — that's a different card).

## Picker algorithm

```
inputs: deck_filter, size, now

1. walk decks → list of (card_id, card_path)
2. SELECT * FROM vw_cards → {card_id: (state, state_type, last_updated)}
3. for each card_id:
       due = scheduler.predict_due(state)  if state else epoch-min
4. shuffle, stable-sort by due ASC, take first `size`
```

New cards rank as overdue (epoch-min) and are picked first. Among new cards, ties are broken randomly.

## CLI surface (`.claude/fsrs_session.py`)

```
next [--deck DECK] [--size N]
    Print current session as JSON. Refills if no session, exhausted,
    or deck mismatch.

grade --card PATH --grade {again,hard,good,easy}
    Apply FSRS transition + advance session pointer. Inserts a
    studylog row with the post-review state.

regrade --card PATH --grade {again,hard,good,easy}
    Replace the latest studylog row for a card (use when a wrong
    grade slipped through). Deletes the most-recent row and
    re-applies the transition from the prior state, preserving the
    original timestamp. Leaves session.json alone.

debug --card PATH
    Print current state, predicted due date, and last 10 studylog
    rows for the card.
```

## Module layout under `.claude/_srs/`

| File                  | Purpose                                                       |
| --------------------- | ------------------------------------------------------------- |
| `_srs/cards.py`       | Deck/card discovery (reuses helpers from `session.py`), Q+A section extraction, content-hash `card_id`. |
| `_srs/scheduler.py`   | Thin wrapper over the `fsrs` PyPI package — `transition()`, `predict_due()`, grade-name ↔ int mapping. |
| `_srs/db.py`          | SQLite DAL — schema bootstrap, `latest_state()`, `list_latest_states()`, `insert_review()`. |
