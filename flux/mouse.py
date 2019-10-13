import globals
import pygame

from events import events
from layer import Layer
from screen import Display


class Mouse:

    def __init__(self):
        self.rect = pygame.draw.circle(Display.fake_display, (250, 0, 0, 0), pygame.mouse.get_pos(), 5, 0)
        self.focus = None

    def get_pos(self):
        return pygame.mouse.get_pos()

    def get_rect(self):
        return self.rect

    def button_pressed(self, button, layer="layer_0"):
        if layer == Layer.get_layer() or layer == "layer_all":
            mappings = {"MONE": 0, "MMIDDLE": 1, "MTWO": 2, "WUP": 4, "WDOWN": 5}
            return self.__dict__["MOUSEBUTTON"][mappings[button]]
        return False

    def contains(self, rect):
        self.rect.contains(rect)

    def update(self):
        self.rect = pygame.draw.circle(Display.fake_display, (250, 0, 0, 0), pygame.mouse.get_pos(), 5, 0)

        for obj in globals.poly_dict:
            if obj.contains(self.rect):
                if events.button_pressed("MONE"):
                    self.focus = obj

        #print(self.focus)


mouse = Mouse()
