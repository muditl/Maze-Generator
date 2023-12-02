import numpy as np
from src.Grid import Grid
import cv2
from src.Distances import Distances

top = cv2.imread("../images/top.png")
bottom = cv2.imread("../images/bottom.png")
right = cv2.imread("../images/right.png")
left = cv2.imread("../images/left.png")


def make_cell_image(cell_image_code, north, south, east, west):
    flags = get_flags_from_code(cell_image_code)
    image = cv2.imread("../images/blank.png")

    if flags[0]:  # north
        image[0:15, 15:105] = north[0:15, 15:105, :]
    if flags[1]:  # south
        image[105:120, 15:105] = south[105:120, 15:105, :]
    if flags[2]:  # east
        image[15:105, 105:120] = east[15:105, 105:120]
    if flags[3]:  # west
        image[15:105, 0:15] = west[15:105, 0:15]
    return image


def get_flags_from_code(code):
    # north, south, east, west
    flags = [False, False, False, False]
    # convert to binary number with 4 digits
    binary_string = str(format(code, '#06b'))
    if binary_string[2] == '0':
        flags[0] = True
    if binary_string[3] == '0':
        flags[1] = True
    if binary_string[4] == '0':
        flags[2] = True
    if binary_string[5] == '0':
        flags[3] = True
    return flags


def make_maze_visual(grid, north, south, east, west):
    final_image = np.zeros((grid.shape[0] * 120, grid.shape[1] * 120, 3), np.uint8)
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            cell_image_code = cell.get_image_code()
            cell_image = make_cell_image(cell_image_code, north, south, east, west)

            final_image[i * 120:(i + 1) * 120, j * 120:(j + 1) * 120] = cell_image
    return final_image


def make_distances_visual(grid):
    grid_image = make_maze_visual(grid, top, bottom, right, left)
    d = Distances(grid, (0, 0))

    for row in grid:
        for c in row:
            pos = c.get_position()


def save_maze_png(image):
    cv2.imwrite("../maze.png", image)
