from __future__ import annotations
from enum import Enum
from itertools import pairwise
import types


def raw_coords(v1: Screen | Grid, v2: Screen | Grid):
    """Compute the relative coords of one viewport in the other. Raw refers
    to being raw pixels."""
    return (v1.x - v2.x, v1.y - v2.y)

def frac_coords(v1: Screen | Grid, v2: Screen | Grid):
    """Compute the fractional (percentage) coords of one viewport in the other.
    """
    raw_x = v1.x - v2.x
    raw_y = v1.y - v2.y
    return (raw_x / v2.w, raw_y / v2.h)


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

    def __init__(self, x=0, y=0, w=0, h=0, update_method=lambda w, h: None):
        self.x = x
        self.y = y
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


class Grid:
    def __init__(self, x, y, w, h, row_count, col_count, parent=None, 
                 anchor=Anchor.TOP_LEFT,
                 p=None,
                 px=None, py=None,
                 pl=None, pr=None, pt=None, pb=None,
                 m=None,
                 mx=None, my=None,
                 ml=None, mr=None, mt=None, mb=None,
                 value=None,
                 rspan=1, cspan=1,
                 spacing=0,
                 index=(0,0)):
        """The constructor, should be noted: No children are added here, more
        than likely, you want to use one of the classmethods to construct a
        grid."""
        # TODO: If anchor is not TOP_LEFT need to modify x, y.
        # Position.
        self._x = x
        self._y = y
        # Dimensions.
        self._w = w
        self._h = h
        # The parent grid this belongs to (if applicable, otherwise None).
        self.parent = parent
        # Padding. Priority is p(l,r,t,b) then p(x,y) then p.
        self.pl = pl or px or p or 0
        self.pr = pr or px or p or 0
        self.pt = pt or py or p or 0
        self.pb = pb or py or p or 0
        # Margins. Priority is m(l,r,t,b) then m(x,y) then m.
        self.ml = ml or mx or m or 0
        self.mr = mr or mx or m or 0
        self.mt = mt or my or m or 0
        self.mb = mb or my or m or 0
        # Index (the array location, not real world coords)
        self.index = index
        # Cell info.
        self.row_count = row_count
        self.col_count = col_count
        # Span in parent grid.
        self._rspan = rspan
        self._cspan = cspan
        # Child Grids (likely cells, but could be another grid.)
        self.children = []

    def __getitem__(self, index):
        return self.children[index]

    def __iter__(self):
        for row in self.children:
            for child in row:
                yield child

    @classmethod
    def grid_with_dim(cls, x, y, w, h,
                      row_count, col_count,
                      p=None,
                      px=None, py=None,
                      pl=None, pr=None, pt=None, pb=None,
                      m=None,
                      mx=None, my=None,
                      ml=None, mr=None, mt=None, mb=None,
                      spacing=0,
                      anchor=Anchor.TOP_LEFT):
        """Given location and size, intialize a grid with the specified 
        number of rows and columns"""
        grid = cls(x, y, w, h, row_count, col_count,
                   p=p,
                   px=px, py=py,
                   pl=pl, pr=pr, pt=pt, pb=pb,
                   m=m,
                   mx=mx, my=my,
                   ml=ml, mr=mr, mt=mt, mb=mb,
                   spacing=spacing,
                   anchor=anchor)
        cell_w = (grid.w - (grid.pl + grid.pr)) / grid.col_count - spacing
        cell_h = (grid.h - (grid.pt + grid.pb)) / grid.row_count - spacing
        # Fill the children with uniform sized cells.
        x_offset = grid.x + grid.pl + spacing / 2
        y_offset = grid.y + grid.pt + spacing / 2
        for i in range(grid.row_count):
            grid.children.append([])
            for j in range(grid.col_count):
                grid.children[i].append(
                    Cell(x_offset + j * (cell_w + spacing),
                         y_offset + i * (cell_h + spacing),
                         cell_w, cell_h,
                         parent=grid,
                         index=(i, j))
                )
        return grid
 
    @classmethod
    def grid_with_cell_dim(cls, x, y, cell_w, cell_h, row_count, col_count,
                           p=None,
                           px=None, py=None,
                           pl=None, pr=None, pt=None, pb=None,
                           m=None,
                           mx=None, my=None,
                           ml=None, mr=None, mt=None, mb=None,
                           spacing=0,
                           anchor=Anchor.TOP_LEFT):
        """Given a location and *cell* size, initialize a grid with the
        specified number of rows and columns."""
        w = cell_w * row_count
        h = cell_h * col_count
        return cls.grid_with_dim(x, y, w, h, row_count, col_count,
                                 p=p, 
                                 px=px, py=py,
                                 pl=pl, pr=pr, pt=pt, pb=pb,
                                 m=m,
                                 mx=mx, my=my,
                                 ml=ml, mr=mr, mt=mt, mb=mb,
                                 spacing=spacing)

    @classmethod
    def fill_screen(cls, screen, row_count, col_count,
                    p=None,
                    px=None, py=None,
                    pl=None, pr=None, pt=None, pb=None,
                    m=None,
                    mx=None, my=None,
                    ml=None, mr=None, mt=None, mb=None,
                    spacing=0):
        """Make the grid fill the specified screen."""
        return cls.grid_with_dim(0, 0, screen.w, screen.h, 
                                 row_count, col_count,
                                 p=p,
                                 px=px, py=py,
                                 pl=pl, pr=pr, pt=pt, pb=pb,
                                 m=m,
                                 mx=mx, my=my,
                                 ml=ml, mr=mr, mt=mt, mb=mb,
                                 spacing=spacing)


    @property
    def x(self):
        """self.x (but remember it is influenced by margin!)"""
        return self._x + self.ml

    @x.setter
    def x(self, val):
        self._x = val

    @property
    def y(self):
        """self.y (but remember it is influenced by margin!)"""
        return self._y + self.mt

    @y.setter
    def y(self, val):
        self._y = val

    @property
    def w(self):
        return self._w - (self.mr + self.ml)

    @w.setter
    def w(self, val):
        self._w = val

    @property
    def h(self):
        return self._h - (self.mb + self.mt)

    @h.setter
    def h(self, val):
        self._h = val
    
    # Padding utilities.

    @property
    def p(self):
        """Padding for the grid."""
        return (self.pl, self.pr, self.pt, self.pb)
    
    @p.setter
    def p(self, val):
        self.pl = val
        self.pr = val
        self.pt = val
        self.pb = val

    @property
    def px(self):
        """Padding-left-right for grid."""
        return (self.pl, self.pr)
    
    @px.setter
    def px(self, val):
        self.pl = val
        self.pr = val

    @property
    def py(self):
        """Padding-top-bottom for grid."""
        return (self.pt, self.pb)
    
    @py.setter
    def py(self, val):
        self.pt = val
        self.pb = val

    def realize(self, anchor=Anchor.CENTER):
        """For a given grid, return the coordinates of that grid. Notice that
        this by default returns the center of the grid, but by specifying the
        `anchor` you may change this to any percentage for width and height
        of the cell."""
        return (self.x + anchor[0] * self.w, self.y + anchor[1] * self.h)

    @property
    def rpsan(self):
        return self._rspan

    @rpsan.setter
    def rspan(self, val):
        self.w += (val - (self._rspan - 1)) * self.w
        # TODO: Change parent's children!
        self._rspan = val

    @property
    def cspan(self):
        return self._cspan

    @cspan.setter
    def cspan(self, val):
        self.h = (val - (self._cspan - 1)) * self.h
        # TODO: Change parent's children!
        self._rspan = val


