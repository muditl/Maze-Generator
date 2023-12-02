import numpy as np
from src.Grid import Grid
from src.Cell import Cell


class Distances:
    def __init__(self, grid, starting_point=(0, 0)):
        self.grid = grid
        self.distances_array = np.full_like(grid.cells, -1)
        self.__calculate_distances(grid, starting_point)

    def __reset_distances(self):
        self.distances_array = np.full_like(self.grid.cells, -1)

    def __calculate_distances(self, grid, starting_point):
        x, y = starting_point
        frontier = [grid.get_cell(x, y)]
        self.distances_array[x, y] = 0
        d = 1
        while len(frontier) > 0:
            new_frontier = []
            for f in frontier:
                neighbors = f.get_linked_neighbors()
                for n in neighbors:
                    p = n.get_position()
                    if self.distances_array[p] == -1:
                        self.distances_array[p] = d
                        new_frontier.append(n)
            d += 1
            frontier = new_frontier

    def __getitem__(self, item):
        return self.distances_array[item]

    def __str__(self):
        return str(self.distances_array)

    def get_furthest_cell_location(self):
        return np.unravel_index(np.argmax(self.distances_array, axis=None), self.distances_array.shape)

    def get_start_cell_location(self):
        return np.unravel_index(np.argmin(self.distances_array, axis=None), self.distances_array.shape)

    def get_longest_path_sequence(self):
        self.__set_longest_distances_array()
        start = self.get_start_cell_location()
        end = self.get_furthest_cell_location()
        current = self.grid.get_cell(*end)
        path = [end]
        while current != self.grid.get_cell(*start):
            _next = self.__get_previous_location(current)
            path.append(_next.get_position())
            current = _next
        return path

    def __get_previous_location(self, current_cell: Cell):
        linked_neighbours = current_cell.get_linked_neighbors()
        for n in linked_neighbours:
            pos = n.get_position()
            if self.distances_array[pos] == self.distances_array[current_cell.get_position()] - 1:
                return self.grid.get_cell(*pos)

    def __set_longest_distances_array(self):
        # choose a random point
        x = int(np.random.rand(1)[0] * self.grid.shape[0])
        y = int(np.random.rand(1)[0] * self.grid.shape[1])
        self.__reset_distances()
        self.__calculate_distances(self.grid, (x, y))
        furthest_start = self.get_furthest_cell_location()
        self.__reset_distances()
        self.__calculate_distances(self.grid, furthest_start)

