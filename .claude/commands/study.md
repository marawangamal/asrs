---
description: Quiz me on one card from the current 10-card study session, grade my answer, append to history.md.
---

You are the spaced-repetition engine. One `/study` invocation = one card from a
batched session of 10. The session is persisted at `.claude/session.json` so it
survives across invocations until exhausted, at which point the next call
refills with a fresh batch.

Run these steps in order.

## 1. Load (or refill) the session

Determine the deck filter from the user's `$ARGUMENTS`:

- If `$ARGUMENTS` contains a path-like token (e.g. `@code/algos/`, `code/algos`,
  `algos`), strip leading `@` and trailing `/` and use it as the deck filter.
- Otherwise: no deck filter.

Then run:

```
python3 .claude/session.py next [--deck <DECK>]
```

(omit `--deck` if no filter was given). This prints a JSON object. Parse it.
Fields you care about:

- `current` — the relative path of the card to quiz
- `index`, `total`, `remaining` — progress within the batch
- `refilled` — `true` iff this call started a new batch
- `cards` — the full batch list

If `refilled` is `true`, **print a session summary first**, then a blank line,
then continue to step 2. The summary should look like:

```
📚 New session (N cards) — deck: <deck or "all">
  1. code/algos/146-lru-cache.md
  2. code/algos/239-sliding-window-maximum.md
  …
```

(List every card in `cards`, numbered, one per line.)

If `refilled` is `false`, skip the summary and go straight to step 2. Optionally
prepend a single short progress line like `Card <index+1>/<total> · <remaining-1> after this`.

The picker handles deck discovery, history parsing, and due-score computation.
It walks all dirs containing `index.md` (recursively, so `code/algos`, `code/ml`,
`math` are all valid decks), treats every other `.md` file in those dirs as a
card, parses `history.md` for the most recent `## <ts> — <path> — <grade>` line
per card, and picks the top-N cards by `days_since / multiplier` (unseen → +∞).
Multipliers: `again` 0.5, `hard` 1, `good` 2.5, `easy` 5. Ties are broken
randomly.

If you ever need to debug or tweak selection/session logic, edit
`.claude/pick.py` or `.claude/session.py` rather than recomputing inline.

## 2. Present the question

The card path is `current` from step 1.

- Read the chosen card's deck `index.md` (the directory containing the card) to
  find the `question:` and `answer:` heading names.
- Read the card file.
- Extract the section under the deck's `question:` heading: everything from
  that heading line (exclusive) up to the next heading of equal or higher
  level (`###`/`##`/`#`) or EOF.
- Print, in this order:
  1. The card's relative path on its own line, e.g. `code/algos/146-lru-cache.md`
  2. The card's name if present (look for an `### Name` or `## Name` section), otherwise skip
  3. A separator line
  4. The question section, rendered as-is (preserve code blocks, lists, etc.)
  5. A final line: `Type your answer; I'll grade against the reference.`

Then stop and wait for the user's reply. Do not reveal the answer yet. Do not
advance the session until after grading.

## 3. Grade the user's response

When the user replies with their answer, compare it to the `answer:` section
of the same card and produce:

1. A grade label on its own line: one of `again`, `hard`, `good`, `easy`.
   - `again` — fundamentally wrong or blank
   - `hard` — partial; missed core idea or made a meaningful error
   - `good` — captured the core idea with minor gaps
   - `easy` — complete and clean
2. 1–3 sentences of feedback: what was missing, wrong, or extra. Be specific.
3. A `--- Reference ---` separator, then the full `answer:` section verbatim.

## 4. Append to history.md

Append a new block to `history.md` at the vault root. If the file doesn't
exist, create it with a single header line first:

```
# Review history
```

Then append:

```
## <ISO timestamp> — <relative card path> — <grade>
<one-to-three-sentence note summarizing what the user got right and wrong>
```

Use a real ISO-8601 timestamp with minute precision (e.g. `2026-05-11T18:40`).
The note should be terse and useful to your future self when picking and
grading this card again — call out specific gotchas the user missed or solid
points they nailed.

## 5. Advance the session

After history is written, run:

```
python3 .claude/session.py advance
```

Parse the JSON output. If `remaining` is `0`, print a single closing line:

```
✅ Session complete (N/N). Next /study will start a fresh batch.
```

Otherwise print:

```
➡️  N left in this session. /study for the next card.
```

## 6. Stop

One card per `/study` invocation. Do not loop. The user will re-invoke when
they want the next card.

ARGUMENTS: $ARGUMENTS
