import pygame
from ... import Grid, Cell


def fast_render(grid: Grid, surface, color=(255, 255, 255), w=1):
    """Renders with lines instead of squares, ignores style."""
    # Render rows.
    for i in range(grid.row_count + 1):
        cell_h = grid.h / grid.row_count
        start_pos = (grid.x, i * cell_h)
        end_pos = (grid.x + grid.w, i * cell_h)
        pygame.draw.line(surface, color, start_pos, end_pos, width=w)
    
    # Render cols.
    for i in range(grid.col_count + 1):
        cell_w = grid.w / grid.col_count
        start_pos = (i * cell_w, grid.y)
        end_pos = (i * cell_w, grid.y + grid.h)
        pygame.draw.line(surface, (255, 255, 255), start_pos, end_pos)

def line_render(grid: Grid, surface):
    """Render with lines and uses applicable styles."""
    pass

def render_recursive(grid: Grid, surface, color=(255,255,255)):
    """Render with style."""
    if isinstance(grid, Cell):
        rect = pygame.Rect(grid.x, grid.y, grid.w, grid.h)
        pygame.draw.rect(surface, color, rect)
    else:
        for subgrid in grid:
            render_recursive(subgrid)
