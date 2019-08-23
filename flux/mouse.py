import pygame
from screen import Display


class Mouse:

    MOUSEBUTTON = {
        0: False,
        1: False,
        2: False
    }

    buttons = ()

    Rect = pygame.draw.circle(Display.fake_display, (250, 0, 0, 0), pygame.mouse.get_pos(), 5, 0)

    @classmethod
    def get_pos(cls):
        return pygame.mouse.get_pos()

    @classmethod
    def get_rect(cls):
        return cls.Rect

    @classmethod
    def event_active(cls, event):
        event_value = cls.__dict__[event]
        event_dict = {event.type: event for event in cls.buttons}
        return event_dict.get(event_value)

    @classmethod
    def button_pressed(cls, button):
        mappings = {"MONE": 0, "MMIDDLE": 1, "MTWO": 2}
        return cls.__dict__["MOUSEBUTTON"][mappings[button]]

    @classmethod
    def update(cls):
        cls.buttons = pygame.mouse.get_pressed()

        cls.MOUSEBUTTON[0] = bool(cls.buttons[0])
        cls.MOUSEBUTTON[1] = bool(cls.buttons[1])
        cls.MOUSEBUTTON[2] = bool(cls.buttons[2])

        cls.Rect = pygame.draw.circle(Display.fake_display, (250, 0, 0, 0), pygame.mouse.get_pos(), 5, 0)
