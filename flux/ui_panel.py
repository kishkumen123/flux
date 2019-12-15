import pygame

from screen import Display


class Panel:

    def __init__(self, name, size=None, position=None, color=(128, 128, 128), debug=False, layer="layer_0", show=False):
        self.name = name
        self.size = size
        self.position = position
        self.debug = debug
        self.layer = layer
        self.show = show
        self.rect = pygame.Rect(position, size)
        self.color = color
        self.components = []

    def attach(self, component):
        self.components.append(component)

    def draw(self):
        pygame.draw.rect(Display.fake_display, self.color, self.rect)
        for component in self.components:
            component.draw()

    def update(self):
        for component in self.components:
            component.update()

