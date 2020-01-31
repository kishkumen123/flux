import pygame

from collections import OrderedDict
from flux.layer import layer
from flux.events import events
from flux.mouse import mouse
from flux.renderer import renderer


class Panel:

    def __init__(self, name, size=None, position=None, color=(128, 128, 128), debug=False, _layer="layer_0", show=False, padding=(15, 30), spacing=15):
        self.name = name

        self.size = size
        self.position = position
        self.debug = debug
        self.layer = _layer
        self.show = show
        self.rect = pygame.Rect(position, size)
        self.color = color
        self.components = OrderedDict()
        self.padding = (padding[0], padding[1])
        self.spacing = spacing

        self.movable = False
        self.calc_mouse_difference = False
        self.mouse_difference = 0
        if self.show:
            layer.set_layer("layer_3")

    def toggle(self):
        if self.show:
            self.show = False
            layer.pop_layer()
        else:
            self.show = True
            layer.set_layer("layer_3")

    def get_component_value(self, component_name):
        return self.components[component_name].get_value()

    def attach(self, component):
        self.components[component.name] = component

    def draw(self):
        if self.show:
            rect = renderer.draw_quad(self.position, self.size, self.color)
            renderer.draw_text(self.name, color=(50, 50, 50), rect=rect, clamp="midtop")
            for component in self.components.values():
                component.draw()

    def update(self):
        if events.button_pressed("MONE", "layer_3"):
            if mouse.get_rect().colliderect(self.rect):
                pass
                #self.movable = True
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

