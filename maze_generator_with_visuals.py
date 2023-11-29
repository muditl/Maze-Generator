import cv2
from Grid import Grid
import numpy as np
from maze_visuals_plus import make_maze_visual_marked, make_maze_visual_color
from maze_solver import find_distances
from maze_visuals import make_maze_visual
from maze_generator import *

top = cv2.imread("images/top.png")
bottom = cv2.imread("images/bottom.png")
right = cv2.imread("images/right.png")
left = cv2.imread("images/left.png")


def binary_algorithm_vis(grid: Grid):
    # iterate from bottom left corner
    for i in range(grid.shape[0] - 1, -1, -1):
        for j in range(grid.shape[1]):
            cell = grid.get_cell(i, j)
            cell.mark(1)
            # find neighbors of cell (only north and east)
            neighbors = bin_get_neighbors_vis(cell)

            # 10 - neighbours
            for n in neighbors:
                n.mark(10)
            display_grid(grid)

            # if no northern and eastern neighbors, move to next cell
            if len(neighbors) == 0:
                pass
            # if only 1 neighbor, link to current cell
            elif len(neighbors) == 1:
                cell.link(neighbors[0])
                neighbors[0].mark(11)
            # if 2 neighbors, pick one randomly and link to current cell
            elif len(neighbors) == 2:
                index = np.random.randint(2)
                neighbors[index].mark(11)
                display_grid(grid)
                neighbors[0].mark(0)
                neighbors[1].mark(0)

                cell.link(neighbors[index])
            cell.mark(100)
            display_grid(grid)
    return grid


def bin_get_neighbors_vis(cell: Cell):
    neighbors = []
    if cell.north is not None:
        neighbors.append(cell.north)
    if cell.east is not None:
        neighbors.append(cell.east)
    return neighbors


def display_grid(grid, show=True, save: str = None):
    image = make_maze_visual_marked(grid, top, bottom, right, left)

    if show:
        cv2.imshow("Maze", image)
        cv2.waitKeyEx(0)
        cv2.destroyAllWindows()
    if save:
        cv2.imwrite(save, image)


# the sidewinder algorithm
def sidewinder_vis(grid: Grid):
    # define run varible
    run = []

    # iterate from bottom left corner
    for i in range(grid.shape[0] - 1, -1, -1):
        for j in range(grid.shape[1]):
            cell = grid.get_cell(i, j)
            cell.mark(1)
            display_grid(grid)
            # if run has been terminated, restart it
            if len(run) == 0:
                run.append(cell)

            # coin flip
            tails = True if np.random.rand() > 0.5 else False

            # if not on east edge and Tails, link cell to east
            if cell.east is not None and tails:
                cell.link(cell.east)
                run.append(cell.east)
                cell.east.mark(2)

            # else, if not on northern border, link a random cell in run to north
            elif cell.north is not None:
                sw_close_run(grid, run)
                for c in run:
                    c.mark(100)
                run = []
            # link every cell in northern border to east (boundary condition on northeast corner)
            elif cell.east is not None:
                cell.link(cell.east)
            display_grid(grid)
    return grid


# closes the run for sidewinder algorithm (links a random cell in the run to its northern neighbor)
def sw_close_run(grid, run):
    rand_idx = np.random.randint(len(run))
    run[rand_idx].link(run[rand_idx].north)
    run[rand_idx].mark(10)
    display_grid(grid)
    run[rand_idx].mark(100)


def aldous_broder_vis(grid: Grid):
    # random starting point
    random_i = np.random.randint(0, grid.shape[0])
    random_j = np.random.randint(0, grid.shape[1])
    cell = grid.get_cell(random_i, random_j)

    # unvisited cells
    unvisited = grid.shape[0] * grid.shape[1] - 1
    visited = [cell]

    # until the entire grid has been visited
    while unvisited > 0:
        cell.mark(1)

        # pick random neighbor of cell
        neighbors = cell.get_neighbors()
        idx = np.random.randint(len(neighbors))
        neighbor = neighbors[idx]

        for c in neighbors:
            c.mark(10)

        neighbor.mark(2)
        display_grid(grid)
        for c in neighbors:
            c.mark(0)
        visited.append(neighbor)
        # if neighbor unvisited
        if len(neighbor.links) == 0:
            # link to current cell
            cell.link(neighbor)
            unvisited -= 1

        # make neighbor current cell
        cell = neighbor
        for c in visited:
            c.mark(100)

    return grid


