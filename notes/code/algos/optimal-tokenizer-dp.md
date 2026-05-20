## Number
N/A
## Tags
interview,anthropic,dp
### Name
Optimal Tokenizer (DP / Viterbi)
### Problem
Given `text` and a `vocab` dict, segment `text` into the **fewest** pieces such that every piece is a vocab key. Return the list of pieces (or their ids).

Why this card exists: greedy longest-match (see `anthropic-tokenizer.md`) is **not optimal**. Committing to the longest match at the current position can consume characters that would have enabled a better split later.

Concrete counterexample:

```
vocab = {"a": 1, "ab": 2, "bcd": 3, "c": 4, "d": 5}
text  = "abcd"
greedy longest-match -> ["ab", "c", "d"]  (3 tokens)
optimal              -> ["a", "bcd"]      (2 tokens)
```

### Solution
Classic 1-D DP over prefix lengths. The whole algorithm is two lines:

```
# dp[i] is the min tokens needed to encode text[:i]
dp[i] = min(dp[j] + 1)  for all j < i where text[j:i] in vocab
```

with `dp[0] = 0`. For each `i`, scan back over every earlier cut point `j`; if `text[j:i]` is a vocab piece, relax `dp[i]`. Answer is `dp[n]`. To recover the pieces, store `parent[i] = argmin j` and walk back from `n`.

Naive scan is `O(n²)` candidate cuts. Prune with `max_len = max(len(w) for w in vocab)` — no piece can be longer than that, so only check `j in [max(0, i - max_len), i)`. That gives `O(n · max_len)`, same as greedy longest-match.

```python
def tokenize_optimal(text, vocab):
    n = len(text)
    max_len = max((len(w) for w in vocab if w != "UNK"), default=1)
    INF = float("inf")
    dp = [0] + [INF] * n
    parent = [-1] * (n + 1)
    for i in range(1, n + 1):
        # Always allow single-char UNK fallback so dp[i] is reachable.
        if dp[i - 1] + 1 < dp[i]:
            dp[i] = dp[i - 1] + 1
            parent[i] = i - 1
        for j in range(max(0, i - max_len), i):
            if text[j:i] in vocab and dp[j] + 1 < dp[i]:
                dp[i] = dp[j] + 1
                parent[i] = j
    pieces, i = [], n
    while i > 0:
        j = parent[i]
        pieces.append(text[j:i])
        i = j
    return pieces[::-1]
```

Why the DP works — **optimal substructure**: the best segmentation of `text[:i]` ends with *some* final piece `text[j:i]`, and the prefix `text[:j]` must itself be optimally segmented (otherwise swap it in for a strictly better answer).

Gotchas:

- **Unreachable positions**: without a UNK fallback, `dp[i] = ∞` is possible (no piece ends at `i`). The single-char fallback above makes every `i` reachable at cost 1.
- **"Optimal" depends on the objective**. For minimum tokens use `min` with `+1`. For **SentencePiece-unigram**, swap to `max` with `+ log p(piece)` — same recurrence, that's Viterbi over a unigram LM.
- **vs greedy**: same `O(n · max_len)` time, same trie applicability, but extra `O(n)` memory for `dp` and `parent`. The win is global optimality; the cost is one linear pass and a backtrack.
- **BPE is different**: BPE doesn't run this DP at inference. It deterministically replays the merge sequence learned at training, so it's neither greedy-longest nor DP-optimal — it's "replay merges in learned priority order".
- In an interview, lead with the greedy solution and the counterexample, *then* offer the DP. Volunteering "greedy is suboptimal, here's why, and here's the DP fix" is the signal.

### Source
Anthropic phone screen follow-up (companion to `anthropic-tokenizer.md`).
