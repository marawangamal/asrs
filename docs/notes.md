# Notes layout

Your notes repo (the "vault") — the plugin's skills run against the current directory:

```
my-notes/
├── notes/
│   ├── code/algos/     deck — any dir with an index.md is a deck
│   │   ├── index.md            ← declares heading names + inactive list
│   │   ├── 146-lru-cache.md    ← one card
│   │   └── …
│   └── math/           deck
├── history.md          append-only review log (used by /study + /study-asrs)
├── state.db            SQLite — FSRS scheduler state (gitignore it or commit it, your call)
└── .claude/
    ├── settings.json       enables the asrs plugin
    ├── session.json        /study-asrs session state (gitignore)
    └── fsrs_session.json   /study session state (gitignore)
```

The plugin itself (this repo):

```
asrs/
├── .claude-plugin/     plugin.json + marketplace.json
├── commands/           note.md, study.md, study-asrs.md
└── scripts/
    ├── session.py        /study-asrs picker (multiplier-based)
    ├── fsrs_session.py   /study picker (FSRS-backed)
    └── _srs/             FSRS scheduler modules (cards/db/scheduler)
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