def wilson_vis(grid):
    count = 0
    # add all cells to unvisited
    unvisited = []
    for row in grid:
        for cell in row:
            unvisited.append(cell)

    # pick random cell and remove from unvisited
    rand = np.random.randint(len(unvisited))
    first = unvisited[rand]
    unvisited.remove(first)
    first.mark(100)
    display_grid(grid, False, "wilson/grid" + str(count) + ".png")
    count += 1
    # while there are unvisited cells
    while len(unvisited) > 0:

        # pick random unvisited cell
        rand = np.random.randint(len(unvisited))
        cell = unvisited[rand]
        # instantiate current run with cell
        run = [cell]
        cell.mark(2)
        display_grid(grid, False, "wilson/grid" + str(count) + ".png")
        count += 1
        # while we do not hit a visited cell
        while unvisited.__contains__(cell):
            # randomly visit a neighbor
            neighbors = cell.get_neighbors()
            idx = np.random.randint(len(neighbors))
            cell = neighbors[idx]
            cell.mark(10)
            position = 0
            display_grid(grid, False, "wilson/grid" + str(count) + ".png")
            count += 1
            # check if the current run already has cell (to detect loop)
            if run.__contains__(cell):
                position = run.index(cell)

            # if it does, remove the loop i.e. keep all cells until first occurence of cell
            if position:
                run[position].mark(11)
                display_grid(grid, False, "wilson/grid" + str(count) + ".png")
                count += 1
                run[position].mark(10)
                for c in run[position + 1:]:
                    c.mark(0)
                display_grid(grid, False, "wilson/grid" + str(count) + ".png")
                count += 1
                run = run[:position + 1]

            # otherwise, append to current run
            else:
                run.append(cell)

        # once we hit a visited cell, remove boundaries to connect run and remove cells from unvisited

        for c in run:
            c.mark(100)
            if unvisited.__contains__(c):
                unvisited.remove(c)
            cell.link(c)
            cell = c
        display_grid(grid, False, "wilson/grid" + str(count) + ".png")
        count += 1

    return grid


def hunt_and_kill_vis(grid: Grid):
    # random starting point
    random_i = np.random.randint(0, grid.shape[0])
    random_j = np.random.randint(0, grid.shape[1])
    current = grid.get_cell(random_i, random_j)
    current.mark(100)
    display_grid(grid)

    # while there are unvisited cells
    while current:
        # find unvisited neighbors (those that have no links, i.e. are closed)
        unvisited_neighbors = current.get_closed_neighbors()
        for c in unvisited_neighbors:
            c.mark(2)
        display_grid(grid)
        for c in unvisited_neighbors:
            c.mark(0)

        # if neighbors, pick a random one and link
        if len(unvisited_neighbors) > 0:
            idx = np.random.randint(0, len(unvisited_neighbors))
            neighbor = unvisited_neighbors[idx]
            neighbor.mark(10)
            display_grid(grid)
            neighbor.mark(100)
            current.link(neighbor)
            current = neighbor

        # otherwise, do a search in grid for a cell that is unvisited but has a visited neighbor
        else:
            current = None
            flag = True
            for row in grid:
                if flag:
                    for cell in row:
                        if flag:
                            visited_neighbors = cell.get_neighbors()
                            unvisited_neighbors = cell.get_closed_neighbors()
                            for n in unvisited_neighbors:
                                visited_neighbors.remove(n)

                            # once an unvisited cell with a visited neighbor is found,
                            # link to one of the visited neighbors
                            # and continue algorithm from there
                            if len(cell.links) == 0 and len(visited_neighbors) > 0:
                                cell.mark(11)
                                current = cell
                                idx = np.random.randint(0, len(visited_neighbors))
                                neighbor = visited_neighbors[idx]
                                current.link(neighbor)
                                display_grid(grid)
                                cell.mark(100)
                                flag = False
    return grid


griddy = Grid(6, 6)

# binary_algorithm_vis(griddy)
# sidewinder_vis(griddy)
# aldous_broder_vis(griddy)
# wilson_vis(griddy)


hunt_and_kill_vis(griddy)

distances = find_distances(griddy, (0, 0))
image = make_maze_visual(griddy, top, bottom, right, left)

# print(distances.cells)

cv2.imshow("grid", image)
cv2.waitKeyEx(0)
cv2.destroyAllWindows()


# cv2.imwrite("grid.jpg", image)

def longest_path(grid):
    randx, randy = np.random.rand(2)
    randx = int(randx * grid.shape[0])
    randy = int(randy * grid.shape[1])

    d = find_distances(grid, (randx, randy))
    maxi = np.unravel_index(np.argmax(d.distances_array, axis=None), d.distances_array.shape)

    d = find_distances(grid, maxi)
    # print(d)


longest_path(griddy)
