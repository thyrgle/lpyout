from enum import Enum


class Anchor(Enum):
    TOP_LEFT = (0, 0)
    TOP_CENTER = (1/2, 0)
    TOP_RIGHT = (1, 0)
    CENTER_LEFT = (0, 1/2)
    CENTER = (1/2, 1/2)
    CENTER_RIGHT = (1, 1/2)
    BOTTOM_LEFT = (0, 1)
    BOTTOM_CENTER = (1/2, 1)
    BOTTOM_RIGHT = (1, 1)


class Grid:
    def __init__(self, x, y, w, h, row_count, col_count):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.row_count = row_count
        self.col_count = col_count

    @classmethod
    def grid_with_dim(cls, x, y, w, h, row_count, col_count):
        return cls(x, y, w, h, row_count, col_count)
    
    @classmethod
    def grid_with_cell_dim(cls, x, y, cell_w, cell_h, row_count, col_count):
        w = cell_w * row_count
        h = cell_h * col_count
        return cls(x, y, w, h, row_count, col_count)

    @classmethod
    def as_subgrid(cls, grid, at, to):
        pass 

    def realize(self, anchor=Anchor.CENTER):
        """For a given grid, return the coordinates of that grid. Notice that
        this by default returns the center of the grid, but by specifying the
        `anchor` you may change this to any percentage for width and height
        of the cell."""
        return (self.x + anchor[0] * self.w, self.y + anchor[1] * self.h)


class Cell(Grid):
    """A 1x1 grid"""
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, 1, 1)


class VBox(Grid):
    """A 1xn grid"""
    def __init__(self, x, y, w, h, n):
        super().__init__(x, y, w, h, 1, n)


class HBox(Grid):
    """A nx1 grid"""
    def __init__(self, x, y, w, h, n):
        super().__init__(x, y, w, h, n, 1)
