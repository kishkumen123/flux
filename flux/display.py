import pygame
from pygame.locals import *


class Display:

    def __init__(self):
        self.x = 1024
        self.y = 720
        self.window = pygame.display.set_mode((self.x, self.y))

display = Display()
