---
description: Create a new study card in one of this vault's decks, written from the current conversation in the deck's existing style.
---

You are turning the current conversation into a single new study card in this vault. One invocation = one card. Run these steps in order.

## 1. Pick the deck

A deck is any directory under the repo root that contains an `index.md` (find them with `find . -name index.md -not -path './.*'`). Read each deck's `index.md` for its `question:` / `answer:` heading names, and skim a card or two to learn what the deck is about.

Pick the deck whose subject best matches the recent discussion. If the conversation could plausibly fit two decks, announce your pick in one short line ("Filing under `notes/math/` — a derivation, not a coding problem.") and proceed. Don't ask. If no deck fits at all, say so and stop.

## 2. Pick a slug

Choose a short kebab-case filename, no extension, matching the deck's naming convention (e.g. LeetCode decks prefix the problem number: `146-lru-cache.md`; others use descriptive slugs: `lagrange-multipliers.md`).

Before writing, check the deck dir to make sure the slug doesn't collide. If it does, append a short qualifier (e.g. `kmeans-step-cosine.md`) — don't overwrite an existing card.

## 3. Match the deck's exact structure

Open 1–2 existing cards in the chosen deck and mirror their structure exactly — heading levels, field order (`## Tags`, `### Name`, `### Source`, …), prose tone, and code-block conventions. Do not invent new top-level fields.

The `question:` / `answer:` headings (per the deck's `index.md`) are mandatory — the picker relies on them. Other fields can be omitted if the neighboring cards omit them.

## 4. Write the content

Synthesize from the current conversation. Keep the same voice the existing cards use: terse, opinionated, mentions gotchas explicitly. Specifically:

- **Problem / Question**: state the task tightly. Include input/output shapes or constraints if relevant. No "we will explore…" filler.
- **Solution / Answer**: lead with the key idea in one or two sentences, then a single fenced code block (if applicable), then a short list of gotchas / tradeoffs / alternatives. Match the prose density of neighboring cards.
- **Source**: cite where this came from — "Interview practice (Problem 3 in `python/interview_practice.ipynb`)", "LeetCode 146", "cuPyNumeric k-means example", etc. Use `N/A` only if nothing fits.

Do not include conversation artifacts: no "as we discussed", no "the user asked", no test output dumps. The card should read standalone weeks later.

## 5. Write the file

Use the Write tool to create `<deck>/<slug>.md`. Do not modify the deck's `index.md` — new cards are active by default; the `inactive:` list is for cards the user has retired manually.

## 6. Confirm

Print, on its own lines:

1. The relative path of the new card (e.g. `code/ml/kmeans-step.md`).
2. One short line on what's in it ("Mask-based group aggregation; covers `np.bincount` weight limits and the empty-cluster `np.clip` trick.").

Stop. Don't loop, don't offer follow-ups, don't summarize the conversation. The user re-invokes `/note` for the next card.
