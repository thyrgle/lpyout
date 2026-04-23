# Example file showing a basic pygame "game loop"
import pygame
from lpyout import Grid
from lpyout.pygame import screen_wrapper
from lpyout.pygame.render import render_recursive

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# Initialize grid:
screen_wrapper.update()
grid = Grid.fill_screen(screen_wrapper, 5, 5, m=30)

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
    render_recursive(grid, screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
