from src.Grid import Grid
from src.Cell import Cell
import unittest
from src.Analysis import Analysis
import cv2
from src.Visuals import make_maze_visual


class TestCell(unittest.TestCase):

    def setUp(self) -> None:
        self.grid_perfect_1 = Grid(4, 4)
        self.grid_not_perfect_1 = Grid(4, 4)
        self.grid_perfect_2 = Grid(4, 4)
        self.grid_not_perfect_2 = Grid(4, 4)
        self.make_grids()

    def test_is_perfect_maze(self):
        self.assertTrue(Analysis(self.grid_perfect_1).is_perfect_maze())
        self.assertTrue(Analysis(self.grid_perfect_2).is_perfect_maze())

    def test_not_perfect_not_reachable(self):
        self.assertFalse(Analysis(self.grid_not_perfect_1).is_perfect_maze())

    def test_not_perfect_loop(self):
        self.assertFalse(Analysis(self.grid_not_perfect_2).is_perfect_maze())

    def test_metrics(self):
        self.assertListEqual([5, 2, 1, 1, 3, 6, 11, 4, 1, 1, 3, 1], Analysis(self.grid_perfect_1).get_metrics_array())
        self.assertListEqual([4, 2, 2, 0, 4, 6, 12, 4, 2, 0, 3, 0], Analysis(self.grid_perfect_2).get_metrics_array())

    def make_grids(self):
        self.grid_perfect_1.get_cell(0, 0).link(self.grid_perfect_1.get_cell(0, 1))
        self.grid_perfect_1.get_cell(0, 1).link(self.grid_perfect_1.get_cell(1, 1))
        self.grid_perfect_1.get_cell(0, 2).link(self.grid_perfect_1.get_cell(1, 2))
        self.grid_perfect_1.get_cell(0, 3).link(self.grid_perfect_1.get_cell(0, 2))
        self.grid_perfect_1.get_cell(1, 0).link(self.grid_perfect_1.get_cell(2, 0))
        self.grid_perfect_1.get_cell(1, 1).link(self.grid_perfect_1.get_cell(1, 2))
        self.grid_perfect_1.get_cell(1, 2).link(self.grid_perfect_1.get_cell(1, 3))
        self.grid_perfect_1.get_cell(1, 3).link(self.grid_perfect_1.get_cell(2, 3))
        self.grid_perfect_1.get_cell(2, 0).link(self.grid_perfect_1.get_cell(2, 1))
        self.grid_perfect_1.get_cell(2, 1).link(self.grid_perfect_1.get_cell(1, 1))
        self.grid_perfect_1.get_cell(2, 2).link(self.grid_perfect_1.get_cell(1, 2))
        self.grid_perfect_1.get_cell(2, 3).link(self.grid_perfect_1.get_cell(3, 3))
        self.grid_perfect_1.get_cell(3, 0).link(self.grid_perfect_1.get_cell(3, 1))
        self.grid_perfect_1.get_cell(3, 1).link(self.grid_perfect_1.get_cell(3, 2))
        self.grid_perfect_1.get_cell(3, 2).link(self.grid_perfect_1.get_cell(3, 3))

        self.grid_perfect_2.get_cell(0, 0).link(self.grid_perfect_2.get_cell(0, 1))
        self.grid_perfect_2.get_cell(0, 1).link(self.grid_perfect_2.get_cell(0, 2))
        self.grid_perfect_2.get_cell(0, 2).link(self.grid_perfect_2.get_cell(1, 2))
        self.grid_perfect_2.get_cell(0, 3).link(self.grid_perfect_2.get_cell(1, 3))
        self.grid_perfect_2.get_cell(1, 0).link(self.grid_perfect_2.get_cell(1, 1))
        self.grid_perfect_2.get_cell(1, 1).link(self.grid_perfect_2.get_cell(2, 1))
        self.grid_perfect_2.get_cell(1, 2).link(self.grid_perfect_2.get_cell(1, 1))
        self.grid_perfect_2.get_cell(1, 3).link(self.grid_perfect_2.get_cell(2, 3))
        self.grid_perfect_2.get_cell(2, 0).link(self.grid_perfect_2.get_cell(1, 0))
        self.grid_perfect_2.get_cell(2, 1).link(self.grid_perfect_2.get_cell(3, 1))
        self.grid_perfect_2.get_cell(2, 2).link(self.grid_perfect_2.get_cell(3, 2))
        self.grid_perfect_2.get_cell(2, 3).link(self.grid_perfect_2.get_cell(2, 2))
        self.grid_perfect_2.get_cell(3, 0).link(self.grid_perfect_2.get_cell(2, 0))
        self.grid_perfect_2.get_cell(3, 1).link(self.grid_perfect_2.get_cell(3, 2))
        self.grid_perfect_2.get_cell(3, 2).link(self.grid_perfect_2.get_cell(3, 3))

        self.grid_not_perfect_1.get_cell(0, 0).link(self.grid_not_perfect_1.get_cell(0, 1))
        self.grid_not_perfect_1.get_cell(0, 1).link(self.grid_not_perfect_1.get_cell(1, 1))
        self.grid_not_perfect_1.get_cell(0, 2).link(self.grid_not_perfect_1.get_cell(1, 2))
        self.grid_not_perfect_1.get_cell(0, 3).link(self.grid_not_perfect_1.get_cell(0, 2))
        self.grid_not_perfect_1.get_cell(1, 1).link(self.grid_not_perfect_1.get_cell(1, 2))
        self.grid_not_perfect_1.get_cell(1, 2).link(self.grid_not_perfect_1.get_cell(1, 3))
        self.grid_not_perfect_1.get_cell(1, 3).link(self.grid_not_perfect_1.get_cell(2, 3))
        self.grid_not_perfect_1.get_cell(2, 0).link(self.grid_not_perfect_1.get_cell(2, 1))
        self.grid_not_perfect_1.get_cell(2, 1).link(self.grid_not_perfect_1.get_cell(1, 1))
        self.grid_not_perfect_1.get_cell(2, 2).link(self.grid_not_perfect_1.get_cell(1, 2))
        self.grid_not_perfect_1.get_cell(2, 3).link(self.grid_not_perfect_1.get_cell(3, 3))
        self.grid_not_perfect_1.get_cell(3, 0).link(self.grid_not_perfect_1.get_cell(3, 1))
        self.grid_not_perfect_1.get_cell(3, 1).link(self.grid_not_perfect_1.get_cell(3, 2))
        self.grid_not_perfect_1.get_cell(3, 2).link(self.grid_not_perfect_1.get_cell(3, 3))

        self.grid_not_perfect_2.get_cell(0, 0).link(self.grid_not_perfect_2.get_cell(0, 1))
        self.grid_not_perfect_2.get_cell(0, 1).link(self.grid_not_perfect_2.get_cell(0, 2))
        self.grid_not_perfect_2.get_cell(0, 2).link(self.grid_not_perfect_2.get_cell(1, 2))
        self.grid_not_perfect_2.get_cell(0, 3).link(self.grid_not_perfect_2.get_cell(1, 3))
        self.grid_not_perfect_2.get_cell(1, 0).link(self.grid_not_perfect_2.get_cell(1, 1))
        self.grid_not_perfect_2.get_cell(1, 1).link(self.grid_not_perfect_2.get_cell(2, 1))
        self.grid_not_perfect_2.get_cell(1, 2).link(self.grid_not_perfect_2.get_cell(1, 1))
        self.grid_not_perfect_2.get_cell(1, 3).link(self.grid_not_perfect_2.get_cell(2, 3))
        self.grid_not_perfect_2.get_cell(2, 0).link(self.grid_not_perfect_2.get_cell(1, 0))
        self.grid_not_perfect_2.get_cell(2, 1).link(self.grid_not_perfect_2.get_cell(3, 1))
        self.grid_not_perfect_2.get_cell(2, 2).link(self.grid_not_perfect_2.get_cell(3, 2))
        self.grid_not_perfect_2.get_cell(2, 3).link(self.grid_not_perfect_2.get_cell(2, 2))
        self.grid_not_perfect_2.get_cell(3, 0).link(self.grid_not_perfect_2.get_cell(2, 0))
        self.grid_not_perfect_2.get_cell(3, 1).link(self.grid_not_perfect_2.get_cell(3, 2))
        self.grid_not_perfect_2.get_cell(3, 2).link(self.grid_not_perfect_2.get_cell(3, 3))
        self.grid_not_perfect_2.get_cell(0, 0).link(self.grid_not_perfect_2.get_cell(1, 0))
