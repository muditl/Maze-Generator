from Grid import Grid
from maze_visuals import make_maze_visual, save_maze_png
from maze_generator import binary_algorithm, sidewinder, aldous_broder, wilson, hunt_and_kill
import cv2
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

top = cv2.imread("images/top.png")
bottom = cv2.imread("images/bottom.png")
right = cv2.imread("images/right.png")
left = cv2.imread("images/left.png")

grid = Grid(16, 16)
grid = hunt_and_kill(grid)
image = make_maze_visual(grid, top, bottom, right, left)
print(f"{Fore.GREEN}DONE MAKING MAZE!{Style.RESET_ALL}")
cv2.imshow("maze", image)
cv2.waitKeyEx(0)
cv2.destroyAllWindows()
save_maze_png(image)
