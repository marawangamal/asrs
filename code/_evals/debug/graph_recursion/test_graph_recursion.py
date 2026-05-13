import unittest

from graph_recursion import count_components, has_cycle, has_path


class TestHasPath(unittest.TestCase):
    def test_direct(self):
        g = {1: [2], 2: []}
        self.assertTrue(has_path(g, 1, 2))

    def test_transitive(self):
        g = {1: [2], 2: [3], 3: []}
        self.assertTrue(has_path(g, 1, 3))

    def test_unreachable(self):
        g = {1: [2], 2: [], 3: [4], 4: []}
        self.assertFalse(has_path(g, 1, 4))

    def test_called_twice_does_not_carry_state(self):
        # If a second call were polluted by the first call's `visited`,
        # an actually-reachable target would look unreachable.
        g = {1: [2], 2: [3], 3: []}
        self.assertTrue(has_path(g, 1, 3))
        self.assertTrue(has_path(g, 1, 3))


class TestCountComponents(unittest.TestCase):
    def test_one_component(self):
        g = {1: [2], 2: [1, 3], 3: [2]}
        self.assertEqual(count_components(g), 1)

    def test_two_components(self):
        g = {1: [2], 2: [1], 3: [4], 4: [3]}
        self.assertEqual(count_components(g), 2)

    def test_singletons(self):
        g = {1: [], 2: [], 3: []}
        self.assertEqual(count_components(g), 3)


class TestHasCycle(unittest.TestCase):
    def test_no_cycle_chain(self):
        g = {1: [2], 2: [3], 3: []}
        self.assertFalse(has_cycle(g))

    def test_dag_diamond_is_not_a_cycle(self):
        # Both 2 and 3 point to 4 — a re-visit, not a cycle.
        g = {1: [2, 3], 2: [4], 3: [4], 4: []}
        self.assertFalse(has_cycle(g))

    def test_self_loop(self):
        g = {1: [1]}
        self.assertTrue(has_cycle(g))

    def test_three_cycle(self):
        g = {1: [2], 2: [3], 3: [1]}
        self.assertTrue(has_cycle(g))


if __name__ == "__main__":
    unittest.main()
