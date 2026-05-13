"""
Debug problem — Vocab class

A Vocab maps tokens (strings) to integer ids and back. Tests in
test_vocab.py fail.

Hint: 2 bugs, in __init__ and encode. Watch for what gets indexed in
a dict comprehension (and whether UNK lands at id 0), and the dict
lookup that explodes on unseen tokens.
"""


class Vocab:
    UNK = "<unk>"

    def __init__(self, tokens, min_count=1):
        """Build vocab from an iterable of (token, count) pairs.

        - UNK is always id 0.
        - Remaining tokens are assigned ids 1, 2, ... in descending
          count order; ties broken by token (alphabetical).
        - Tokens with count < min_count are dropped.
        """
        # breakpoint()
        kept = [(t, c) for t, c in tokens if c >= min_count]
        kept.sort(key=lambda tc: (-tc[1], tc[0]))
        self.id_to_token = [Vocab.UNK] + [t for t, _ in kept]
        self.token_to_id = {t: i for i, t in enumerate(self.id_to_token)}

    def __len__(self):
        return len(self.id_to_token)

    def encode(self, text):
        """Whitespace-tokenize `text` and return a list of ids. Tokens
        not in the vocabulary map to UNK (id 0).
        """
        return [self.token_to_id.get(w, 0) for w in text.split()]

    def decode(self, ids):
        """Inverse of encode: ids -> space-joined tokens."""
        return " ".join(self.id_to_token[i] for i in ids)
