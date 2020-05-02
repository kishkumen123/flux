import pygame
import random


class Terrain:
    def __init__(self, chunk_size, xcoord, ycoord, seed):
        self.seed = seed
        self.chunk_size = chunk_size
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.xposition = xcoord * chunk_size
        self.yposition = ycoord * chunk_size
        self.rect = pygame.Rect(self.xposition, self.yposition, chunk_size, chunk_size)
        self.color = (random.randint(50, 254), 0, 0)
        self.surface = pygame.Surface((chunk_size, chunk_size))

    def set_surface(self, surface):
        self.surface = surface

    def update(self, offsets=(0, 0)):
        self.rect = pygame.Rect(self.xposition + offsets[0], self.yposition + offsets[1], self.chunk_size, self.chunk_size)
