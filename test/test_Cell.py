from src.Grid import Grid
from src.Cell import Cell
import unittest


class TestCell(unittest.TestCase):
    def test_cell_instantiate(self):
        new_cell = Cell(10, 10)
        self.assertIsNotNone(new_cell)
        self.assertEqual((10, 10), new_cell.position)

    def test_raises_invalid_row_column_exception(self):
        with self.assertRaises(Exception) as ctx:
            Cell(-5, 2)
        self.assertEqual('Given row or column invalid: (-5, 2)', str(ctx.exception))

        with self.assertRaises(Exception) as ctx:
            Cell(-5, 2)
        self.assertEqual('Given row or column invalid: (-5, 2)', str(ctx.exception))

        with self.assertRaises(Exception) as ctx:
            Cell(3, -4)
        self.assertEqual('Given row or column invalid: (3, -4)', str(ctx.exception))

        with self.assertRaises(Exception) as ctx:
            Cell(-1, -6)
        self.assertEqual('Given row or column invalid: (-1, -6)', str(ctx.exception))

    def test_link(self):
        grid = Grid(10, 10)
        cell1 = grid.get_cell(4, 5)
        cell2 = grid.get_cell(4, 6)
        self.assertTrue(cell1.check_unlink(cell2))
        self.assertTrue(cell2.check_unlink(cell1))
        cell1.link(cell2)
        self.assertTrue(cell1.check_link(cell2))
        self.assertTrue(cell2.check_link(cell1))

    def test_unlink(self):
        grid = Grid(10, 10)
        cell1 = grid.get_cell(4, 5)
        cell2 = grid.get_cell(4, 6)
        self.assertTrue(cell1.check_unlink(cell2))
        self.assertTrue(cell2.check_unlink(cell1))
        cell1.link(cell2)
        self.assertTrue(cell1.check_link(cell2))
        self.assertTrue(cell2.check_link(cell1))
        cell1.unlink(cell2)
        self.assertTrue(cell1.check_unlink(cell2))
        self.assertTrue(cell2.check_unlink(cell1))
