import pygame
from collections import OrderedDict

from flux.events import events
from flux.mouse import mouse
from flux.screen import Display


class Panel:

    def __init__(self, name, size=None, position=None, color=(128, 128, 128), debug=False, layer="layer_0", show=False, padding=(15, 15), spacing=15):
        self.name = name
        self.size = size
        self.position = position
        self.debug = debug
        self.layer = layer
        self.show = show
        self.rect = pygame.Rect(position, size)
        self.color = color
        self.components = OrderedDict()
        self.padding = padding
        self.spacing = spacing

        self.movable = False
        self.calc_mouse_difference = False
        self.mouse_difference = 0

    def get_component_value(self, component_name):
        return self.components[component_name].get_value()

    def attach(self, component):
        self.components[component.name] = component

    def draw(self):
        pygame.draw.rect(Display.fake_display, self.color, self.rect)
        for component in self.components.values():
            component.draw()

    def update(self):
        if events.button_pressed("MONE", "layer_0"):
            if mouse.get_rect().colliderect(self.rect):
                self.movable = True
        else:
            self.movable = False
            self.calc_mouse_difference = False

        if self.movable:
            if not self.calc_mouse_difference:
                self.mouse_difference = (self.position[0] - mouse.get_pos()[0], self.position[1] - mouse.get_pos()[1])
                self.calc_mouse_difference = True
            self.position = (mouse.get_pos()[0] + self.mouse_difference[0], mouse.get_pos()[1] + self.mouse_difference[1])
            self.rect = pygame.Rect(self.position, self.size)

        for component in self.components.values():
            component.update(self.position)

