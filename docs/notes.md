# Notes layout

```
notes/
├── code/
│   ├── algos/      deck — LeetCode / coding problems
│   │   ├── index.md            ← declares heading names + inactive list
│   │   ├── 146-lru-cache.md    ← one card
│   │   ├── 211-add-search-words.md
│   │   └── …
│   ├── ml/         deck — ML / NumPy patterns
│   └── basics/     deck — Python fundamentals
├── math/           deck — optimization / analysis
├── history.md      append-only review log (used by /study + /study-asrs)
├── state.db        SQLite — FSRS scheduler state (used by /study only)
├── .claude/
│   ├── commands/   skill definitions: note.md, study.md, study-asrs.md
│   ├── session.py        /study-asrs picker (multiplier-based)
│   ├── fsrs_session.py   /study picker (FSRS-backed)
│   ├── _srs/             FSRS scheduler modules (cards/db/scheduler)
│   ├── session.json       /study-asrs session state (gitignored)
│   └── fsrs_session.json  /study session state (gitignored)
└── pyproject.toml
```

## Decks

A **deck** is any directory containing an `index.md`. The index declares the per-note heading names used by the picker and skill:

```
question: ### Problem
answer: ### Solution
inactive:
  - 3-longest-substring-no-repeat.md   ← note excluded from scheduling
```

## Notes

A **note** is any `.md` file in a deck directory (except `index.md` and anything in the deck's `inactive:` list). Card structure is per-deck — `code/algos/*.md` use `### Problem` / `### Solution`, `math/*.md` use `### Question` / `### Answer`.