class Cell(Grid):
    """A 1x1 grid"""
    def __init__(self, x, y, w, h,
                 p=None,
                 px=None, py=None,
                 pl=None, pr=None, pt=None, pb=None,
                 m=None,
                 mx=None, my=None,
                 ml=None, mr=None, mt=None, mb=None,
                 rspan=1, cspan=1,
                 value=None,
                 parent=None,
                 index=(0,0)):
        super().__init__(x, y, w, h,
                         p=p,
                         px=px, py=py,
                         pl=pl, pr=pr, pt=pt, pb=pb,
                         m=m,
                         mx=mx, my=my,
                         ml=ml, mr=mr, mt=mt, mb=mb,
                         row_count=1, col_count=1, # Def of a cell.
                         rspan=rspan, cspan=cspan,
                         value=value,
                         parent=parent,
                         index=index)

class VBox(Grid):
    """A 1xn grid"""
    @classmethod
    def divide_screen(cls, screen, n, heights=None):
        """Divide the screen into n equidistant cells row-wise."""
        # TODO Allow custom heights.
        return super(VBox, cls).fill_screen(screen, n, 1)


class HBox(Grid):
    """A nx1 grid"""
    @classmethod
    def divide_screen(cls, screen, n, widths=None):
        """Divide the screen into n equidistant cells column-wise."""
        # TODO: Allow custom widths.
        return super(HBox, cls).fill_screen(screen, 1, n)
