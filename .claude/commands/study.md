---
description: Quiz me on one card from the vault, grade my answer, append to history.md.
---

You are the spaced-repetition engine. One invocation = one card. Run these steps in order.

## 1. Pick the next card

Run `python3 pick.py` from the vault root. It prints one relative card path (e.g. `coding/146-lru-cache.md`) on stdout. That is your card.

The picker handles deck discovery, history parsing, and due-score computation. It walks immediate subdirs containing `index.md`, treats every other `.md` file in those dirs as a card, parses `history.md` for the most recent `## <ts> — <path> — <grade>` line per card, and picks the card with the highest `days_since / multiplier` (unseen → +∞). Multipliers: `again` 0.5, `hard` 1, `good` 2.5, `easy` 5.

If you ever need to debug or tweak selection, edit `pick.py` rather than recomputing inline.

## 2. Present the question

- Read the chosen card's deck `index.md` to find the `question:` and `answer:` heading names.
- Read the card file.
- Extract the section under the deck's `question:` heading: everything from that heading line (exclusive) up to the next heading of equal or higher level (`###`/`##`/`#`) or EOF.
- Print, in this order:
  1. The card's relative path on its own line, e.g. `coding/146-lru-cache.md`
  2. The card's name if present (look for an `### Name` or `## Name` section), otherwise skip
  3. A separator line
  4. The question section, rendered as-is (preserve code blocks, lists, etc.)
  5. A final line: `Type your answer; I'll grade against the reference.`

Then stop and wait for the user's reply. Do not reveal the answer yet.

## 3. Grade the user's response

When the user replies with their answer, compare it to the `answer:` section of the same card and produce:

1. A grade label on its own line: one of `again`, `hard`, `good`, `easy`.
   - `again` — fundamentally wrong or blank
   - `hard` — partial; missed core idea or made a meaningful error
   - `good` — captured the core idea with minor gaps
   - `easy` — complete and clean
2. 1–3 sentences of feedback: what was missing, wrong, or extra. Be specific.
3. A `--- Reference ---` separator, then the full `answer:` section verbatim.

## 4. Append to history.md

Append a new block to `history.md` at the vault root. If the file doesn't exist, create it with a single header line first:

```
# Review history
```

Then append:

```
## <ISO timestamp> — <relative card path> — <grade>
<one-to-three-sentence note summarizing what the user got right and wrong>
```

Use a real ISO-8601 timestamp with minute precision (e.g. `2026-05-11T18:40`). The note should be terse and useful to your future self when picking and grading this card again — call out specific gotchas the user missed or solid points they nailed.

## 5. Stop

One card per `/study` invocation. Do not loop. The user will re-invoke when they want the next card.
