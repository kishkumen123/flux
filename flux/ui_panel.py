import pygame

from screen import Display


class Panel:

    def __init__(self, name, size=None, position=None, color=(128, 128, 128), debug=False, layer="layer_0", show=True, padding=(15, 15), spacing=15):
        self.name = name
        self.size = size
        self.position = position
        self.debug = debug
        self.layer = layer
        self.show = show
        self.rect = pygame.Rect(position, size)
        self.color = color
        self.components = []
        self.padding = padding
        self.spacing = spacing

    def attach(self, component):
        self.components.append(component)

    def draw(self):
        pygame.draw.rect(Display.fake_display, self.color, self.rect)
        for i, component in enumerate(self.components):
            component.draw()

    def update(self):
        #if mouse down and contains mouse - move me
        for component in self.components:
            component.update()

