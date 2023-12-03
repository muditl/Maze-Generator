import numpy as np
from src.Grid import Grid
from src.Cell import Cell


class Generator:

    def __init__(self, i, j):
        self.x = i
        self.y = j

    def resize_grid(self, i, j):
        self.__init__(i, j)

    # makes very simple mazes
    def binary_algorithm(self):
        grid = Grid(self.x, self.y)
        # iterate from bottom left corner
        for i in range(grid.shape[0] - 1, -1, -1):
            for j in range(grid.shape[1]):
                cell = grid.get_cell(i, j)
                # find neighbors of cell (only north and east)
                neighbors = Generator.__bin_get_neighbors(cell)
                # if no northern and eastern neighbors, move to next cell
                if len(neighbors) == 0:
                    pass
                # if only 1 neighbor, link to current cell
                elif len(neighbors) == 1:
                    cell.link(neighbors[0])
                # if 2 neighbors, pick one randomly and link to current cell
                elif len(neighbors) == 2:
                    index = np.random.randint(2)
                    cell.link(neighbors[index])
        return grid

    # return north and east neighbours, if they exist
    @staticmethod
    def __bin_get_neighbors(cell: Cell):
        neighbors = []
        if cell.north is not None:
            neighbors.append(cell.north)
        if cell.east is not None:
            neighbors.append(cell.east)
        return neighbors

    # the sidewinder algorithm
    def sidewinder(self):
        grid = Grid(self.x, self.y)
        # define run varible
        run = []

        # iterate from bottom left corner
        for i in range(grid.shape[0] - 1, -1, -1):
            for j in range(grid.shape[1]):
                cell = grid.get_cell(i, j)

                # if run has been terminated, restart it
                if len(run) == 0:
                    run.append(cell)

                # coin flip, Tails is True
                tails = True if np.random.rand() > 0.5 else False

                # if not on east edge and Tails, link cell to east
                if cell.east is not None and tails:
                    cell.link(cell.east)
                    run.append(cell.east)

                # else, if not on northern border, link a random cell in run to north
                elif cell.north is not None:
                    Generator.__sw_close_run(run)
                    run = []
                # link every cell in northern border to east (boundary condition on northeast corner)
                elif cell.east is not None:
                    cell.link(cell.east)
        return grid

    # closes the run for sidewinder algorithm (links a random cell in the run to its northern neighbor)
    @staticmethod
    def __sw_close_run(run):
        rand_idx = np.random.randint(len(run))
        run[rand_idx].link(run[rand_idx].north)

    def aldous_broder(self):
        grid = Grid(self.x, self.y)
        # random starting point
        random_i = np.random.randint(0, grid.shape[0])
        random_j = np.random.randint(0, grid.shape[1])
        cell = grid.get_cell(random_i, random_j)

        # unvisited cells
        unvisited = grid.shape[0] * grid.shape[1] - 1

        # until the entire grid has been visited
        while unvisited > 0:
            # pick random neighbor of cell
            neighbors = cell.get_neighbors()
            idx = np.random.randint(len(neighbors))
            neighbor = neighbors[idx]

            # if neighbor unvisited
            if len(neighbor.links) == 0:
                # link to current cell
                cell.link(neighbor)
                unvisited -= 1

            # make neighbor current cell
            cell = neighbor

        return grid

    def wilson(self):
        grid = Grid(self.x, self.y)
        # add all cells to unvisited
        unvisited = []
        for row in grid:
            for cell in row:
                unvisited.append(cell)

        # pick random cell and remove from unvisited
        rand = np.random.randint(len(unvisited))
        first = unvisited[rand]
        unvisited.remove(first)

        # while there are unvisited cells
        while len(unvisited) > 0:
            # pick random unvisited cell
            rand = np.random.randint(len(unvisited))
            cell = unvisited[rand]
            # instantiate current run with cell
            run = [cell]

            # while we do not hit a visited cell
            while unvisited.__contains__(cell):
                # randomly visit a neighbor
                neighbors = cell.get_neighbors()
                idx = np.random.randint(len(neighbors))
                cell = neighbors[idx]
                position = 0

                # check if the current run already has cell (to detect loop)
                if run.__contains__(cell):
                    position = run.index(cell)

                # if it does, remove the loop i.e. keep all cells until first occurence of cell
                if position:
                    run = run[:position + 1]
                # otherwise, append to current run
                else:
                    run.append(cell)

            # once we hit a visited cell, remove boundaries to connect run and remove cells from unvisited
            for c in run:
                if unvisited.__contains__(c):
                    unvisited.remove(c)
                cell.link(c)
                cell = c

        return grid

    def hunt_and_kill(self):
        grid = Grid(self.x, self.y)
        # random starting point
        random_i = np.random.randint(0, grid.shape[0])
        random_j = np.random.randint(0, grid.shape[1])
        current = grid.get_cell(random_i, random_j)

        # while there are unvisited cells
        while current:
            # find unvisited neighbors (those that have no links, i.e. are closed)
            unvisited_neighbors = current.get_closed_neighbors()

            # if neighbors, pick a random one and link
            if len(unvisited_neighbors) > 0:
                idx = np.random.randint(0, len(unvisited_neighbors))
                neighbor = unvisited_neighbors[idx]
                current.link(neighbor)
                current = neighbor

            # otherwise, do a search in grid for a cell that is unvisited but has a visited neighbor
            else:
                current = None
                for row in grid:
                    for cell in row:
                        visited_neighbors = cell.get_neighbors()
                        unvisited_neighbors = cell.get_closed_neighbors()
                        for n in unvisited_neighbors:
                            visited_neighbors.remove(n)

                        # once an unvisited cell with a visited neighbor is found, link to one of the visited neighbors
                        # and continue algorithm from there
                        if len(cell.links) == 0 and len(visited_neighbors) > 0:
                            current = cell
                            idx = np.random.randint(0, len(visited_neighbors))
                            neighbor = visited_neighbors[idx]
                            current.link(neighbor)
        return grid

    def recursive_backtracker(self):
        grid = Grid(self.x, self.y)
        random_i = np.random.randint(0, grid.shape[0])
        random_j = np.random.randint(0, grid.shape[1])
        stack = [grid.get_cell(random_i, random_j)]

        while len(stack) > 0:
            current = stack[-1]
            neighbors = current.get_closed_neighbors()

            if len(neighbors) == 0:
                stack.remove(current)
            else:
                rand_i = np.random.randint(0, len(neighbors))
                neighbor = neighbors[rand_i]
                current.link(neighbor)
                stack.append(neighbor)

        return grid
