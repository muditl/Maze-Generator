from Grid import *
import cv2


def make_cell_image_marked(cell_image_code, north, south, east, west, marker):
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

    # current cell
    if marker == 1:
        image[15:105, 15:105] = [16, 146, 37]

    # current group
    if marker == 2:
        image[15:105, 15:105] = [165, 195, 86]

    # current group
    if marker == 9:
        image[15:105, 15:105] = [114, 128, 250]

    # shortlist, e.g. neighbours, unlinked etc.
    if marker == 10:
        image[15:105, 15:105] = [60, 189, 251]

    # selected
    if marker == 11:
        image[15:105, 15:105] = [157, 147, 0]

    # visited
    if marker == 100:
        image[15:105, 15:105] = [201, 255, 186]

    return image


def make_cell_image_distances(cell_image_code, north, south, east, west, distance, highest):
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

    color = 255 - int(255 * distance / highest)

    image[15:105, 15:105] = [color/3, color, color/2]

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


def make_maze_visual_marked(grid, north, south, east, west):
    final_image = np.zeros((grid.shape[0] * 120, grid.shape[1] * 120, 3), np.uint8)
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            cell_image_code = cell.calculate_image_code()
            cell_image = make_cell_image_marked(cell_image_code, north, south, east, west, cell.marker)

            final_image[i * 120:(i + 1) * 120, j * 120:(j + 1) * 120] = cell_image
    return final_image


def make_maze_visual_color(grid, north, south, east, west, distances):
    high = distances.distances_array.max()
    final_image = np.zeros((grid.shape[0] * 120, grid.shape[1] * 120, 3), np.uint8)
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            cell_image_code = cell.calculate_image_code()
            cell_image = make_cell_image_distances(cell_image_code, north, south, east, west,
                                                   distances.__getitem__(cell.get_position()), high)

            final_image[i * 120:(i + 1) * 120, j * 120:(j + 1) * 120] = cell_image
    return final_image


def save_maze_png(image):
    cv2.imwrite("../maze.png", image)
