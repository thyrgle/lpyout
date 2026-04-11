from enum import Enum


class Screen:
    """Mostly for keeping track of the size of the screen."""
    def __init__(self, x=0, y=0, w=0, h=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


class Anchor(Enum):
    """Some common anchor points to operator from."""
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
    def __init__(self, x, y, w, h, row_count, col_count, 
                 anchor=Anchor.TOP_LEFT):
        # TODO: If anchor is not TOP_LEFT need to modify x, y.
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.row_count = row_count
        self.col_count = col_count

    @classmethod
    def grid_with_dim(cls, x, y, w, h, row_count, col_count,
                      anchor=Anchor.TOP_LEFT):
        return cls(x, y, w, h, row_count, col_count)
    
    @classmethod
    def grid_with_cell_dim(cls, x, y, cell_w, cell_h, row_count, col_count,
                           anchor=Anchor.TOP_LEFT):
        w = cell_w * row_count
        h = cell_h * col_count
        return cls(x, y, w, h, row_count, col_count)

    @classmethod
    def grid_from_cells(cls, x, y, row_count, col_count, width, height,
                        cells):
        """ Given a number of cells (possibly different spans). Organize 
        appropriately."""
        pass

    @classmethod
    def as_subgrid(cls, grid, at, to):
        """Make a grid that uses two indices of the parent grid to get a
        subgrid."""
        min_x, max_x = min(at[0], to[0]), max(at[0], to[0])
        min_y, max_y = min(at[1], to[1]), max(at[1], to[1])
        # TODO Finish
        pass

    @classmethod
    def fill_screen(cls, screen, row_count, col_count):
        """Make the grid fill the specified screen."""
        pass
    
    # Padding utilities.

    def p(self):
        """Padding for the grid."""
        pass

    def px(self):
        """Padding-left-right for grid."""

    def pl(self):
        """Padding-left for the grid."""
        pass

    def pr(self):
        """Padding-right for the grid."""
        pass

    def py(self):
        """Padding-top-bottom for grid."""
        pass

    def pt(self):
        """Padding-top for the grid."""
        pass

    def pb(self):
        """Padding-bottom for the grid."""
        pass

    # Max and min restrictions.

    def min_w(self):
        """Minimum-width for the grid."""
        pass

    def max_w(self):
        """Maximum-width for the grid."""
        pass

    def min_h(self):
        """Minimum-height for the grid."""
        pass

    def max_h(self):
        """Maximum-height for the grid."""
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

    def make_with_cell_size(cell_width, cell_height):
        pass


class HBox(Grid):
    """A nx1 grid"""
    def __init__(self, x, y, w, h, n):
        super().__init__(x, y, w, h, n, 1)
