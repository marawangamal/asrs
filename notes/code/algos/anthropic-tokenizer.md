## Number
N/A
## Tags
interview,anthropic
### Name
Vocabulary Tokenizer (WordPiece-style)
### Problem
Given a `text` string and a `vocab` dict mapping words to token IDs (plus a special `"UNK"` entry with ID -1), tokenize the text using greedy longest-match. Unmatched characters become UNK.

Example: `vocab = {"app": 1, "apple": 2, "UNK": -1}`; `tokenize("apple", vocab) -> [2]`, `tokenize("bbb", vocab) -> [-1, -1, -1]`.

Follow-ups:
1. Make it efficient for long inputs full of matches.
2. Collapse consecutive UNKs into one UNK token.
### Solution
Walk the text left to right with a pointer `i`. At each position, try the longest substring first and shrink until a vocab entry matches. If nothing matches, emit UNK and advance by one.

The `for/else` Python idiom replaces the explicit `matched` flag — the `else` clause runs only if the inner loop completes without `break`. The walrus operator `:=` lets us assign and test in one line.

Concise version with **both follow-ups** built in (max-length pruning + UNK collapsing):

```python
def tokenize(text, vocab):
    unk_id = vocab["UNK"]
    max_len = max((len(w) for w in vocab if w != "UNK"), default=0)
    tokens, i, n = [], 0, len(text)
    while i < n:
        for j in range(min(i + max_len, n), i, -1):
            if (s := text[i:j]) in vocab and s != "UNK":
                tokens.append(vocab[s])
                i = j
                break
        else:
            if not (tokens and tokens[-1] == unk_id):
                tokens.append(unk_id)
            i += 1
    return tokens
```

**Optimization 1** (max-length pruning): precompute `max_len = max(len(w) for w in vocab)` and cap the inner loop at `min(i + max_len, n)`. Drops complexity from O(n²·L) to roughly O(n · max_len).

**Optimization 2** (UNK collapsing): on a no-match, only append UNK if the previous emitted token wasn't already UNK.

Key insight: greedy longest-match commits to the longest match at the *current position* and jumps past it. It does not search across all positions for the globally longest match — so a shorter vocab entry like `"ple"` might never get used if a longer entry like `"pple"` consumes it.

Strong follow-up to volunteer in an interview: "If the vocab were huge, I'd build a trie over the vocab strings and walk it character by character, recording the deepest accepting node hit. That's O(n · max_len) without the substring-slicing overhead, and it generalizes to streaming input." That mention signals you've thought beyond the toy version.

Tests:
- Knowledge of greedy with backtracking awareness (recognize that scan-and-match alone fails — need longest-match to disambiguate `app` vs `apple`).
- Spotting the O(n²) trap when input gets long.
- Adapting to changing requirements smoothly.
### Source
Anthropic Phone Screen (ModernLoop Phone Coding Q6)
