# `/study-asrs` (legacy multiplier picker)

Ranks cards by `(now - last_review) / grade_multiplier`. Multipliers: `again=0.5`, `hard=1.0`, `good=2.5`, `easy=5.0`. Unseen cards score `+∞` (picked first). Reads `history.md` directly — no database. Kept around for A/B comparison with `/study`.

## Why two pickers?

`/study-asrs` is dead-simple and depends only on `history.md` (a plain markdown file). It was the original scheduler. `/study` uses real FSRS — it gives each card a difficulty/stability state and a predicted due date — but requires `state.db` to be in sync. Both run side-by-side on the same vault while FSRS beds in. Eventually `/study-asrs` may be retired.
