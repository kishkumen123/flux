import pygame
from screen import Display


class Button:

    def __init__(self, name, panel, size=None, position=None, color=(128, 0, 128)):
        self.name = name
        self.parent = panel.name
        self.size = size
        self.world_position = panel.position
        self.relative_position = position
        self.local_position = [a + self.relative_position[i] for i, a in enumerate(self.world_position)]
        self.color = color
        self.rect = pygame.Rect(self.local_position, size)
        self.font = pygame.font.SysFont('Consolas', 22)
        self.name_surface = self.font.render(self.name, True, (50, 50, 50))

    def draw(self):
        pygame.draw.rect(Display.fake_display, self.color, self.rect)
        Display.fake_display.blit(self.name_surface, ((self.local_position[0] + (self.size[0] - self.name_surface.get_width())/2), (self.local_position[1] + (self.size[1] - self.name_surface.get_height())/2)))

    def update(self):
        pass
