import pygame
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
    def button_pressed(cls, button):
        mappings = {"MONE": 0, "MMIDDLE": 1, "MTWO": 2}
        return cls.__dict__["MOUSEBUTTON"][mappings[button]]

    @classmethod
    def update(cls):
        cls.Rect = pygame.draw.circle(Display.fake_display, (250, 0, 0, 0), pygame.mouse.get_pos(), 5, 0)
