import pygame
from .. import Screen

def pygame_screen_update(self):
    self.w, self.h = pygame.display.get_window_size()

screen_wrapper = Screen(update_method=pygame_screen_update)
