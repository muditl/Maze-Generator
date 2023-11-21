from Grid import *
from pytest import raises


# -------------- CELL TESTS -------------- #
def test_cell_instantiate():
    new_cell = Cell(10, 10)
    assert (new_cell is not None)
    assert (new_cell.position == (10, 10))


def test_raises_invalid_row_column_exception():
    with raises(Exception) as e_info:
        cell = Cell(-5, 2)
    assert (e_info.value.args[0] == 'Given row or column invalid: (-5, 2)')

    with raises(Exception) as e_info:
        cell = Cell(3, -4)
    assert (e_info.value.args[0] == 'Given row or column invalid: (3, -4)')

    with raises(Exception) as e_info:
        cell = Cell(-1, -6)
    assert (e_info.value.args[0] == 'Given row or column invalid: (-1, -6)')


def test_link():
    cell1 = Cell(4, 5)
    cell2 = Cell(4, 6)
    assert (cell1.check_unlink(cell2) is True)
    assert (cell2.check_unlink(cell1) is True)
    cell1.link(cell2)
    assert (cell1.check_link(cell2) is True)
    assert (cell2.check_link(cell1) is True)


def test_unlink():
    cell1 = Cell(4, 5)
    cell2 = Cell(4, 6)
    assert (cell1.check_unlink(cell2) is True)
    assert (cell2.check_unlink(cell1) is True)
    cell1.link(cell2)
    assert (cell1.check_link(cell2) is True)
    assert (cell2.check_link(cell1) is True)
    cell1.unlink(cell2)
    assert (cell1.check_unlink(cell2) is True)
    assert (cell2.check_unlink(cell1) is True)


# -------------- GRID TESTS -------------- #
def test_initialise_grid():
    x = 10
    y = 10
    grid = Grid(x, y)
    assert (grid.cells.shape == (10, 10))
    assert (isinstance(grid.get_cell(5, 1), Cell))
    for i in range(x):
        for j in range(y):
            assert (grid.get_cell(i, j).position == (i, j))
            # indexing from top left
            if i > 0:
                assert (grid.get_cell(i, j).north == grid.get_cell(i - 1, j))
            else:
                assert (grid.get_cell(i, j).north is None)
            if j > 0:
                assert (grid.get_cell(i, j).west == grid.get_cell(i, j - 1))
            else:
                assert (grid.get_cell(i, j).west is None)
            if i < x - 1:
                assert (grid.get_cell(i, j).south == grid.get_cell(i + 1, j))
            else:
                assert (grid.get_cell(i, j).south is None)
            if j < y - 1:
                assert (grid.get_cell(i, j).east == grid.get_cell(i, j + 1))
            else:
                assert (grid.get_cell(i, j).east is None)


def test_get_neighbors():
    grid = Grid(5, 5)
    for i in range(5):
        for j in range(5):
            neighbors = grid.get_cell(i, j).get_neighbors()
            if 0 < i < 4 and 0 < j < 4:  # central cells
                assert (neighbors[0] == grid.get_cell(i - 1, j))  # north
                assert (neighbors[1] == grid.get_cell(i + 1, j))  # south
                assert (neighbors[2] == grid.get_cell(i, j + 1))  # east
                assert (neighbors[3] == grid.get_cell(i, j - 1))  # west
            elif i == 0 and 0 < j < 4:  # northern border
                assert (neighbors[0] == grid.get_cell(i + 1, j))  # south
                assert (neighbors[1] == grid.get_cell(i, j + 1))  # west
                assert (neighbors[2] == grid.get_cell(i, j - 1))  # east
            elif i == 4 and 0 < j < 4:  # southern border
                assert (neighbors[0] == grid.get_cell(i - 1, j))  # north
                assert (neighbors[1] == grid.get_cell(i, j + 1))  # east
                assert (neighbors[2] == grid.get_cell(i, j - 1))  # west
            elif 0 < i < 4 and j == 0:  # western border
                assert (neighbors[0] == grid.get_cell(i - 1, j))  # north
                assert (neighbors[1] == grid.get_cell(i + 1, j))  # south
                assert (neighbors[2] == grid.get_cell(i, j + 1))  # east
            elif 0 < i < 4 and j == 4:  # eastern border
                assert (neighbors[0] == grid.get_cell(i - 1, j))  # north
                assert (neighbors[1] == grid.get_cell(i + 1, j))  # south
                assert (neighbors[2] == grid.get_cell(i, j - 1))  # west
            elif i == 0 and j == 0:  # north-west corner
                assert (neighbors[0] == grid.get_cell(i + 1, j))  # south
                assert (neighbors[1] == grid.get_cell(i, j + 1))  # east
            elif i == 0 and j == 4:  # north-east corner
                assert (neighbors[0] == grid.get_cell(i + 1, j))  # south
                assert (neighbors[1] == grid.get_cell(i, j - 1))  # west
            elif i == 4 and j == 0:  # south-west corner
                assert (neighbors[0] == grid.get_cell(i - 1, j))  # north
                assert (neighbors[1] == grid.get_cell(i, j + 1))  # east
            elif i == 4 and j == 4:  # south-east corner
                assert (neighbors[0] == grid.get_cell(i - 1, j))  # north
                assert (neighbors[1] == grid.get_cell(i, j - 1))  # west



# TODO make test for calculate image,

def test_some_runner_code():
    grid = Grid(5, 5)
