from src.Grid import Grid
from src.Cell import Cell
import unittest
from unittest.mock import patch, call


class TestCell(unittest.TestCase):

    def setUp(self) -> None:
        self.grid = Grid(10, 10)

    def test_cell_instantiate(self):
        new_cell = Cell(10, 10)
        self.assertIsNotNone(new_cell)
        self.assertEqual((10, 10), new_cell.get_position())

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
        cell1 = self.grid.get_cell(4, 5)
        cell2 = self.grid.get_cell(4, 6)
        self.assertTrue(cell1.check_unlink(cell2))
        self.assertTrue(cell2.check_unlink(cell1))
        cell1.link(cell2)
        self.assertTrue(cell1.check_link(cell2))
        self.assertTrue(cell2.check_link(cell1))

    @patch('builtins.print')
    def test_link_invalid(self, mocked_print):
        cell1 = self.grid.get_cell(3, 6)
        cell2 = self.grid.get_cell(6, 3)
        cell1.link(cell2)
        self.assertTrue(cell1.check_unlink(cell2))
        self.assertTrue(cell2.check_unlink(cell1))
        self.assertEqual([call('\x1b[33mInternal Warning: Cell is not a neighbor, could not link!\x1b[0m')],
                         mocked_print.mock_calls)

    def test_unlink(self):
        cell1 = self.grid.get_cell(4, 5)
        cell2 = self.grid.get_cell(4, 6)
        self.assertTrue(cell1.check_unlink(cell2))
        self.assertTrue(cell2.check_unlink(cell1))
        cell1.link(cell2)
        self.assertTrue(cell1.check_link(cell2))
        self.assertTrue(cell2.check_link(cell1))
        cell1.unlink(cell2)
        self.assertTrue(cell1.check_unlink(cell2))
        self.assertTrue(cell2.check_unlink(cell1))

    def test_get_neighbors_middle(self):
        i, j = 3, 4
        cell = self.grid.get_cell(i, j)
        neighbors = [self.grid.get_cell(i - 1, j), self.grid.get_cell(i + 1, j), self.grid.get_cell(i, j + 1),
                     self.grid.get_cell(i, j - 1)]
        self.assertCountEqual(neighbors, cell.get_neighbors())

    def test_get_neighbors_edges(self):
        i, j = 0, 5
        cell = self.grid.get_cell(i, j)
        neighbors = [self.grid.get_cell(i + 1, j), self.grid.get_cell(i, j + 1), self.grid.get_cell(i, j - 1)]
        self.assertCountEqual(neighbors, cell.get_neighbors())

        i, j = 9, 4
        cell = self.grid.get_cell(i, j)
        neighbors = [self.grid.get_cell(i - 1, j), self.grid.get_cell(i, j + 1), self.grid.get_cell(i, j - 1)]
        self.assertCountEqual(neighbors, cell.get_neighbors())

        i, j = 4, 0
        cell = self.grid.get_cell(i, j)
        neighbors = [self.grid.get_cell(i - 1, j), self.grid.get_cell(i + 1, j), self.grid.get_cell(i, j + 1)]
        self.assertCountEqual(neighbors, cell.get_neighbors())

        i, j = 5, 9
        cell = self.grid.get_cell(i, j)
        neighbors = [self.grid.get_cell(i - 1, j), self.grid.get_cell(i + 1, j), self.grid.get_cell(i, j - 1)]
        self.assertCountEqual(neighbors, cell.get_neighbors())

    def test_get_neighbors_corners(self):
        i, j = 0, 0
        cell = self.grid.get_cell(i, j)
        neighbors = [self.grid.get_cell(i + 1, j), self.grid.get_cell(i, j + 1), ]
        self.assertCountEqual(neighbors, cell.get_neighbors())

        i, j = 0, 9
        cell = self.grid.get_cell(i, j)
        neighbors = [self.grid.get_cell(i + 1, j), self.grid.get_cell(i, j - 1)]
        self.assertCountEqual(neighbors, cell.get_neighbors())

        i, j = 9, 0
        cell = self.grid.get_cell(i, j)
        neighbors = [self.grid.get_cell(i - 1, j), self.grid.get_cell(i, j + 1)]
        self.assertCountEqual(neighbors, cell.get_neighbors())

        i, j = 9, 9
        cell = self.grid.get_cell(i, j)
        neighbors = [self.grid.get_cell(i - 1, j), self.grid.get_cell(i, j - 1)]
        self.assertCountEqual(neighbors, cell.get_neighbors())

    def test_get_linked_unlinked_neighbors(self):
        i, j = 4, 5
        cell = self.grid.get_cell(i, j)
        neighbors = cell.get_neighbors()

        linked = []
        unlinked = neighbors
        self.assertCountEqual(unlinked, cell.get_unlinked_neighbors())
        self.assertCountEqual(linked, cell.get_linked_neighbors())

        cell.link(neighbors[2])
        unlinked = [neighbors[0], neighbors[1], neighbors[3]]
        linked = [neighbors[2]]
        self.assertCountEqual(unlinked, cell.get_unlinked_neighbors())
        self.assertCountEqual(linked, cell.get_linked_neighbors())

        cell.link(neighbors[3])
        unlinked = [neighbors[0], neighbors[1]]
        linked = [neighbors[2], neighbors[3]]
        self.assertCountEqual(unlinked, cell.get_unlinked_neighbors())
        self.assertCountEqual(linked, cell.get_linked_neighbors())

        cell.unlink(neighbors[2])
        unlinked = [neighbors[0], neighbors[1], neighbors[2]]
        linked = [neighbors[3]]
        self.assertCountEqual(unlinked, cell.get_unlinked_neighbors())
        self.assertCountEqual(linked, cell.get_linked_neighbors())

    def test_get_closed_neighbors(self):
        i, j = 4, 5
        cell = self.grid.get_cell(i, j)
        neighbors = cell.get_neighbors()

        closed = neighbors
        self.assertCountEqual(closed, cell.get_closed_neighbors())

        cell.link(neighbors[1])
        closed = [neighbors[0], neighbors[2], neighbors[3]]
        self.assertCountEqual(closed, cell.get_closed_neighbors())

        cell.unlink(neighbors[1])

        neighbors[3].link(neighbors[3].get_neighbors()[0])
        closed = neighbors[0:3]
        self.assertCountEqual(closed, cell.get_closed_neighbors())

        neighbors[2].link(neighbors[2].get_neighbors()[1])
        closed = neighbors[0:2]
        self.assertCountEqual(closed, cell.get_closed_neighbors())

    def test_mark_unmark(self):
        cell = self.grid.get_cell(4, 5)
        self.assertEqual(cell.marker, 0)

        cell.mark(24)
        self.assertEqual(cell.marker, 24)

        cell.unmark()
        self.assertEqual(cell.marker, 0)

    def test_calculate_image_code(self):
        cell = self.grid.get_cell(3, 5)
        image_code = 0b0000
        self.assertEqual(image_code, cell.get_image_code())

        cell.link(cell.north)
        image_code = 0b1000
        self.assertEqual(image_code, cell.get_image_code())

        cell.link(cell.east)
        image_code = 0b1010
        self.assertEqual(image_code, cell.get_image_code())

        cell.link(cell.south)
        image_code = 0b1110
        self.assertEqual(image_code, cell.get_image_code())

        cell.link(cell.west)
        image_code = 0b1111
        self.assertEqual(image_code, cell.get_image_code())

    def test_cell__str__(self):
        i, j = 3, 6
        cell = self.grid.get_cell(i, j)
        c_str = "(" + str(i) + ", " + str(j) + ")"
        self.assertEqual(c_str, str(cell))

    def test_cell_verbose__str__(self):
        i, j = 3, 6
        cell = self.grid.get_cell(i, j)
        c_str = "Cell((3, 6)), north:(2, 6), south:(4, 6), east:(3, 7), west:(3, 5)"
        self.assertEqual(c_str, cell.verbose__str__())

        i, j = 9, 9
        cell = self.grid.get_cell(i, j)
        c_str = "Cell((9, 9)), north:(8, 9), south:None, east:None, west:(9, 8)"
        self.assertEqual(c_str, cell.verbose__str__())
