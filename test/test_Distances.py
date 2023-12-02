from src.Distances import Distances
from src.Grid import Grid
import unittest
from numpy import array, array_equal


class TestDistances(unittest.TestCase):

    def setUp(self) -> None:
        self.grid1 = Grid(4, 4)
        self.grid2 = Grid(4, 4)
        self.make_grids()

    def test_init(self):
        d = Distances(self.grid1)
        self.assertIsNotNone(d)

    def test_calculate_distances(self):
        d1 = array([[0, 1, 4, 5], [5, 2, 3, 4], [4, 3, 4, 5], [9, 8, 7, 6]])
        d2 = array([[0, 1, 2, 11], [5, 4, 3, 10], [6, 5, 8, 9], [7, 6, 7, 8]])
        self.assertTrue(array_equal(Distances(self.grid1).distances_array, d1))
        self.assertTrue(array_equal(Distances(self.grid2).distances_array, d2))

    def test_get_longest_path_sequence(self):
        expected_s1 = [(3, 0), (3, 1), (3, 2), (3, 3), (2, 3), (1, 3), (1, 2), (1, 1), (2, 1), (2, 0), (1, 0)]
        expected_s2 = [(0, 0), (0, 1), (0, 2), (1, 2), (1, 1), (2, 1), (3, 1), (3, 2), (2, 2), (2, 3), (1, 3), (0, 3)]
        actual_s1 = Distances(self.grid1).get_longest_path_sequence()
        actual_s2 = Distances(self.grid2).get_longest_path_sequence()
        rev_s1 = list(reversed(expected_s1))
        rev_s2 = list(reversed(expected_s2))
        self.assertTrue(expected_s1 == actual_s1 or rev_s1 == actual_s1)
        self.assertTrue(expected_s2 == actual_s2 or rev_s2 == actual_s2)

    def make_grids(self):
        self.grid1.get_cell(0, 0).link(self.grid1.get_cell(0, 1))
        self.grid1.get_cell(0, 1).link(self.grid1.get_cell(1, 1))
        self.grid1.get_cell(0, 2).link(self.grid1.get_cell(1, 2))
        self.grid1.get_cell(0, 3).link(self.grid1.get_cell(0, 2))
        self.grid1.get_cell(1, 0).link(self.grid1.get_cell(2, 0))
        self.grid1.get_cell(1, 1).link(self.grid1.get_cell(1, 2))
        self.grid1.get_cell(1, 2).link(self.grid1.get_cell(1, 3))
        self.grid1.get_cell(1, 3).link(self.grid1.get_cell(2, 3))
        self.grid1.get_cell(2, 0).link(self.grid1.get_cell(2, 1))
        self.grid1.get_cell(2, 1).link(self.grid1.get_cell(1, 1))
        self.grid1.get_cell(2, 2).link(self.grid1.get_cell(1, 2))
        self.grid1.get_cell(2, 3).link(self.grid1.get_cell(3, 3))
        self.grid1.get_cell(3, 0).link(self.grid1.get_cell(3, 1))
        self.grid1.get_cell(3, 1).link(self.grid1.get_cell(3, 2))
        self.grid1.get_cell(3, 2).link(self.grid1.get_cell(3, 3))

        self.grid2.get_cell(0, 0).link(self.grid2.get_cell(0, 1))
        self.grid2.get_cell(0, 1).link(self.grid2.get_cell(0, 2))
        self.grid2.get_cell(0, 2).link(self.grid2.get_cell(1, 2))
        self.grid2.get_cell(0, 3).link(self.grid2.get_cell(1, 3))
        self.grid2.get_cell(1, 0).link(self.grid2.get_cell(1, 1))
        self.grid2.get_cell(1, 1).link(self.grid2.get_cell(2, 1))
        self.grid2.get_cell(1, 2).link(self.grid2.get_cell(1, 1))
        self.grid2.get_cell(1, 3).link(self.grid2.get_cell(2, 3))
        self.grid2.get_cell(2, 0).link(self.grid2.get_cell(1, 0))
        self.grid2.get_cell(2, 1).link(self.grid2.get_cell(3, 1))
        self.grid2.get_cell(2, 2).link(self.grid2.get_cell(3, 2))
        self.grid2.get_cell(2, 3).link(self.grid2.get_cell(2, 2))
        self.grid2.get_cell(3, 0).link(self.grid2.get_cell(2, 0))
        self.grid2.get_cell(3, 1).link(self.grid2.get_cell(3, 2))
        self.grid2.get_cell(3, 2).link(self.grid2.get_cell(3, 3))
