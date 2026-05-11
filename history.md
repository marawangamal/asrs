# Review history

## 2026-05-11T19:23 — code/209-min-subarray-sum.md — again
User had no recall at all ("I dont know"). Next time, prompt them on the variable-size sliding window pattern: expand right to grow sum, contract left while sum ≥ target. Key constraint to remember: works only because all values are positive (monotone window).

## 2026-05-11T19:28 — code/1244-leaderboard.md — good
Nailed addScore (dict + get-or-init). Right approach for top (sort-on-query) but skipped the sum step — said "use a sorting algorithm" without mentioning that top returns sum of top K values. Said reset "removes the user" instead of setting to 0 — operationally equivalent only because addScore uses .get(..., 0); flag this if it comes up again. Asked about big-O up front — good instinct.
