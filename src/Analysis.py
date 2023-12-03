from src.Cell import Cell
from src.Grid import Grid
from src.Distances import Distances
from numpy import full_like, any


class Analysis:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.dead_ends = 0
        self.branch_points = 0
        self.triple_branch = 0
        self.quad_branch = 0
        self.straights = 0
        self.turns = 0
        self.__calculate_metrics()

    def change_maze_to(self, grid):
        self.__init__(grid)

    def __calculate_metrics(self):
        self.dead_ends = 0
        self.branch_points = 0
        self.triple_branch = 0
        self.quad_branch = 0
        self.straights = 0
        self.turns = 0

        for row in self.grid:
            for cell in row:
                num_neighbors = len(cell.get_linked_neighbors())
                if num_neighbors == 1:
                    self.dead_ends += 1
                elif num_neighbors == 2:
                    if Analysis.__is_straight(cell):
                        self.straights += 1
                    else:
                        self.turns += 1
                else:
                    if num_neighbors == 3:
                        self.triple_branch += 1
                    elif num_neighbors == 4:
                        self.quad_branch += 1
                    self.branch_points += 1

    @staticmethod
    def __is_straight(cell: Cell):
        if cell.north is not None and cell.south is not None:
            return True
        if cell.east is not None and cell.west is not None:
            return True
        return False

    # 1. all places reachable
    # 2. no loops, i.e. only one path from A to B.
    def is_perfect_maze(self):
        distances = Distances(self.grid)
        if any(distances.distances_array == -1):
            return False

        return self.count_links()

    # count how many missing edges there are. if there are more than 2*((x*y)-1), there are too many and
    # a loop must exist
    def count_links(self):
        expected = (self.grid.shape[0] * self.grid.shape[1] - 1) * 2
        actual = 0
        for row in self.grid:
            for cell in row:
                actual += len(cell.get_linked_neighbors())
        return expected == actual
