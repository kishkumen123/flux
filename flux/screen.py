import pygame
from pygame.locals import *


class Display:

    def __init__(self, resolution=None):
        self.x = resolution[0]
        self.y = resolution[1]
        self.display = pygame.display.set_mode((resolution[0], resolution[1]), RESIZABLE|DOUBLEBUF|HWSURFACE)
        self.fake_display = self.display.copy()

    def resize(self, size):
        self.display = pygame.display.set_mode(size, HWSURFACE|DOUBLEBUF|RESIZABLE)
        self.display.blit(pygame.transform.scale(self.fake_display, size), (0, 0))

    def load_to_buffer(self, surface, x=0, y=0):
        self.fake_display.blit(surface, (x, y))

    def clear_screen(self, _color=None):
        if _color:
            self.fake_display.fill(color)
        else:
            self.fake_display.fill((0, 0, 0))

    def set_caption(self, name):
        pygame.display.set_caption(name)

    def swap_buffer(self):
        #pygame.display.update()
        pygame.display.flip()

