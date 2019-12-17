import pygame

from screen import Display
from mouse import mouse
from events import events


class Button:

    def __init__(self, name, panel, size=None, color=(128, 0, 128)):
        self.name = name
        self.parent = panel.name
        self.size = size
        if len(panel.components) == 0:
            self.world_position = [panel.position[0] + panel.padding[0], panel.position[1] + panel.padding[1]]
        else:
            panel_components = list(panel.components.items())
            self.world_position = [panel.position[0] + panel.padding[0], (panel.position[1] + panel.padding[1] + panel_components[-1][1].local_position[1] + panel_components[-1][1].size[1] + panel.spacing)]
        self.local_position = (self.world_position[0] - panel.position[0], self.world_position[1] - panel.position[1])
        self.color = color
        self.rect = pygame.Rect(self.world_position, size)
        self.font = pygame.font.SysFont('Consolas', 22)
        self.surface_name = self.font.render(self.name, True, (50, 50, 50))
        self.pressed = False

    def get_value(self):
        return self.pressed

    def draw(self):
        pygame.draw.rect(Display.fake_display, self.color, self.rect)
        Display.fake_display.blit(self.surface_name, ((self.world_position[0] + (self.size[0] - self.surface_name.get_width())/2), (self.world_position[1] + (self.size[1] - self.surface_name.get_height())/2)))

    def update(self):
        self.pressed = False
        if mouse.get_rect().colliderect(self.rect):
            if events.button_pressed("MONE", "layer_0"):
                pass
            if events.button_released("MONE", "layer_0"):
                self.pressed = True


