import pygame
from screen import Display


class Button:

    def __init__(self, name, parent, world_position, size=None, position=None, color=(128, 0, 128)):
        self.name = name
        self.parent = parent
        self.size = size
        self.world_position = world_position
        self.relative_position = position
        self.local_position = [a + self.relative_position[i] for i, a in enumerate(self.world_position)]
        self.color = color
        self.rect = pygame.Rect(self.local_position, size)

    def draw(self):
        pygame.draw.rect(Display.fake_display, self.color, self.rect)

    def update(self):
        pass
