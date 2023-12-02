from src.Cell import Cell
from src.Grid import Grid
from src.Distances import Distances
from numpy import full_like, any


class Analysis:
    def __init__(self, grid: Grid):
        self.grid = grid

    def change_maze_to(self, grid):
        self.__init__(grid)

    def run(self):
        pass

    def count_dead_ends(self):
        pass

    def count_branch_points(self):
        pass

    def count_turns(self):
        pass

    def count_straights(self):
        pass

    def calculate_difficulty(self):
        pass

    # 2 conditions
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
