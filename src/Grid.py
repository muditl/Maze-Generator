import numpy as np
from src.Cell import Cell


class Grid:

    def __init__(self, x=25, y=25):
        self.shape = (x, y)
        self.cells = np.zeros(shape=(x, y), dtype=Cell)
        self.initialise_cells()

    # Check if removing this breaks anything...
    # def __iter__(self):
    #     return self.cells.__iter__()

    def initialise_cells(self):
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                self.cells[i, j] = Cell(i, j)

        # indexing from top left
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                self.cells[i, j].north = (self.cells[i - 1, j] if i > 0 else None)
                self.cells[i, j].south = (self.cells[i + 1, j] if i < self.shape[1] - 1 else None)
                self.cells[i, j].east = (self.cells[i, j + 1] if j < self.shape[0] - 1 else None)
                self.cells[i, j].west = (self.cells[i, j - 1] if j > 0 else None)

    def get_cell(self, i, j) -> Cell:
        return self.cells[i, j]

    def __str__(self):
        res = ""
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                res += str(self.cells[i, j]) + ", "
            res += "\n"
        return res[:-3]
