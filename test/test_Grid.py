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

# coverage run --source=./test -m unittest discover -s test/ && coverage report
# python -m coverage run --source= test -m unittest discover -s test
