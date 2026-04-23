# Example file showing a basic pygame "game loop"
import pygame
from lpyout import Grid
from lpyout.pygame import screen_wrapper

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# Initialize grid:
screen_wrapper.update()
grid = Grid.fill_square(screen_wrapper, 8, 8, p=20)

def chess_render(grid: Grid, surface):
    for cell in grid:
        if sum(cell.index) % 2 == 1:
            rect = pygame.Rect(cell.x, cell.y, cell.w, cell.h)
            pygame.draw.rect(surface, (255, 255, 255), rect, 0)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    
    # Render grid
    screen_wrapper.update()
    chess_render(grid, screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
