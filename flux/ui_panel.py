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
        self.buttons = []
        #this guy later
        self.components = []

    def attach_button(self, button):
        self.buttons.append(button)

    def draw(self):
        pygame.draw.rect(Display.fake_display, self.color, self.rect)
        for button in self.buttons:
            button.draw()

