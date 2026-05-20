## Number
N/A
## Tags
python,idiom,list-comprehension
### Name
Nested list comprehensions — flatten vs. list-of-lists
### Problem
Given a list of lists (or any iterable of iterables), produce a single flat list of its elements. Then: understand why putting **two `for`s in one comprehension** flattens, but **nesting `[...]` inside the expression slot** produces a list-of-lists.

```python
classrooms = [["Alice", "Bob"], ["Carol"], ["Dan", "Eve"]]
# want: ["Alice", "Bob", "Carol", "Dan", "Eve"]
```
### Solution
Read every `for`/`if` clause **left-to-right exactly as you'd write the nested loop**. The leading expression is what gets appended at the innermost level.

```python
# flatten one level
[student for classroom in classrooms for student in classroom]
# -> ["Alice", "Bob", "Carol", "Dan", "Eve"]
```

is the same as:

```python
out = []
for classroom in classrooms:        # outer (first for)
    for student in classroom:       # inner (second for)
        out.append(student)         # leading expr
```

Mental rule:

- `[expr for A for B]`     → **flatten** (nested loops, single flat list)
- `[[expr for B] for A]`   → **list of lists** (inner comp is the expr; only outer for-loop at top level)

Inner clauses can reference outer ones — that's how you build cross products / triangles:

```python
[(i, j) for i in range(3) for j in range(i)]   # j depends on i
# -> [(1,0), (2,0), (2,1)]
```

Gotchas:

- `sum([sublist for sublist in lists], [])` works for flattening but is **O(n²)** (each `+` copies). Prefer the comprehension or `itertools.chain.from_iterable(lists)`.
- Don't confuse with `np.concatenate` / `np.flatten` — those are NumPy-only and don't accept ragged Python lists.
- For deeper nesting (list of list of lists), you need either three `for`s or recursion — comprehensions don't recurse on their own.
- `for/if` order matters: `[x for x in xs if cond]` filters; `[x if cond else y for x in xs]` is element-wise ternary in the expression slot.
### Source
Interview practice (Problem 9 debug — `tree_files_at_depth` in `python/debug/tree_fns/`).
