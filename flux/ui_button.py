import pygame

from flux._globals import add_rect
from flux.mouse import mouse
from flux.events import events
from flux.renderer import renderer
from flux.screen import Display


class Button:

    def __init__(self, name, panel, size=None, color=(128, 0, 128)):
        self.name = name
        self.parent = panel.name
        self.size = size
        self.color = color

        self.panel_position = panel.position
        self.panel_padding = panel.padding
        self.panel_components = list(panel.components.items())
        self.panel_spacing = panel.spacing

        if len(self.panel_components) == 0:
            self.world_position = [self.panel_position[0] + self.panel_padding[0], self.panel_position[1] + self.panel_padding[1]]
        else:
            self.world_position = [self.panel_position[0] + self.panel_padding[0], (self.panel_position[1] + self.panel_padding[1] + self.panel_components[-1][1].local_position[1] + self.panel_components[-1][1].size[1] + self.panel_spacing)]

        self.local_position = (self.world_position[0] - self.panel_position[0], self.world_position[1] - self.panel_position[1])
        add_rect(pygame.Rect(self.world_position, self.size), self.color, 50)

        self.rect = pygame.Rect(self.world_position, self.size)

        self.pressed = False
        self.held = False

    def get_value(self):
        return self.pressed

    def draw(self):
        self.rect = renderer.draw_quad(self.world_position, self.size, self.color)
        renderer.draw_text(self.name, color=(50, 50, 50), rect=self.rect, clamp="center")

    def update_ui_positions(self, panel_position):
        self.panel_position = panel_position

        if len(self.panel_components) == 0:
            self.world_position = [self.panel_position[0] + self.panel_padding[0], self.panel_position[1] + self.panel_padding[1]]
        else:
            self.world_position = [self.panel_position[0] + self.panel_padding[0], (self.panel_position[1] + self.panel_padding[1] + self.panel_components[-1][1].local_position[1] + self.panel_components[-1][1].size[1] + self.panel_spacing)]
        self.local_position = (self.world_position[0] - self.panel_position[0], self.world_position[1] - self.panel_position[1])

        self.rect = pygame.Rect(self.world_position, self.size)

    def update(self, panel_position):
        self.update_ui_positions(panel_position)

        self.pressed = False
        if mouse.get_rect().colliderect(self.rect):
            if events.button_pressed_once("MONE", "layer_3"):
                self.held = True
            if events.button_released("MONE", "layer_3") and self.held:
                self.pressed = True
                self.held = False
        else:
            self.held = False
