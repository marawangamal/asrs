# Review history

## 2026-05-13T18:13 — code/algos/1166-design-file-system.md — again
Missed the card's whole point: reached for a tree first when the lesson is "use a flat dict — no traversal needed." Also invented file/folder type semantics the problem doesn't ask for. Drill: parent of `/a` is `""` not `"/"`; use `path[:path.rfind("/")]`. Trie/tree only when problem 588 (`ls`, enumeration) is in scope.

## 2026-05-13T18:10 — code/algos/141-linked-list-cycle.md — good
Floyd's tortoise-and-hare captured: two pointers, slow +1, fast +2, meeting = cycle. Slips: framed start as index `i=j=0` instead of `slow = fast = head` (these are pointers), and gave loop guard as `while j.next` instead of `while fast and fast.next` — the missing `fast and` check crashes on cycle-less lists when fast reaches None. Didn't state O(n)/O(1).

## 2026-05-13T18:08 — code/algos/211-add-search-words.md — good
Captured the trie + lazy node creation + `is_end` flag + wildcard branching into all children. Two minor slips: framed the root as "having all lowercase chars as children" (children are populated lazily) and didn't explicitly state the wildcard returns true if any child succeeds. Drill: search base case is `i == len(word) and node.is_end` — the flag is what distinguishes a stored word from a prefix.

## 2026-05-12T17:15 — code/algos/278-first-bad-version.md — good
Framed it as bisect_left(1) over the virtual 0/1 array (good → 0, bad → 1) — correct mental model. Did not write out the lo/hi update rules; brief slip saying bisect_right before correcting to bisect_left. Drill the invariant next time: `hi = mid` when bad (could be answer), `lo = mid + 1` when good (not answer).

## 2026-05-11T19:45 — code/algos/208-implement-trie.md — again
Got the basic tree idea but stated O(n log n) complexity instead of O(n); missed the critical `is_end` flag that distinguishes a complete word from a prefix during `search`.

## 2026-05-11T19:30 — code/algos/11-container-with-most-water.md — again
No attempt. Core idea to drill: two pointers from both ends, always move the shorter pointer inward — moving the taller one can never improve the area since the bound is the shorter line and width only decreases.

## 2026-05-11T19:23 — code/algos/209-min-subarray-sum.md — again
User had no recall at all ("I dont know"). Next time, prompt them on the variable-size sliding window pattern: expand right to grow sum, contract left while sum ≥ target. Key constraint to remember: works only because all values are positive (monotone window).

## 2026-05-11T19:28 — code/algos/1244-leaderboard.md — good
Nailed addScore (dict + get-or-init). Right approach for top (sort-on-query) but skipped the sum step — said "use a sorting algorithm" without mentioning that top returns sum of top K values. Said reset "removes the user" instead of setting to 0 — operationally equivalent only because addScore uses .get(..., 0); flag this if it comes up again. Asked about big-O up front — good instinct.

## 2026-05-11T19:55 — code/algos/3-longest-substring-no-repeat.md — again
User had no answer. Core idea to remember: variable-size sliding window with a hash map storing each character's most recent index; jump `left` to `seen[ch] + 1` when a duplicate is found inside the current window.

## 2026-05-13T23:14 — code/algos/anthropic-tokenizer.md — hard
Got the core two-pointer greedy-longest-match structure (outer i, inner j shrinking from right). Missed: UNK fallback when j shrinks to i with no match, resetting j after each match, and both follow-ups (max-length pruning, UNK collapsing). Next time push for the UNK emit-and-advance branch explicitly.

## 2026-06-06T00:00 — code/algos/981-time-based-kv-store.md — again
Got the structure (dict str->list, bisect_right, step back one) but fell into the exact card gotcha: used max(0, idx-1) instead of `if idx==0: return ""`. Also hand-rolled bisect_right was broken — never used the search val (compared arr[mid] >= arr[left]) and left=mid with left<=right infinite-loops.
