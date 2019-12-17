import pygame

from screen import Display
from collections import OrderedDict


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

    def get_value(self, component_name):
        return self.components[component_name].get_value()

    def attach(self, component):
        self.components[component.name] = component

    def draw(self):
        pygame.draw.rect(Display.fake_display, self.color, self.rect)
        for component in self.components.values():
            component.draw()

    def update(self):
        # TODO: if mouse down and contains mouse - move me
        for component in self.components.values():
            component.update()

