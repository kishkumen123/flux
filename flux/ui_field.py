import pygame
from screen import Display


class Field:

    def __init__(self, name, panel, size=None, _type=str()):
        self.name = name
        self.parent = panel.name
        self.size = size
        self._type = _type

        self.font = pygame.font.SysFont('Consolas', 20)
        self.surface_name = self.font.render(self.name, True, (50, 50, 50))
        self.surface_text = self.font.render(self.name, True, (50, 50, 50))

        self.spacing_x = 20
        self.name_position_x = panel.position[0] + panel.padding[0]
        self.background_position_x = self.name_position_x + self.surface_name.get_width() + self.spacing_x
        self.text_position_x = self.background_position_x

        if len(panel.components) == 0:
            self.world_position = [panel.position[0] + panel.padding[0], panel.position[1] + panel.padding[1]]
        else:
            self.world_position = [panel.position[0] + panel.padding[0], (panel.position[1] + panel.padding[1] + panel.components[-1].local_position[1] + panel.components[-1].size[1] + panel.spacing)]
        self.local_position = (self.world_position[0] - panel.position[0], self.world_position[1] - panel.position[1])

        self.rect = pygame.Rect(self.world_position, size)

    def draw(self):
        Display.fake_display.blit(self.surface_name, ((self.world_position[0] + (self.size[0] - self.surface_name.get_width())/2), (self.world_position[1] + (self.size[1] - self.surface_name.get_height())/2)))

    def update(self):
        pass
