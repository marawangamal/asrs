---
description: Create a new study card under code/algos, code/ml, or math, written from the current conversation in the deck's existing style.
---

You are turning the current conversation into a single new study card in this vault. One invocation = one card. Run these steps in order.

## 1. Pick the deck

Infer the deck from the conversation. The vault has these decks at the repo root:

- `code/algos/` — LeetCode / coding-interview problems. Heading style uses `## Number`, `### Problem`, `### Solution`, `### Source`.
- `code/ml/` — ML / NumPy / modelling patterns. Heading style uses `## Tags`, `### Problem`, `### Solution`, `### Source` (no `## Number`).
- `code/basics/` — Basic python, recursion. Heading style uses `## Tags`, `### Problem`, `### Solution`, `### Source` (no `## Number`).
- `math/` — math / optimization / analysis. Heading style uses `## Topic`, `### Question`, `### Answer`.

Use the recent discussion to choose:
- Talking about a LeetCode problem, data structure design, concurrency primitive → `code/algos/`.
- Talking about NumPy, ML algorithms, training tricks, broadcasting patterns → `code/ml/`.
- Talking about proofs, derivatives, optimization theory, linear algebra identities → `math/`.

Read `<deck>/index.md` to confirm the `question:` and `answer:` heading names — never guess them.

If the conversation could plausibly fit two decks, announce your pick in one short line ("Filing under `code/ml/` — broadcasting pattern, not a LeetCode-style problem.") and proceed. Don't ask.

## 2. Pick a slug

Choose a short kebab-case filename, no extension. Match the deck's naming convention:
- `code/algos/` cards from LeetCode start with the problem number: `146-lru-cache.md`. Cards without a number use a descriptive slug: `anthropic-tokenizer.md`.
- `code/ml/` and `math/` use descriptive slugs: `kmeans-step.md`, `lagrange-multipliers.md`.

Before writing, check the deck dir to make sure the slug doesn't collide. If it does, append a short qualifier (e.g. `kmeans-step-cosine.md`) — don't overwrite an existing card.

## 3. Match the deck's exact structure

Open 1–2 existing cards in the chosen deck and mirror their structure exactly — heading levels, field order, prose tone, and code-block conventions. Do not invent new top-level fields. Concretely:

- `code/algos/`: `## Number` (LeetCode # or `N/A`), `## Tags` (comma-separated, lowercase), `### Name`, `### Problem`, `### Solution`, `### Source`.
- `code/ml/`: `## Tags`, `### Name`, `### Problem`, `### Solution`, `### Source`.
- `math/`: `## Topic`, `## Tags`, `### Name`, `### Question`, `### Answer`.

The `question:` / `answer:` headings (per the deck's `index.md`) are mandatory — the picker relies on them. Other fields above can be omitted if the source card omits them.

## 4. Write the content

Synthesize from the current conversation. Keep the same voice the existing cards use: terse, opinionated, mentions gotchas explicitly. Specifically:

- **Problem / Question**: state the task tightly. Include input/output shapes or constraints if relevant. No "we will explore…" filler.
- **Solution / Answer**: lead with the key idea in one or two sentences, then a single fenced code block (if applicable), then a short list of gotchas / tradeoffs / alternatives. Match the prose density of neighboring cards — look at `code/algos/146-lru-cache.md` or `math/lagrange-multipliers.md` for calibration.
- **Source**: cite where this came from — "Interview practice (Problem 3 in `python/interview_practice.ipynb`)", "LeetCode 146", "cuPyNumeric k-means example", etc. Use `N/A` only if nothing fits.

Do not include conversation artifacts: no "as we discussed", no "the user asked", no test output dumps. The card should read standalone weeks later.

## 5. Write the file

Use the Write tool to create `<deck>/<slug>.md`. Do not modify the deck's `index.md` — new cards are active by default; the `inactive:` list is for cards the user has retired manually.

## 6. Confirm

Print, on its own lines:

1. The relative path of the new card (e.g. `code/ml/kmeans-step.md`).
2. One short line on what's in it ("Mask-based group aggregation; covers `np.bincount` weight limits and the empty-cluster `np.clip` trick.").

Stop. Don't loop, don't offer follow-ups, don't summarize the conversation. The user re-invokes `/note` for the next card.
