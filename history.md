# Review history

## 2026-05-11T19:45 — code/208-implement-trie.md — again
Got the basic tree idea but stated O(n log n) complexity instead of O(n); missed the critical `is_end` flag that distinguishes a complete word from a prefix during `search`.

## 2026-05-11T19:30 — code/11-container-with-most-water.md — again
No attempt. Core idea to drill: two pointers from both ends, always move the shorter pointer inward — moving the taller one can never improve the area since the bound is the shorter line and width only decreases.

## 2026-05-11T19:23 — code/209-min-subarray-sum.md — again
User had no recall at all ("I dont know"). Next time, prompt them on the variable-size sliding window pattern: expand right to grow sum, contract left while sum ≥ target. Key constraint to remember: works only because all values are positive (monotone window).

## 2026-05-11T19:28 — code/1244-leaderboard.md — good
Nailed addScore (dict + get-or-init). Right approach for top (sort-on-query) but skipped the sum step — said "use a sorting algorithm" without mentioning that top returns sum of top K values. Said reset "removes the user" instead of setting to 0 — operationally equivalent only because addScore uses .get(..., 0); flag this if it comes up again. Asked about big-O up front — good instinct.

## 2026-05-11T19:55 — code/3-longest-substring-no-repeat.md — again
User had no answer. Core idea to remember: variable-size sliding window with a hash map storing each character's most recent index; jump `left` to `seen[ch] + 1` when a duplicate is found inside the current window.
