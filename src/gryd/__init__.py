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
    def __init__(self, x, y, w, h, row_count, col_count, parent=None, 
                 anchor=Anchor.TOP_LEFT,
                 p=None,
                 px=None, py=None,
                 pl=None, pr=None, pt=None, pb=None,
                 m=None,
                 mx=None, my=None,
                 ml=None, mr=None, mt=None, mb=None,
                 spacing=None):
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
        # Padding. The assignment is done this way because the "fundamental"
        # values (pl, pr, pt, pb) should always have a number. So they
        # *cannot* be None and default to 0. But, is p, px, or py is assigned
        # and they are not, we want them to default to the p, px, or py
        # value. Furthermore, if both p, px, or py is assigned and the value
        # is overriden then we want to use the overriden value.
        self.pl = pl or px or p or 0
        self.pr = pr or px or p or 0
        self.pt = pt or py or p or 0
        self.pb = pb or py or p or 0
        # Margins. The assignment is done this way because the "fundamental"
        # values (ml, mr, mt, mb) should always have a number. So they
        # *cannot* be None and default to 0. But, is m, mx, or my is assigned
        # and they are not, we want them to default to the m, mx, or my
        # value. Furthermore, if both m, mx, or my is assigned and the value
        # is overriden then we want to use the overriden value.
        self.ml = ml or mx or m or 0
        self.mr = mr or mx or m or 0
        self.mt = mt or my or m or 0
        self.mb = mb or my or m or 0
        # Cell info.
        self.row_count = row_count
        self.col_count = col_count
        # Cells
        self.children = []

    def __getitem__(self, index):
        return self.children[index]

    def __next__(self):
        for row in range(self.children):
            for child in range(row):
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
        cell_w = (grid.w - (grid.pl + grid.pr)) / grid.col_count
        cell_h = (grid.h - (grid.pt + grid.pb)) / grid.row_count
        # Fill the children with uniform sized cells.
        x_offset = grid.x + grid.pl
        y_offset = grid.y + grid.pt
        for i in range(grid.row_count):
            grid.children.append([])
            for j in range(grid.col_count):
                grid.children[i].append(
                    Cell(x_offset + j * cell_w,
                         y_offset + i * cell_h, cell_w, cell_h,
                         parent=grid)
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
                    ml=None, mr=None, mt=None, mb=None):
        """Make the grid fill the specified screen."""
        return cls.grid_with_dim(0, 0, screen.w, screen.h, 
                                 row_count, col_count,
                                 p=p,
                                 px=px, py=py,
                                 pl=pl, pr=pr, pt=pt, pb=pb,
                                 m=m,
                                 mx=mx, my=my,
                                 ml=ml, mr=mr, mt=mt, mb=mb)


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
        return (self._pl, self._pr, self._pt, self._pb)
    
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

    def realize(self, anchor=Anchor.CENTER):
        """For a given grid, return the coordinates of that grid. Notice that
        this by default returns the center of the grid, but by specifying the
        `anchor` you may change this to any percentage for width and height
        of the cell."""
        return (self.x + anchor[0] * self.w, self.y + anchor[1] * self.h)


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
                 parent=None):
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self.parent = parent
        # Padding. The assignment is done this way because the "fundamental"
        # values (pl, pr, pt, pb) should always have a number. So they
        # *cannot* be None and default to 0. But, is p, px, or py is assigned
        # and they are not, we want them to default to the p, px, or py
        # value. Furthermore, if both p, px, or py is assigned and the value
        # is overriden then we want to use the overriden value.
        self.pl = p
        self.pr = p
        self.pt = p
        self.pb = p
        self.pl = px if px is not None else self.pl
        self.pr = px if px is not None else self.pr
        self.pt = py if py is not None else self.pt
        self.pb = py if py is not None else self.pb
        self.pl = pl if pl is not None else self.pl
        self.pr = pr if pr is not None else self.pr
        self.pt = pt if pt is not None else self.pt
        self.pb = pb if pb is not None else self.pb
        self.pl = 0 if self.pl is None else self.pl
        self.pr = 0 if self.pr is None else self.pr
        self.pt = 0 if self.pt is None else self.pt
        self.pb = 0 if self.pb is None else self.pb
        # Margins. The assignment is done this way because the "fundamental"
        # values (ml, mr, mt, mb) should always have a number. So they
        # *cannot* be None and default to 0. But, is m, mx, or my is assigned
        # and they are not, we want them to default to the m, mx, or my
        # value. Furthermore, if both m, mx, or my is assigned and the value
        # is overriden then we want to use the overriden value.
        self.ml = m
        self.mr = m
        self.mt = m
        self.mb = m
        self.ml = mx if mx is not None else self.ml
        self.mr = mx if mx is not None else self.mr
        self.mt = my if my is not None else self.mt
        self.mb = my if my is not None else self.mb
        self.ml = ml if ml is not None else self.ml
        self.mr = mr if mr is not None else self.mr
        self.mt = mt if mt is not None else self.mt
        self.mb = mb if mb is not None else self.mb
        self.ml = 0 if self.ml is None else self.ml
        self.mr = 0 if self.mr is None else self.mr
        self.mt = 0 if self.mt is None else self.mt
        self.mb = 0 if self.mb is None else self.mb


class VBox(Grid):
    """A 1xn grid"""
    def __init__(self, x, y, w, h, n):
        super().__init__(x, y, w, h, 1, n)

    def make_with_cell_size(cls, cell_width, cell_height):
        pass


class HBox(Grid):
    """A nx1 grid"""
    def __init__(self, x, y, w, h, n):
        super().__init__(x, y, w, h, n, 1)
