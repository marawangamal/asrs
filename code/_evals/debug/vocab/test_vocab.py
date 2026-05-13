import unittest

from vocab import Vocab


class TestVocab(unittest.TestCase):
    def test_unk_is_zero(self):
        v = Vocab([("the", 5), ("a", 3)])
        self.assertEqual(v.token_to_id[Vocab.UNK], 0)

    def test_ids_match_inverse_table(self):
        v = Vocab([("the", 5), ("a", 3)])
        # Whatever id "the" has, id_to_token[that id] must equal "the".
        self.assertEqual(v.id_to_token[v.token_to_id["the"]], "the")
        self.assertEqual(v.id_to_token[v.token_to_id["a"]], "a")

    def test_descending_count_then_alphabetical(self):
        v = Vocab([("the", 5), ("a", 3), ("z", 5)])
        # "the" and "z" tie at count 5; "the" wins alphabetically -> id 1.
        self.assertEqual(v.token_to_id["the"], 1)
        self.assertEqual(v.token_to_id["z"], 2)
        self.assertEqual(v.token_to_id["a"], 3)

    def test_min_count_drops_rare(self):
        v = Vocab([("the", 5), ("rare", 1)], min_count=2)
        self.assertNotIn("rare", v.token_to_id)
        self.assertEqual(len(v), 2)  # UNK + "the"

    def test_encode_known(self):
        v = Vocab([("the", 5), ("a", 3)])
        self.assertEqual(
            v.encode("the a the"),
            [v.token_to_id["the"], v.token_to_id["a"], v.token_to_id["the"]],
        )

    def test_encode_unknown_maps_to_unk(self):
        v = Vocab([("the", 5)])
        self.assertEqual(v.encode("xyz the foo"), [0, v.token_to_id["the"], 0])

    def test_decode_roundtrip(self):
        v = Vocab([("the", 5), ("a", 3)])
        text = "the a the a"
        self.assertEqual(v.decode(v.encode(text)), text)


if __name__ == "__main__":
    unittest.main()
