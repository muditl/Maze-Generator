from src.Cell import Cell
from src.Grid import Grid
import unittest


class TestGrid(unittest.TestCase):
    def test_initialise_grid(self):
        x = 10
        y = 10
        grid = Grid(x, y)
        self.assertEqual((10, 10), grid.cells.shape)
        assert (isinstance(grid.get_cell(5, 1), Cell))
        for i in range(x):
            for j in range(y):
                self.assertEqual((i, j), grid.get_cell(i, j).position)
                # indexing from top left
                if i > 0:
                    self.assertEqual(grid.get_cell(i - 1, j), grid.get_cell(i, j).north)
                else:
                    self.assertIsNone(grid.get_cell(i, j).north)
                if j > 0:
                    self.assertEqual(grid.get_cell(i, j - 1), grid.get_cell(i, j).west)
                else:
                    self.assertIsNone(grid.get_cell(i, j).west)
                if i < x - 1:
                    self.assertEqual(grid.get_cell(i + 1, j), grid.get_cell(i, j).south)
                else:
                    self.assertIsNone(grid.get_cell(i, j).south)
                if j < y - 1:
                    self.assertEqual(grid.get_cell(i, j + 1), grid.get_cell(i, j).east)
                else:
                    self.assertIsNone(grid.get_cell(i, j).east)

    def test_get_neighbors(self):
        grid = Grid(5, 5)
        for i in range(5):
            for j in range(5):
                neighbors = grid.get_cell(i, j).get_neighbors()
                if 0 < i < 4 and 0 < j < 4:  # central cells
                    self.assertEqual(grid.get_cell(i - 1, j), neighbors[0])  # north
                    self.assertEqual(grid.get_cell(i + 1, j), neighbors[1])  # south
                    self.assertEqual(grid.get_cell(i, j + 1), neighbors[2])  # east
                    self.assertEqual(grid.get_cell(i, j - 1), neighbors[3])  # west
                elif i == 0 and 0 < j < 4:  # northern border
                    self.assertEqual(grid.get_cell(i + 1, j), neighbors[0])  # south
                    self.assertEqual(grid.get_cell(i, j + 1), neighbors[1])  # west
                    self.assertEqual(grid.get_cell(i, j - 1), neighbors[2])  # east
                elif i == 4 and 0 < j < 4:  # southern border
                    self.assertEqual(grid.get_cell(i - 1, j), neighbors[0])  # north
                    self.assertEqual(grid.get_cell(i, j + 1), neighbors[1])  # east
                    self.assertEqual(grid.get_cell(i, j - 1), neighbors[2])  # west
                elif 0 < i < 4 and j == 0:  # western border
                    self.assertEqual(grid.get_cell(i - 1, j), neighbors[0])  # north
                    self.assertEqual(grid.get_cell(i + 1, j), neighbors[1])  # south
                    self.assertEqual(grid.get_cell(i, j + 1), neighbors[2])  # east
                elif 0 < i < 4 and j == 4:  # eastern border
                    self.assertEqual(grid.get_cell(i - 1, j), neighbors[0])  # north
                    self.assertEqual(grid.get_cell(i + 1, j), neighbors[1])  # south
                    self.assertEqual(grid.get_cell(i, j - 1), neighbors[2])  # west
                elif i == 0 and j == 0:  # north-west corner
                    self.assertEqual(grid.get_cell(i + 1, j), neighbors[0])  # south
                    self.assertEqual(grid.get_cell(i, j + 1), neighbors[1])  # east
                elif i == 0 and j == 4:  # north-east corner
                    self.assertEqual(grid.get_cell(i + 1, j), neighbors[0])  # south
                    self.assertEqual(grid.get_cell(i, j - 1), neighbors[1])  # west
                elif i == 4 and j == 0:  # south-west corner
                    self.assertEqual(grid.get_cell(i - 1, j), neighbors[0])  # north
                    self.assertEqual(grid.get_cell(i, j + 1), neighbors[1])  # east
                elif i == 4 and j == 4:  # south-east corner
                    self.assertEqual(grid.get_cell(i - 1, j), neighbors[0])  # north
                    self.assertEqual(grid.get_cell(i, j - 1), neighbors[1])  # west

    def test_str(self):
        grid = Grid(5, 5)
        expected = "(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), \n" + \
                   "(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), \n" + \
                   "(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), \n" + \
                   "(3, 0), (3, 1), (3, 2), (3, 3), (3, 4), \n" + \
                   "(4, 0), (4, 1), (4, 2), (4, 3), (4, 4)"
        self.assertEqual(expected, grid.__str__())

    def test_get_markers_str(self):
        grid = Grid(5, 5)
        expected = "0 0 0 0 0 \n" + \
                   "0 0 0 0 0 \n" + \
                   "0 0 0 0 0 \n" + \
                   "0 0 0 0 0 \n" + \
                   "0 0 0 0 0"
        self.assertEqual(expected, grid.get_markers_str())

# python -m coverage run --source=src -m unittest discover -s test
# python -m coverage report
