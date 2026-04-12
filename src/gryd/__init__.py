from enum import Enum
from itertools import pairwise
import types


class ScreenSize(Enum):
    """Based on TailwindCSS. See: 
    https://tailwindcss.com/docs/responsive-design"""
    XS = 0
    SM = 640
    MD = 768
    LG = 1024
    XL = 1280
    XXL = 1536
    XXXL = 1537


class Screen:
    """Mostly for keeping track of the size of the screen and making media
    queries"""
    @property
    def query(self) -> ScreenSize:
        """Based on https://tailwindcss.com/docs/responsive-design"""
        for q1, q2 in pairwise(ScreenSize):
            if self.w < q2:
                return q1
        return ScreenSize.XXXL
            

    def __init__(self, w=0, h=0, update_method=lambda w, h: None):
        self.w = w
        self.h = h
        # If the screen changes size potentially, need to get the values
        # for the updated screen. Many prebuilts for screens are provided
        # in optional submodules.
        self.update = types.MethodType(update_method, self)


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


class QueryGrid:
    """Grid that adapats to media queries from a screen."""
    pass


class Grid:
    def __init__(self, x, y, w, h, row_count, col_count, 
                 anchor=Anchor.TOP_LEFT,
                 p=0,
                 px=0, py=0,
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
        self.p = p
        self.px = px
        self.py = py
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
        # Cells
        cell_w = self.w / self.col_count
        cell_h = self.h / self.row_count
        self.children = []
        for i in range(self.row_count):
            self.children.append([])
            for j in range(self.col_count):
                self.children[i].append(
                    Cell(j * cell_w, i * cell_h, cell_w, cell_h)
                )

    def __getitem__(self, index):
        return self.children[index]

    def __next__(self):
        for i in range(self.row_count):
            for j in range(self.col_count):
                yield self[i][j]

    def _propegate_changes(self):
        pass

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
                        cells,
                        anchor=Anchor.TOP_LEFT):
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

    @property
    def p(self):
        """Padding for the grid."""
        return (self.pl, self.pr, self.pt, self.pb)
    
    @p.setter
    def p(self, val):
        self._pl = val
        self._pr = val
        self._pt = val
        self._pb = val

    @property
    def px(self):
        """Padding-left-right for grid."""
        return (self._pl, self._pr)
    
    @px.setter
    def px(self, val):
        self._pl = val
        self._pr = val

    @property
    def pl(self):
        """Padding-left for the grid."""
        return self._pl

    @pl.setter
    def pl(self, val):
        self._pl = val

    @property
    def pr(self):
        """Padding-right for the grid."""
        return self._pr

    @pr.setter
    def pr(self, val):
        self._pr = val
    
    @property
    def py(self):
        """Padding-top-bottom for grid."""
        return (self._pt, self._pb)
    
    @py.setter
    def py(self, val):
        self._pt = val
        self._pb = val

    @property
    def pt(self):
        """Padding-top for the grid."""
        return self._pt
    
    @pt.setter
    def pt(self, val):
        self._pt = val
    
    @property
    def pb(self):
        """Padding-bottom for the grid."""
        return self._pb

    @pb.setter
    def pb(self, val):
        self._pb = val

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
        self.x = x
        self.y = y
        self.w = w
        self.h = h


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
