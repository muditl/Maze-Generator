import numpy as np
from Grid import Grid
from maze_generator import binary_algorithm


def find_distances(grid: Grid, starting_position):
    distances = Distances(grid)
    x, y = starting_position
    frontier = [grid.get_cell(x, y)]
    distances.cells[x, y] = 0
    d = 1
    while len(frontier) > 0:
        new_frontier = []
        for f in frontier:
            neighbors = f.get_linked_neighbors()
            for n in neighbors:
                p = n.get_position()
                if distances.cells[p] == -1:
                    distances.cells[p] = d
                    new_frontier.append(n)
        d += 1
        frontier = new_frontier

    return distances

def find_furthest_point():
    pass

def find_longest_path():
    pass


class Distances:
    def __init__(self, grid):
        self.cells = np.full_like(grid.cells, -1)

    def __getitem__(self, item):
        return self.cells[item]

    def set_distance(self, i, j, d):
        self.cells[i, j] = d

    def __str__(self):
        return str(self.cells)


print(find_distances(binary_algorithm(Grid(5, 5)), (0, 0)).cells)
