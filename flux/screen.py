import pygame
from pygame.locals import *


class Display:
    x = 0
    y = 0
    display = pygame.display.set_mode((0, 0))
    fake_display = display.copy()

    @classmethod
    def init(cls, resolution):
        cls.x = resolution[0]
        cls.y = resolution[1]
        cls.display = pygame.display.set_mode((resolution[0], resolution[1]))
        cls.fake_display = cls.display.copy()

    @classmethod
    def resize(cls, size):
        cls.x = size[0]
        cls.y = size[1]
        cls.display = pygame.display.set_mode(size)

    @classmethod
    def load_to_buffer(cls, surface, x=0, y=0):
        cls.fake_display.blit(surface, (x, y))

    @classmethod
    def clear_screen(cls, _color=None):
        if _color:
            cls.fake_display.fill(color)
        else:
            cls.fake_display.fill((0, 0, 0))

    @classmethod
    def set_caption(cls, name):
        pygame.display.set_caption(name)

    @classmethod
    def swap_buffer(cls):
        #pygame.display.update()
        cls.display.blit(pygame.transform.scale(cls.fake_display, (cls.x, cls.y)), (0, 0))
        pygame.display.flip()
