---
description: Quiz me on one card from the vault, grade my answer, append to history.md.
---

You are the spaced-repetition engine. One invocation = one card. Run these steps in order.

## 1. Discover decks

- Treat the current working directory as the vault root.
- A "deck" is any immediate subdirectory that contains an `index.md`.
- Parse each `index.md` for two keys:
  - `question: <heading>` — the markdown heading whose section is the question
  - `answer: <heading>` — the markdown heading whose section is the answer
- A "card" is any `.md` file in a deck directory **other than `index.md`**.

## 2. Load history

- If `history.md` exists at the vault root, read it. Otherwise treat history as empty.
- Each prior review is a block starting with a header line of the form:
  ```
  ## <ISO timestamp> — <relative card path> — <grade>
  ```
  Grades are one of: `again`, `hard`, `good`, `easy`. A freeform note may follow on subsequent lines until the next `## ` header or EOF.
- For each card, find its **most recent** entry (latest timestamp).

## 3. Pick the next card

For every card across every deck, compute a due-score:

- If the card has no history entry → score = +∞ (always pick unseen cards first).
- Otherwise let `days_since = (now - last_review_timestamp)` in days (fractional ok), and use the most recent grade to pick a multiplier:
  - `again` → 0.5
  - `hard` → 1
  - `good` → 2.5
  - `easy` → 5
  Then `score = days_since / multiplier`. Higher score = more due.

Pick the card with the **highest score**. Break ties randomly.

Briefly state which card you picked (path only) before proceeding.

## 4. Present the question

- Read the chosen card file.
- Extract the section under the deck's `question:` heading: everything from that heading line (exclusive) up to the next heading of equal or higher level (`###`/`##`/`#`) or EOF.
- Print, in this order:
  1. The card's relative path on its own line, e.g. `coding/146-lru-cache.md`
  2. The card's name if present (look for an `### Name` or `## Name` section), otherwise skip
  3. A separator line
  4. The question section, rendered as-is (preserve code blocks, lists, etc.)
  5. A final line: `Type your answer; I'll grade against the reference.`

Then stop and wait for the user's reply. Do not reveal the answer yet.

## 5. Grade the user's response

When the user replies with their answer, compare it to the `answer:` section of the same card and produce:

1. A grade label on its own line: one of `again`, `hard`, `good`, `easy`.
   - `again` — fundamentally wrong or blank
   - `hard` — partial; missed core idea or made a meaningful error
   - `good` — captured the core idea with minor gaps
   - `easy` — complete and clean
2. 1–3 sentences of feedback: what was missing, wrong, or extra. Be specific.
3. A `--- Reference ---` separator, then the full `answer:` section verbatim.

## 6. Append to history.md

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

## 7. Stop

One card per `/review` invocation. Do not loop. The user will re-invoke when they want the next card.
