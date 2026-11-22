"""Run from the repository root: python -m unittest discover -v"""
import unittest
from topology_twin import create_twin, set_link, topology_accuracy, validate_matrix

class TestTopologyTwin(unittest.TestCase):
    def setUp(self):
        self.network = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]

    def test_initial_copy_is_independent(self):
        twin = create_twin(self.network)
        self.assertEqual(topology_accuracy(self.network, twin), 1.0)
        set_link(self.network, 0, 1, False)
        self.assertEqual(twin[0][1], 1)

    def test_one_changed_link(self):
        twin = create_twin(self.network)
        set_link(self.network, 0, 1, False)
        self.assertAlmostEqual(topology_accuracy(self.network, twin), 2 / 3)

    def test_refresh(self):
        twin = create_twin(self.network)
        set_link(self.network, 0, 1, False)
        twin = create_twin(self.network)
        self.assertEqual(topology_accuracy(self.network, twin), 1.0)

    def test_invalid_matrix(self):
        with self.assertRaises(ValueError):
            validate_matrix([[0, 1], [0, 0]])

    def test_different_sizes(self):
        with self.assertRaises(ValueError):
            topology_accuracy(self.network, [[0, 1], [1, 0]])


if __name__ == "__main__":
    unittest.main()
