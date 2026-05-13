"""
Debug problem — medium recursion

Two recursive functions. Tests in test_recursion_medium.py fail. Find and fix.

Hint: 1 bug per function.
  - One bug is a classic backtracking footgun about mutable state.
  - One bug is in how multi-character tokens are accumulated.
"""


def permutations(nums):
    """Return all permutations of the distinct integers in `nums`."""
    result = []

    def backtrack(current, remaining):
        if not remaining:
            result.append(current)
            return
        for i in range(len(remaining)):
            current.append(remaining[i])
            backtrack(current, remaining[:i] + remaining[i + 1 :])
            current.pop()

    backtrack([], nums)
    return result


def decode_string(s):
    """Decode strings like '3[a2[c]]' -> 'accaccacc'.

    Grammar: a decoded string is a sequence of either literal letters or
    `<digits>[<inner>]` blocks, where the digits give a repeat count.
    """

    def helper(i):
        result = ""
        while i < len(s) and s[i] != "]":
            if s[i].isdigit():
                k = 0
                while s[i].isdigit():
                    k = k + int(s[i])
                    i += 1
                # skip '['
                i += 1
                sub, i = helper(i)
                # skip ']'
                i += 1
                result += sub * k
            else:
                result += s[i]
                i += 1
        return result, i

    decoded, _ = helper(0)
    return decoded
