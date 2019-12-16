import pygame
from screen import Display


class Button:

    def __init__(self, name, panel, size=None, color=(128, 0, 128)):
        self.name = name
        self.parent = panel.name
        self.size = size
        if len(panel.components) == 0:
            #self.world_position = [panel.position[0] + panel.padding[0], (panel.position[1] + panel.padding[1] + (len(panel.components)) * (panel.spacing + self.size[1]))]
            self.world_position = [panel.position[0] + panel.padding[0], panel.position[1] + panel.padding[1]]
        else:
            #self.world_position = [panel.position[0] + panel.padding[0], (panel.position[1] + panel.padding[1] + (len(panel.components)) * (panel.spacing + panel.components[-1].size[1]))]
            #self.world_position = [panel.position[0] + panel.padding[0], (panel.position[1] + panel.components[-1].world_position[1] + panel.components[-1].size[1] + panel.spacing)]
            self.world_position = [panel.position[0] + panel.padding[0], (panel.position[1] + panel.padding[1] + panel.components[-1].local_position[1] + panel.components[-1].size[1] + panel.spacing)]
        self.local_position = (self.world_position[0] - panel.position[0], self.world_position[1] - panel.position[1])
        self.color = color
        self.rect = pygame.Rect(self.world_position, size)
        self.font = pygame.font.SysFont('Consolas', 22)
        self.name_surface = self.font.render(self.name, True, (50, 50, 50))

    def draw(self):
        pygame.draw.rect(Display.fake_display, self.color, self.rect)
        Display.fake_display.blit(self.name_surface, ((self.world_position[0] + (self.size[0] - self.name_surface.get_width())/2), (self.world_position[1] + (self.size[1] - self.name_surface.get_height())/2)))

    def update(self):
        pass
