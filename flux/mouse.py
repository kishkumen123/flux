import pygame
from layer import Layer
from screen import Display


class Mouse:
    Rect = pygame.draw.circle(Display.fake_display, (250, 0, 0, 0), pygame.mouse.get_pos(), 5, 0)

    @classmethod
    def get_pos(cls):
        return pygame.mouse.get_pos()

    @classmethod
    def get_rect(cls):
        return cls.Rect

    @classmethod
    def button_pressed(cls, button, layer="layer_0"):
        if layer == Layer.get_layer() or layer == "layer_all":
            mappings = {"MONE": 0, "MMIDDLE": 1, "MTWO": 2, "WUP": 4, "WDOWN": 5}
            return cls.__dict__["MOUSEBUTTON"][mappings[button]]
        return False

    @classmethod
    def update(cls):
        cls.Rect = pygame.draw.circle(Display.fake_display, (250, 0, 0, 0), pygame.mouse.get_pos(), 5, 0)
