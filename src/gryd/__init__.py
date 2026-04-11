from enum import Enum


class ScreenSize(Enum):
    """Based on TailwindCSS. See: 
    https://tailwindcss.com/docs/responsive-design"""
    SM = 640
    MD = 768
    LG = 1024
    XL = 1280
    XXL = 1536


class Screen:
    """Mostly for keeping track of the size of the screen."""
    def __init__(self, w=0, h=0):
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
                 anchor=Anchor.TOP_LEFT,
                 pl=0, pr=0, pt=0, pb=0,
                 ml=0, mr=0, mt=0, mb=0):
        # TODO: If anchor is not TOP_LEFT need to modify x, y.
        # Position.
        self.x = x
        self.y = y
        # Dimensions.
        self.w = w
        self.h = h
        # Padding.
        self.pl = pl
        self.pr = pr
        self.pt = pt
        self.pb = pb
        # Margins.
        self.ml = ml
        self.mr = mr
        self.mt = mt
        self.mb = mb
        # Cell info.
        self.row_count = row_count
        self.col_count = col_count

    @classmethod
    def grid_with_dim(cls, x, y, w, h, row_count, col_count,
                      anchor=Anchor.TOP_LEFT):
        """Given location and size, intialize a grid with the specified 
        number of rows and columns"""
        return cls(x, y, w, h, row_count, col_count)
    
    @classmethod
    def grid_with_cell_dim(cls, x, y, cell_w, cell_h, row_count, col_count,
                           anchor=Anchor.TOP_LEFT):
        """Given a location and *cell* size, initialize a grid with the
        specified number of rows and columns."""
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
        min_coord = (min_x, min_y)
        max_coord = (max_x, max_y)
        # TODO: Continue so it actually initializes.

    @classmethod
    def fill_screen(cls, screen, row_count, col_count):
        """Make the grid fill the specified screen."""
        return cls.grid_with_dim(0, 0, screen.w, screen.h, 
                                 row_count, col_count)
    
    # Padding utilities.

    def p(self, val):
        """Padding for the grid."""
        self.pl = val
        self.pr = val
        self.pt = val
        self.pb = val

    def px(self, val):
        """Padding-left-right for grid."""
        self.pl = val
        self.pr = val

    def pl(self):
        """Padding-left for the grid."""
        self.pl = val

    def pr(self):
        """Padding-right for the grid."""
        self.pr = val

    def py(self):
        """Padding-top-bottom for grid."""
        self.pt = val
        self.pb = val

    def pt(self):
        """Padding-top for the grid."""
        self.pt = val

    def pb(self):
        """Padding-bottom for the grid."""
        self.pb = val

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
