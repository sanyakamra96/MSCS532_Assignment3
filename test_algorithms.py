"""Run with python -m unittest -v."""
import unittest
from quicksort import randomized_quicksort, deterministic_quicksort
from hash_table import ChainedHashTable


class AlgorithmTests(unittest.TestCase):
    def test_sort_edge_cases(self):
        cases = [[], [1], [3, 3, 3], [1, 2, 3, 4], [4, 3, 2, 1],
                 [0, -2, 1, -2, 100, 0], list(range(1000))]
        for case in cases:
            for sort in (randomized_quicksort, deterministic_quicksort):
                with self.subTest(sort=sort.__name__, case_size=len(case)):
                    original = list(case)
                    self.assertEqual(sort(case), sorted(case))
                    self.assertEqual(case, original)

    def test_hash_insert_search_update_delete(self):
        table = ChainedHashTable(capacity=2, seed=532)
        for key in range(-100, 100):
            table.insert(key, str(key))
        self.assertEqual(len(table), 200)
        self.assertLessEqual(table.load_factor, 0.75)
        for key in range(-100, 100):
            self.assertEqual(table.search(key), str(key))
        table.insert(3, "updated")
        self.assertEqual(table.search(3), "updated")
        self.assertEqual(len(table), 200)
        for key in range(-100, 100):
            table.delete(key)
        self.assertEqual(len(table), 0)
        with self.assertRaises(KeyError):
            table.search(3)
        with self.assertRaises(KeyError):
            table.delete(3)

    def test_hash_collision_and_validation(self):
        table = ChainedHashTable(capacity=1, seed=1)
        table.insert(1, None)
        self.assertIsNone(table.search(1))
        with self.assertRaises(TypeError):
            table.insert("not integer", 1)
        with self.assertRaises(ValueError):
            ChainedHashTable(capacity=0)


if __name__ == "__main__":
    unittest.main()
