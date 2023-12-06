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
        self.turn_straight_ratio = 0
        self.longest_path = []
        self.longest_path_length = 0
        self.longest_path_turns = 0
        self.longest_path_straights = 0
        self._longest_path_turn_straight_ratio = 0
        self.longest_path_triple_branches = 0
        self.longest_path_quad_branches = 0
        self.longest_path_branches = 0
        if self.is_perfect_maze():
            self.__calculate_metrics()

    def change_maze_to(self, grid):
        self.__init__(grid)

    def get_metrics_array(self):
        return [self.dead_ends, self.branch_points, self.triple_branch, self.quad_branch, self.straights, self.turns,
                self.turn_straight_ratio, self.longest_path_length, self.longest_path_branches,
                self.longest_path_triple_branches, self.longest_path_quad_branches, self.longest_path_straights,
                self.longest_path_straights, self.longest_path_turns, self._longest_path_turn_straight_ratio]

    def __calculate_metrics(self):
        self.dead_ends = 0
        self.branch_points = 0
        self.triple_branch = 0
        self.quad_branch = 0
        self.straights = 0
        self.turns = 0
        for row in self.grid:
            for cell in row:
                num_links = len(cell.get_linked_neighbors())
                if num_links == 1:
                    self.dead_ends += 1
                elif num_links == 2:
                    if Analysis.__is_straight(cell):
                        self.straights += 1
                    else:
                        self.turns += 1
                else:
                    if num_links == 3:
                        self.triple_branch += 1
                    elif num_links == 4:
                        self.quad_branch += 1
                    self.branch_points += 1
        self.longest_path = Distances(self.grid).get_longest_path_sequence()
        self.longest_path_length = len(self.longest_path)

        if self.straights == 0:
            self.turn_straight_ratio = self.turns / 0.1
        else:
            self.turn_straight_ratio = self.turns / self.straights

        for x, y in self.longest_path:
            cell = self.grid.get_cell(x, y)
            num_links = len(cell.get_linked_neighbors())
            if num_links == 2:
                if Analysis.__is_straight(cell):
                    self.longest_path_straights += 1
                else:
                    self.longest_path_turns += 1
            else:
                if num_links == 3:
                    self.longest_path_triple_branches += 1
                elif num_links == 4:
                    self.longest_path_quad_branches += 1
                self.longest_path_branches += 1
        if self.longest_path_straights==0:
            self._longest_path_turn_straight_ratio = self.longest_path_turns/0.1
        else:
            self._longest_path_turn_straight_ratio = self.longest_path_turns / self.longest_path_straights

    @staticmethod
    def __is_straight(cell: Cell):
        if cell.check_link(cell.north) and cell.check_link(cell.south):
            return True
        if cell.check_link(cell.east) and cell.check_link(cell.west):
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
