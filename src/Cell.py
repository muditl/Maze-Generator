from colorama import Fore, Style


class Cell:

    def __init__(self, row, column):
        if row < 0 or column < 0:
            raise Exception("Given row or column invalid: " + str((row, column)))
        self.position = (row, column)
        self.north = None
        self.south = None
        self.east = None
        self.west = None
        self.links = []
        self.marker = 0

    # link cell to given cell
    def link(self, cell):
        if self.get_neighbors().__contains__(cell):
            if not self.links.__contains__(cell):
                self.links.append(cell)
            if not cell.links.__contains__(self):
                cell.links.append(self)
        else:
            print(f"{Fore.YELLOW}Internal Warning: Cell is not a neighbor, could not link!{Style.RESET_ALL}")

    # unlink cell to given cell
    def unlink(self, cell):
        if self.links.__contains__(cell):
            self.links.remove(cell)
        if cell.links.__contains__(self):
            cell.links.remove(self)

    # check if cell is linked to given cell
    def check_link(self, cell):
        return self.links.__contains__(cell) and cell.links.__contains__(self)

    # check if cells are not linked together (for testing purposes)
    def check_unlink(self, cell):
        return not (self.links.__contains__(cell) or cell.links.__contains__(self))

    def get_neighbors(self):
        neighbors = []
        if self.north is not None:
            neighbors.append(self.north)
        if self.south is not None:
            neighbors.append(self.south)
        if self.east is not None:
            neighbors.append(self.east)
        if self.west is not None:
            neighbors.append(self.west)
        return neighbors

    def get_unlinked_neighbors(self):
        neighbors = self.get_neighbors()
        unl = []
        for cell in neighbors:
            if self.check_unlink(cell):
                unl.append(cell)
        return unl

    def get_linked_neighbors(self):
        neighbors = self.get_neighbors()
        lin = []
        for cell in neighbors:
            if self.check_link(cell):
                lin.append(cell)
        return lin

    def get_closed_neighbors(self):
        neighbors = self.get_neighbors()
        closed = []
        for cell in neighbors:
            if len(cell.links) == 0:
                closed.append(cell)
        return closed

    def mark(self, mark):
        self.marker = mark

    def unmark(self):
        self.marker = 0

    def get_position(self):
        return self.position

    # gives a code for what the cell should look like graphically
    # binary number where each digit represents each direction
    # 1000: north, 100: south, 10: east, 1: west
    # e.g. 1010 -> north and east are open, south and west are closed
    def calculate_image_code(self):
        image = 0b0000
        for _l in self.links:
            if self.north == _l:
                image += 0b1000
            if self.south == _l:
                image += 0b100
            if self.east == _l:
                image += 0b10
            if self.west == _l:
                image += 0b1
        return image

    # simple string representation of cell
    def __str__(self):
        return str(self.position)

    # detailed string representation of cell
    def verbose__str__(self):
        res = "Cell(" + str(self.position) + ")"
        res += ", north:"
        res += str(self.north.position) if self.north is not None else "None"
        res += ", south:"
        res += str(self.south.position) if self.south is not None else "None"
        res += ", east:"
        res += str(self.east.position) if self.east is not None else "None"
        res += ", west:"
        res += str(self.west.position) if self.west is not None else "None"
        return res
